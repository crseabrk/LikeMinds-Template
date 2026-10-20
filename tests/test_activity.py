#!/usr/bin/env python3
"""Inactivity boundaries, conservative evidence, reactivation, CAS and planner integration."""
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import activity
import lmtr

NOW = datetime(2026, 10, 20, 12, tzinfo=timezone.utc)


def write(root, path, text):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def fixture(root, age=8, project_age=31):
    stamp = (NOW - timedelta(days=age)).isoformat()
    write(root, 'installation.yml', 'installed: true\n')
    write(root, 'system/AGENTS.md', '# Registry\n\n| Stable role | State | Last confirmed |\n|---|---|---|\n| Agent One | ACTIVE | ' + stamp + ' |\n')
    write(root, 'ROUTING.md', '| Project | Path | State |\n|---|---|---|\n| Demo | `projects/demo/` | ACTIVE |\n')
    write(root, 'projects/demo/CHAT.md', '### DEMO-001 — ' + (NOW - timedelta(days=project_age)).isoformat() + '\nFrom: Someone Else\nType: HANDOFF\n\nCompleted work.\n')


def raises(fn):
    try:
        fn()
    except activity.ActivityError:
        return
    raise AssertionError('expected conservative rejection')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture(root)
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        report = activity.evaluate(root, NOW)
        assert report['agents']['Agent One']['effective_state'] == 'INACTIVE'
        assert report['projects']['demo']['effective_state'] == 'STALE'
        activity.change(root, report['input_sha256'], 'reconcile', now=NOW)
        assert all((root / p).read_bytes() == value for p, value in before.items())
        assert json.loads((root / 'system/INACTIVITY.json').read_text())['agents']['Agent One']['declared_state'] == 'ACTIVE'
        # New activity revives eligibility, never rewrites membership or a cursor.
        activity.change(root, report['input_sha256'], 'record', subject_type='agent', subject='Agent One', kind='RESUME', summary='Human requested renewed work', now=NOW)
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'ACTIVE'
        assert activity.evaluate(root, NOW)['projects']['demo']['effective_state'] == 'STALE'
        raises(lambda: activity.change(root, report['input_sha256'], 'reconcile', now=NOW))
        current = activity.evaluate(root, NOW)
        activity.change(root, current['input_sha256'], 'record', subject_type='project', subject='demo', kind='WORK', summary='Project work resumed', now=NOW + timedelta(seconds=1))
        assert activity.evaluate(root, NOW + timedelta(seconds=1))['projects']['demo']['effective_state'] == 'ACTIVE'
        assert len(json.loads((root / 'system/ACTIVITY.json').read_text())['events']) == 2
        # A conflicting edit to ANY evidence invalidates a plan.
        current = activity.evaluate(root, NOW + timedelta(seconds=1))
        write(root, 'system/CHAT.md', 'new data')
        raises(lambda: activity.change(root, current['input_sha256'], 'reconcile', now=NOW + timedelta(seconds=1)))

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture(root, age=7, project_age=30)
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'INACTIVE'
        assert activity.evaluate(root, NOW - timedelta(seconds=1))['agents']['Agent One']['effective_state'] == 'ACTIVE'
        assert activity.evaluate(root, NOW)['projects']['demo']['effective_state'] == 'STALE'
        fixture(root, age=-1)
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'UNKNOWN'
        fixture(root)
        write(root, 'system/AGENTS.md', '| Stable role | State | Last confirmed |\n|---|---|---|\n| Agent One | ACTIVE | — |\n')
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'UNKNOWN'
        write(root, 'system/CHAT.md', '### BAD-001 — nonsense\nFrom: Agent One\nType: STATUS\n')
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'UNKNOWN'

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture(root)
        # Polling and heartbeat leases alone must not extend useful activity.
        write(root, 'system/CHAT.md', f'### POLL-001 — {NOW.isoformat()}\nFrom: Agent One\nType: STATUS\nActivity: POLL\n')
        write(root, 'system/PRESENCE.json', json.dumps({'version': 1, 'sessions': {'Agent One': {'last_seen': NOW.isoformat(), 'interval_seconds': 180, 'exit_state': 'OPEN'}}}))
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'INACTIVE'
        prior = lmtr.ROOT
        lmtr.ROOT = root
        try:
            assert lmtr.detect_state(activity.evaluate(root, NOW)) == 'RECOVER'
            assert lmtr.effective_presence(activity.evaluate(root, NOW))['collaboration_state'] == 'NOBODY'
        finally:
            lmtr.ROOT = prior
        write(root, 'system/CHAT.md', f'### WORK-001 — {NOW.isoformat()}\nFrom: Agent One (nickname)\nType: HANDOFF\nMeaningful progress\n')
        assert activity.evaluate(root, NOW)['agents']['Agent One']['effective_state'] == 'ACTIVE'
        # Paused/finished states are never implicitly activated.
        write(root, 'ROUTING.md', '| Project | Path | State |\n|---|---|---|\n| Demo | `projects/demo/` | FINISHED |\n')
        assert activity.evaluate(root, NOW)['projects']['demo']['effective_state'] == 'FINISHED'
        report = activity.evaluate(root, NOW)
        raises(lambda: activity.change(root, report['input_sha256'], 'record', subject_type='project', subject='demo', kind='RESUME', summary='No reopening', now=NOW))
        write(root, 'system/ACTIVITY.json', '{broken')
        raises(lambda: activity.evaluate(root, NOW))
        write(root, 'system/ACTIVITY.json', json.dumps({'version': 1, 'policy': {'agent_idle_days': True, 'project_stale_days': 30}, 'events': []}))
        raises(lambda: activity.evaluate(root, NOW))

    # Identity-directory mode never falls back to legacy ACTIVE rows.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture(root)
        (root / 'system/identities').mkdir()
        assert activity.evaluate(root, NOW)['agents'] == {}
        spec = importlib.util.spec_from_file_location('test_lmtr_fixture', ROOT / 'tests/test_lmtr.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ident = module.identity(0, 'ACTIVE')
        write(root, 'system/identities/agt-scale-000.json', json.dumps(ident))
        assert activity.evaluate(root, NOW)['agents']['agt-scale-000']['effective_state'] == 'INACTIVE'
        ident['updated_at'] = NOW.isoformat()
        write(root, 'system/identities/agt-scale-000.json', json.dumps(ident))
        assert activity.evaluate(root, NOW)['agents']['agt-scale-000']['effective_state'] == 'ACTIVE'
        write(root, 'projects/demo/CHAT.md', f'### FUTURE-001 — {(NOW + timedelta(days=1)).isoformat()}\nFrom: Agent\nType: STATUS\n')
        assert activity.evaluate(root, NOW)['projects']['demo']['effective_state'] == 'UNKNOWN'
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture(root)
        routing = '| Route | Path | State |\n|---|---|---|\n| System | system/ | ACTIVE |\n| Demo | projects/demo/ | PAUSED |\n'
        write(root, 'ROUTING.md', routing)
        plan = activity.admission(root, ['demo'], NOW)
        assert plan['state'] == 'OWNER_INVITED_RECOVERY'
        assert plan['required_acknowledgements'] == []
        assert 'Agent One' in plan['excluded_approvers']
        assert plan['activation_authorized'] is False
        # A returning peer changes both fingerprint and required quorum.
        write(root, 'system/CHAT.md', f'### RETURN — {NOW.isoformat()}\nFrom: Agent One\nType: HANDOFF\n')
        fresh = activity.admission(root, ['demo'], NOW)
        assert fresh['state'] == 'AWAIT_ACKS'
        assert fresh['required_acknowledgements'] == ['Agent One']
        assert fresh['input_sha256'] != plan['input_sha256']
        assert activity.admission(root, ['missing'], NOW)['state'] == 'RECOVER'
        write(root, 'system/CHAT.md', '### BAD — bad-date\nFrom: Agent One\nType: HANDOFF\n')
        assert activity.admission(root, ['demo'], NOW)['state'] == 'RECOVER'
        (root / 'system/CHAT.md').unlink()
        (root / 'system/identities').mkdir()
        ident = module.identity(0, 'ACTIVE')
        write(root, 'system/identities/agt-scale-000.json', json.dumps(ident))
        routing = '| Route | Path | Admission agent IDs | State |\n|---|---|---|---|\n| System | system/ | agt-scale-000 | ACTIVE |\n| Demo | projects/demo/ | agt-scale-000 | PAUSED |\n'
        write(root, 'ROUTING.md', routing)
        assert activity.admission(root, ['demo'], NOW)['state'] == 'OWNER_INVITED_RECOVERY'
        ident['updated_at'] = NOW.isoformat()
        write(root, 'system/identities/agt-scale-000.json', json.dumps(ident))
        assert activity.admission(root, ['demo'], NOW)['required_acknowledgements'] == ['agt-scale-000']
        write(root, 'ROUTING.md', routing.replace('agt-scale-000', 'missing'))
        assert activity.admission(root, ['demo'], NOW)['state'] == 'RECOVER'
    print('Inactivity checks passed: thresholds, unknown evidence, polling exclusion, identity/legacy modes, CAS, recovery, history preservation.')


if __name__ == '__main__':
    main()
