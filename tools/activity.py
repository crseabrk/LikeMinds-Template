#!/usr/bin/env python3
"""Evidence-based inactivity reports; no identity, route or heartbeat mutation."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = {"agent_idle_days": 7, "project_stale_days": 30}
EVENT_KINDS = {"WORK", "HANDOFF", "ACK", "RESUME"}


class ActivityError(Exception):
    pass


def timestamp(value):
    if not isinstance(value, str):
        raise ActivityError("timestamp must be a string")
    try:
        # A historical date-only entry means end of that UTC day, conservatively.
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return datetime.fromisoformat(value).replace(tzinfo=timezone.utc) + timedelta(days=1) - timedelta(microseconds=1)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError()
        return parsed.astimezone(timezone.utc)
    except ValueError as exc:
        raise ActivityError(f"invalid or timezone-free timestamp: {value}") from exc


def read(root, rel):
    path = root / rel
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ActivityError(f"unsafe input: {rel}")
    try:
        return path.read_text(encoding="utf-8") if path.exists() else None
    except (OSError, UnicodeError) as exc:
        raise ActivityError(f"cannot read {rel}: {exc}") from exc


def inputs(root):
    names = {"ROUTING.md", "system/AGENTS.md", "system/ACTIVITY.json", "system/PRESENCE.json"}
    for directory, pattern in (("system/identities", "*.json"), ("system", "CHAT.md"), ("projects", "*/CHAT.md")):
        base = root / directory
        if base.is_symlink():
            raise ActivityError(f"unsafe input directory: {directory}")
        if base.exists():
            names.update(p.relative_to(root).as_posix() for p in base.glob(pattern))
    # Resolve parents too: a project directory must not redirect outside the checkout.
    for name in names:
        if (root / name).resolve().is_relative_to(root.resolve()) is False:
            raise ActivityError(f"input escapes repository: {name}")
    return {name: read(root, name) for name in sorted(names)}


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def ledger(raw):
    if raw is None:
        return {"version": 1, "policy": dict(DEFAULT_POLICY), "events": []}
    try:
        data = json.loads(raw)
    except (ValueError, TypeError) as exc:
        raise ActivityError("invalid system/ACTIVITY.json") from exc
    if not isinstance(data, dict) or set(data) != {"version", "policy", "events"} or data["version"] != 1:
        raise ActivityError("unsupported activity ledger")
    policy = data["policy"]
    if not isinstance(policy, dict) or set(policy) != set(DEFAULT_POLICY):
        raise ActivityError("invalid inactivity policy")
    for name, value in policy.items():
        if type(value) is not int or not 1 <= value <= 3650:
            raise ActivityError(f"{name} must be an integer from 1 to 3650")
    if not isinstance(data["events"], list):
        raise ActivityError("activity events must be a list")
    ids = set()
    for event in data["events"]:
        if not isinstance(event, dict) or set(event) != {"id", "subject_type", "subject", "at", "kind", "summary"}:
            raise ActivityError("invalid activity event")
        if not isinstance(event["id"], str) or not event["id"] or event["id"] in ids:
            raise ActivityError("duplicate or invalid event ID")
        ids.add(event["id"])
        if event["subject_type"] not in {"agent", "project"} or event["kind"] not in EVENT_KINDS:
            raise ActivityError("invalid event subject type or kind; polling is not activity")
        if any(not isinstance(event[k], str) or not event[k].strip() or len(event[k]) > 1000 for k in ("subject", "summary")):
            raise ActivityError("event subject and summary must be nonempty text")
        timestamp(event["at"])
    return data


def tables(text):
    header = None
    for line in (text or "").splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [x.strip().strip('`') for x in line.strip('|').split('|')]
        if all(re.fullmatch(r"[: -]+", x) for x in cells):
            continue
        if header is None:
            header = cells
        elif len(cells) == len(header):
            yield dict(zip(header, cells))


def discover(data, directory_exists=False):
    agents, projects = {}, {}
    identities = [p for p in data if p.startswith('system/identities/')]
    # An existing directory is authoritative; never mix immutable IDs with legacy roles.
    if directory_exists:
        for path in identities:
            try:
                obj = json.loads(data[path])
                key, state, name = obj['agent_id'], obj['membership_state'], obj['display_name']
                if Path(path).name != key + '.json' or key in agents:
                    raise ValueError()
                if state not in {'ACTIVE', 'PAUSED', 'RETIRED', 'BLOCKED', 'PROPOSED', 'ACKNOWLEDGING'}:
                    raise ValueError()
                aliases = [key, name, *obj.get('previous_display_names', [])]
                if any(not isinstance(v, str) for v in aliases):
                    raise ValueError()
                agents[key] = {'state': state, 'aliases': aliases, 'evidence': [(obj['updated_at'], path)]}
            except (KeyError, TypeError, ValueError) as exc:
                raise ActivityError(f"invalid identity input: {path}") from exc
    else:
        registry = re.sub(r'```.*?```', '', data.get('system/AGENTS.md') or '', flags=re.S)
        for row in tables(registry):
            key = row.get('Stable role') or row.get('Agent role')
            if key:
                if key in agents:
                    raise ActivityError(f"duplicate legacy role: {key}")
                date = row.get('Last confirmed') or row.get('Joined at')
                agents[key] = {'state': row.get('State', 'UNKNOWN'), 'aliases': [key], 'evidence': [(date, 'system/AGENTS.md')] if date and date != '—' else []}
        for block in re.split(r'^### ', registry, flags=re.M)[1:]:
            title = block.splitlines()[0].strip()
            fields = dict(re.findall(r'^([A-Za-z-]+):\s*(.*)$', block, re.M))
            if 'State' not in fields:
                continue
            if title in agents:
                raise ActivityError(f"duplicate legacy role: {title}")
            dates = [(fields[k], 'system/AGENTS.md') for k in ('Proposed-At', 'Activated-At', 'Last-Confirmed') if fields.get(k) and fields[k] != '—']
            agents[title] = {'state': fields['State'], 'aliases': [title], 'evidence': dates}
    for row in tables(data.get('ROUTING.md')):
        path = row.get('Path', '').rstrip('/')
        if path.startswith('projects/'):
            if not re.fullmatch(r'projects/[a-z0-9][a-z0-9_-]*', path):
                raise ActivityError(f"unsafe project route: {path}")
            key = path.split('/')[1]
            if key in projects:
                raise ActivityError(f"duplicate project route: {key}")
            projects[key] = {'state': row.get('State', 'UNKNOWN'), 'aliases': [], 'evidence': []}
    return agents, projects


def evaluate(root=ROOT, now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ActivityError('evaluation clock requires a timezone')
    data = inputs(root)
    log = ledger(data['system/ACTIVITY.json'])
    agents, projects = discover(data, (root / "system/identities").exists())
    # Older Markdown messages are evidence, except explicitly identified idle polls.
    for path, text in data.items():
        if not path.endswith('/CHAT.md') or text is None:
            continue
        project = path.split('/')[1] if path.startswith('projects/') else None
        for block in re.split(r'^### ', re.sub(r'```.*?```', '', text, flags=re.S), flags=re.M)[1:]:
            first = block.splitlines()[0]
            if ' — ' not in first:
                continue
            date = first.split(' — ', 1)[1].strip()
            fields = dict(re.findall(r'^(From|Type|Activity):\s*(.*)$', block, re.M))
            if fields.get('Activity') == 'POLL' or fields.get('Type') in {'POLL', 'HEARTBEAT'}:
                continue
            if project in projects:
                projects[project]['evidence'].append((date, path))
            author = fields.get('From', '')
            for agent in agents.values():
                if any(author == alias or author.startswith(alias + ' (') for alias in agent['aliases']):
                    agent['evidence'].append((date, path))
    for event in log['events']:
        subjects = agents if event['subject_type'] == 'agent' else projects
        if event['subject'] not in subjects:
            raise ActivityError(f"activity event references an unknown {event['subject_type']}: {event['subject']}")
        subjects[event['subject']]['evidence'].append((event['at'], 'system/ACTIVITY.json#' + event['id']))

    def classify(items, days, inactive):
        result = {}
        for key, item in items.items():
            dates, errors = [], []
            for value, source in item['evidence']:
                try:
                    date = timestamp(value)
                    if date > now:
                        # Same-day date-only registry values are conservative, not future clock errors.
                        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(value)) and date.date() == now.date():
                            date = now
                        else:
                            raise ActivityError('future timestamp')
                    dates.append((date, source))
                except ActivityError as exc:
                    errors.append(f'{source}: {exc}')
            latest = max(dates) if dates else None
            age = (now - latest[0]).total_seconds() if latest else None
            if item['state'] != 'ACTIVE':
                effective = item['state']
            elif errors or latest is None:
                effective = 'UNKNOWN'
            else:
                effective = inactive if age >= days * 86400 else 'ACTIVE'
            result[key] = {'declared_state': item['state'], 'effective_state': effective,
                           'last_activity': latest[0].isoformat() if latest else None,
                           'age_days': round(age / 86400, 3) if age is not None else None,
                           'evidence': latest[1] if latest else None,
                           'problems': errors or (['No dated activity evidence'] if latest is None else [])}
        return result

    return {'version': 1, 'evaluated_at': now.isoformat(), 'input_sha256': fingerprint(data),
            'policy': log['policy'],
            'agents': classify(agents, log['policy']['agent_idle_days'], 'INACTIVE'),
            'projects': classify(projects, log['policy']['project_stale_days'], 'STALE')}


def admission(root=ROOT, routes=(), now=None):
    """Read-only quorum calculation. Never treats exclusions as ACKs or activates anyone."""
    report = evaluate(root, now)
    directory = (root / 'system/identities').exists()
    required, blocked = set(), []
    route_rows = list(tables(read(root, 'ROUTING.md')))
    wanted = {'system', *routes}
    found = set()
    for row in route_rows:
        path = row.get('Path', '').rstrip('/')
        route = 'system' if path == 'system' else path.removeprefix('projects/')
        if route not in wanted:
            continue
        if route in found:
            blocked.append(f'duplicate route: {route}')
        found.add(route)
        if directory:
            ids = [v.strip().strip('`') for v in row.get('Admission agent IDs', '').split(',') if v.strip()]
            if not 1 <= len(ids) <= 3 or len(set(ids)) != len(ids):
                blocked.append(f'missing or ambiguous admission configuration: {route}')
            required.update(ids)
    blocked.extend(f'missing requested route: {route}' for route in sorted(wanted - found))
    if not directory:
        # Legacy all-participant membership is filtered by evidence, not silence.
        required = {key for key, value in report['agents'].items() if value['declared_state'] == 'ACTIVE'}
    eligible, excluded = [], {}
    for key in sorted(required):
        item = report['agents'].get(key)
        if item is None or item['effective_state'] == 'UNKNOWN':
            blocked.append(f'unresolved approver: {key}')
        elif item['effective_state'] == 'ACTIVE':
            eligible.append(key)
        elif item['effective_state'] in {'INACTIVE', 'PAUSED', 'RETIRED'}:
            excluded[key] = item
        else:
            blocked.append(f'ineligible configured approver: {key}')
    return {'version': 1, 'evaluated_at': report['evaluated_at'],
            'input_sha256': report['input_sha256'], 'policy': report['policy'],
            'mode': 'directory' if directory else 'legacy', 'routes': sorted(wanted),
            'required_acknowledgements': eligible, 'excluded_approvers': excluded,
            'blockers': blocked,
            'state': 'RECOVER' if blocked else ('AWAIT_ACKS' if eligible else 'OWNER_INVITED_RECOVERY'),
            'activation_authorized': False}


def atomic_json(root, relative, value):
    dest = root / relative
    if dest.is_symlink() or dest.parent.is_symlink():
        raise ActivityError('unsafe output path')
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp = dest.with_suffix('.tmp')
    if temp.exists():
        raise ActivityError(f'output temporary file exists: {temp.name}')
    try:
        with temp.open('x', encoding='utf-8') as stream:
            stream.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
        temp.replace(dest)
    finally:
        if temp.exists():
            temp.unlink()


def change(root, expected, command, *, subject_type=None, subject=None, kind=None, summary=None, now=None):
    """CAS over all evidence, plus a local exclusive writer lock. Remote writers still need blob SHA CAS."""
    lock = root / '.likeminds' / 'activity.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        stream = lock.open('x')
    except FileExistsError as exc:
        raise ActivityError('another local activity writer holds the lock') from exc
    try:
        stream.close()
        report = evaluate(root, now)
        if expected != report['input_sha256']:
            raise ActivityError('evidence changed; reread the report before writing')
        if command == 'reconcile':
            atomic_json(root, 'system/INACTIVITY.json', report)
        elif command == 'record':
            group = report['agents' if subject_type == 'agent' else 'projects']
            if subject not in group or group[subject]['declared_state'] != 'ACTIVE':
                raise ActivityError('record requires a known declared ACTIVE subject; admission/route changes are separate')
            log = ledger(read(root, 'system/ACTIVITY.json'))
            event = {'id': 'activity-' + report['evaluated_at'], 'subject_type': subject_type, 'subject': subject,
                     'at': report['evaluated_at'], 'kind': kind, 'summary': summary}
            log['events'].append(event)
            ledger(json.dumps(log))  # Validate the complete append before writing anything.
            atomic_json(root, 'system/ACTIVITY.json', log)
        else:
            raise ActivityError('unknown mutation')
        return report if command == 'reconcile' else evaluate(root, now)
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('report', 'admission', 'reconcile', 'record'), nargs='?', default='report')
    parser.add_argument('--route', action='append', default=[], help='requested project slug for admission; repeatable')
    parser.add_argument('--expect', help='input_sha256 from a fresh report; required for writes')
    parser.add_argument('--subject-type', choices=('agent', 'project'))
    parser.add_argument('--subject')
    parser.add_argument('--kind', choices=sorted(EVENT_KINDS))
    parser.add_argument('--summary')
    args = parser.parse_args()
    try:
        if args.command == 'report':
            result = evaluate()
        elif args.command == 'admission':
            result = admission(routes=args.route)
        else:
            if not args.expect:
                raise ActivityError('--expect is required for writes')
            if args.command == 'record' and not all((args.subject_type, args.subject, args.kind, args.summary)):
                raise ActivityError('record requires --subject-type, --subject, --kind and --summary')
            result = change(ROOT, args.expect, args.command, subject_type=args.subject_type, subject=args.subject,
                            kind=args.kind, summary=args.summary)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ActivityError, OSError) as exc:
        print(f'ACTIVITY-E001 {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
