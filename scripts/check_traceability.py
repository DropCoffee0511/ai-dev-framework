#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_traceability.py — Traceability Convention §3–§5 자동 계산 (NEXT.md 구현 후보 2)

`docs/traceability-convention.md`(이하 convention)의 계산 규칙을 저장소에 적용해
REQ별 차원 판정(§3), REQ 상태 계산(§4), Gate 기록의 현재 값(§5)을 계산한다.
이 스크립트는 **계산기**다. 규칙의 단일 출처는 convention이며 이 파일은 규칙을
추가하거나 완화하지 않는다. 계산하지 못하는 항목은 PASS 대신 보수적으로
PARTIAL/MISSING과 비고로 남긴다 (거짓 DONE 방지 — MASTER_PROMPT §21).

사용:
    python3 scripts/check_traceability.py [ROOT]          # 저장소 검사
    python3 scripts/check_traceability.py --self-test     # 내장 픽스처 시험 (§3–§5 사례)

종료 코드: 0 = 계산 완료(구조 위반 없음. MISSING 상태는 위반이 아니라 정상 상태다),
1 = 구조 위반 존재(dangling 참조, 허용되지 않은 not_applicable, 형식 위반 기록 줄 등),
2 = 실행 오류 또는 내장 시험 실패. --self-test는 임시 디렉터리에 git 저장소를
만들므로 git이 실행 가능해야 한다.

v0 한계 (convention §5.4·§6의 수동 절차를 대체하지 않는다):
- Requirement의 "검증 불가능한 문구"(PARTIAL 사유)는 문맥 판단이 필요해 계산하지 않는다.
- not_applicable 사유의 타당성과 판정자 칸의 진위(위조)는 검사하지 않는다 (§5.4).
- Tests의 "실행 시점 커밋 이후 코드 변경 시 재실행" 규칙(§4)은 검사하지 않는다.
  (Gate 재판정 §5.3 확인은 Review 차원 계산에서만 수행한다.)
- yaml 파서는 convention §2의 제한된 형식(list·중첩 acceptance·not_applicable 사전)만
  이해한다. 문자열 값은 큰따옴표 또는 무따옴표, 주석은 행 단위(# 시작)만 지원한다.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

ID_RE = r'(?:REQ|AC|WF|SCR|API|DATA|PERM|ERR|TC|TASK)-\d{3,}'
DEF_DOC = {
    'REQ': 'docs/02_requirements.md',
    'AC': 'docs/02_requirements.md',
    'WF': 'docs/03_workflow.md',
    'SCR': 'docs/04_screens.md',
    'API': 'docs/04_screens.md',
    'DATA': 'docs/05_data_model.md',
    'PERM': 'docs/06_permissions.md',
    'ERR': 'docs/08_error_cases.md',
    'TC': 'docs/09_test_cases.md',
}
# convention §2: not_applicable을 쓸 수 있는 차원
NA_ALLOWED = ('workflow', 'screen_api', 'data', 'permission', 'error_cases')
LIST_KEYS = ('workflow', 'screen_api', 'data', 'permission', 'error_cases',
             'tests', 'tasks', 'code')
DIM_ORDER = ['Requirement', 'Workflow', 'Screen/API', 'Data', 'Permission',
             'Error Cases', 'Tests', 'Implementation', 'Review']
# convention §5.2 Gate별 기록자
USER_ONLY_GATES = {'APPROVAL_SPEC', 'APPROVAL_IMPLEMENTATION', 'ACCEPTANCE'}
REVIEWER_USER_GATES = {'PLAN_REVIEW_PASS', 'IMPLEMENTATION_REVIEW_PASS',
                       'NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS',
                       'TRACEABILITY_COMPLETE', 'NO_CRITICAL_OPEN_ISSUES',
                       'B_FINAL'}


def find_ids(text, prefixes):
    rx = re.compile(r'\b(?:%s)-\d{3,}\b' % '|'.join(prefixes))
    return set(rx.findall(text))


def split_row(line):
    s = line.strip()
    if not s.startswith('|'):
        return None
    cells = [c.strip() for c in s.strip('|').split('|')]
    if cells and all(re.fullmatch(r':?-+:?', c) for c in cells if c):
        return None  # 표 구분선
    return cells


def read_text(root, rel):
    try:
        with open(os.path.join(root, rel), encoding='utf-8') as f:
            return f.read()
    except OSError:
        return None


# ---------------------------------------------------------------- 레지스트리

class Registry:
    """정의 문서들에서 수집한 ID 등록 상태 (convention §1)."""

    def __init__(self):
        self.ids = {p: set() for p in DEF_DOC}
        self.ids['TASK'] = set()  # specs/*/tasks.md에서 수집
        self.req_detail = {}      # req -> {retired, has_detail, acs, perms, errs}
        self.perm_server = {}     # perm -> 서버/API 검사 위치 칸이 채워져 있는가
        self.perm_tcs = {}        # perm -> 필수 권한 테스트 TC 집합 (06 표)
        self.tc_result = {}       # tc -> 케이스 목록의 결과 칸 값
        self.tc_targets = {}      # tc -> 대상 칸의 ID 집합
        self.tc_code = {}         # tc -> 테스트 코드 위치 칸
        self.tc_evidence = set()  # 실행 증거 표에 PASS 줄이 있는 TC
        self.missing_docs = []

    def effective_tc_result(self, tc):
        """convention §4: 증거 없는 PASS는 NOT RUN이다. 목록에 없어도 NOT RUN이다."""
        raw = self.tc_result.get(tc)
        if raw is None:
            return 'NOT RUN'
        if raw == 'PASS' and tc not in self.tc_evidence:
            return 'NOT RUN'
        return raw


def _new_req():
    return {'retired': False, 'has_detail': False,
            'acs': {}, 'perms': set(), 'errs': set()}


def parse_registry(root):
    reg = Registry()
    _parse_requirements(root, reg)
    _parse_permissions(root, reg)
    _parse_test_cases(root, reg)
    for prefix in ('WF', 'SCR', 'API', 'DATA', 'ERR'):
        text = read_text(root, DEF_DOC[prefix])
        if text is None:
            reg.missing_docs.append(DEF_DOC[prefix])
            continue
        reg.ids[prefix] |= find_ids(text, {prefix})
    for tasks in _specs_files(root, 'tasks.md'):
        text = read_text(root, tasks)
        if text:
            reg.ids['TASK'] |= find_ids(text, {'TASK'})
    return reg


def _parse_requirements(root, reg):
    rel = DEF_DOC['REQ']
    text = read_text(root, rel)
    if text is None:
        reg.missing_docs.append(rel)
        return
    current = None
    for line in text.splitlines():
        heading = re.match(r'^#{2,6}\s+(.*)$', line)
        if heading:
            m = re.search(r'\b(REQ-\d{3,})\b', heading.group(1))
            current = None
            if m:
                current = m.group(1)
                reg.req_detail.setdefault(current, _new_req())['has_detail'] = True
        for rid in find_ids(line, {'REQ'}):
            d = reg.req_detail.setdefault(rid, _new_req())
            if 'RETIRED' in line:
                d['retired'] = True
        if current is not None:
            d = reg.req_detail[current]
            for ac in find_ids(line, {'AC'}):
                d['acs'][ac] = 'RETIRED' in line
            d['perms'] |= find_ids(line, {'PERM'})
            d['errs'] |= find_ids(line, {'ERR'})
    reg.ids['REQ'] = set(reg.req_detail)
    for d in reg.req_detail.values():
        reg.ids['AC'] |= set(d['acs'])


def _parse_permissions(root, reg):
    rel = DEF_DOC['PERM']
    text = read_text(root, rel)
    if text is None:
        reg.missing_docs.append(rel)
        return
    section = ''
    for line in text.splitlines():
        heading = re.match(r'^#{2,6}\s+(.*)$', line)
        if heading:
            section = heading.group(1)
        cells = split_row(line)
        if not cells or not cells[0]:
            continue
        perms = find_ids(line, {'PERM'})
        reg.ids['PERM'] |= perms
        if re.search(r'검사 위치', section) and len(cells) >= 3 \
                and re.fullmatch(ID_RE, cells[0]):
            val = cells[2]
            reg.perm_server[cells[0]] = bool(val) and '<' not in val
        if re.search(r'필수 권한 테스트', section) and cells[0] in perms:
            reg.perm_tcs[cells[0]] = find_ids(line, {'TC'})


def _parse_test_cases(root, reg):
    rel = DEF_DOC['TC']
    text = read_text(root, rel)
    if text is None:
        reg.missing_docs.append(rel)
        return
    section = ''
    for line in text.splitlines():
        heading = re.match(r'^#{2,6}\s+(.*)$', line)
        if heading:
            section = heading.group(1)
        cells = split_row(line)
        if not cells or not cells[0]:
            continue
        reg.ids['TC'] |= find_ids(line, {'TC'})
        if re.search(r'케이스 목록', section) and re.fullmatch(ID_RE, cells[0]):
            reg.tc_result[cells[0]] = cells[-1].upper()
            reg.tc_targets[cells[0]] = find_ids(line, {'AC', 'ERR', 'PERM'})
            reg.tc_code[cells[0]] = cells[5] if len(cells) > 5 else ''
        elif re.search(r'실행 증거', section) and len(cells) >= 2 \
                and re.fullmatch(ID_RE, cells[0]) and cells[1].upper() == 'PASS':
            reg.tc_evidence.add(cells[0])


def _specs_files(root, name):
    specs = os.path.join(root, 'specs')
    out = []
    if os.path.isdir(specs):
        for cid in sorted(os.listdir(specs)):
            p = os.path.join('specs', cid, name)
            if os.path.isfile(os.path.join(root, p)):
                out.append(p)
    return out


# ------------------------------------------------------- traceability.md 파싱

def parse_traceability(text):
    """convention §2의 제한된 YAML 블록을 파싱한다. (entries, problems) 반환."""
    blocks, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        if re.match(r'^```yaml\s*$', lines[i]):
            j = i + 1
            block = []
            while j < len(lines) and not re.match(r'^```\s*$', lines[j]):
                block.append(lines[j])
                j += 1
            blocks.append(block)
            i = j + 1
        else:
            i += 1

    entries, problems = [], []
    for block in blocks:
        cur, mode, na_indent = None, None, 0
        for raw in block:
            line = raw.rstrip()
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            m = re.match(r'^-\s*id:\s*(\S+)\s*$', s)
            if m:
                cur = {'id': m.group(1), 'acceptance': {}, 'not_applicable': {}}
                for k in LIST_KEYS:
                    cur[k] = []
                entries.append(cur)
                mode = None
                continue
            if cur is None:
                problems.append('id 항목 밖의 줄: "%s"' % s)
                continue
            indent = len(raw) - len(raw.lstrip())
            m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', s)
            if not m:
                problems.append('이해할 수 없는 줄: "%s"' % s)
                continue
            key, val = m.group(1), m.group(2).strip()
            if mode == 'acceptance' and re.fullmatch(ID_RE, key):
                cur['acceptance'][key] = _parse_list(val, problems, s)
                continue
            if mode == 'na':
                if indent > na_indent:
                    if key in NA_ALLOWED:
                        cur['not_applicable'][key] = val.strip().strip('"')
                    else:
                        problems.append('not_applicable은 %s에만 허용된다 (§2): %s'
                                        % (', '.join(NA_ALLOWED), key))
                    continue
                mode = None  # 들여쓰기 복귀 — 이 줄부터는 일반 키로 처리한다
            if key == 'acceptance':
                if val:
                    problems.append('acceptance는 중첩 목록이어야 한다: "%s"' % s)
                mode = 'acceptance'
                continue
            if key == 'not_applicable':
                if val in ('', '{'):
                    mode = 'na'
                    na_indent = indent
                elif val == '{}':
                    pass
                elif val.startswith('{') and val.endswith('}'):
                    for k2, v2 in re.findall(r'([A-Za-z_]+):\s*"([^"]*)"', val):
                        cur['not_applicable'][k2] = v2
                else:
                    problems.append('not_applicable 형식: "%s"' % s)
                continue
            if key in LIST_KEYS:
                mode = None
                cur[key] = _parse_list(val, problems, s)
                continue
            problems.append('알 수 없는 키: "%s"' % s)
    return entries, problems


def _parse_list(val, problems, src):
    if not val:
        return []
    if val.startswith('[') and val.endswith(']'):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [x.strip().strip('"') for x in inner.split(',')]
    problems.append('목록은 [ ... ] 형식이어야 한다: "%s"' % src)
    return [val.strip('"')]


# ---------------------------------------------------------------- gates.md

class GateRow:
    def __init__(self, cells, problems):
        self.cells = cells
        self.problems = problems
        self.valid = not problems
        self.gate = cells[1] if len(cells) > 1 else ''
        self.value = (cells[2].upper() if len(cells) > 2 and
                      cells[2].upper() in ('TRUE', 'FALSE', 'STALE') else None)
        self.judge = cells[3] if len(cells) > 3 else ''
        self.evidence = cells[4] if len(cells) > 4 else ''
        m = re.search(r'\b([0-9a-f]{7,40})\b', self.evidence)
        self.commit = m.group(1) if m else None


def parse_gates(text):
    """맨 아래 `## 기록` 구역의 표만 읽는다 (convention §5.1). 이력 구역은 제외."""
    lines = text.splitlines()
    heads = []
    for n, l in enumerate(lines):
        m = re.match(r'^#{1,6}\s+(.*)$', l)
        if m:
            heads.append((n, m.group(1).strip()))
    head_nums = [n for n, _ in heads]

    def section_end(n):
        return min([h for h in head_nums if h > n] + [len(lines)])

    hist = [n for n, t in heads if t.startswith('이력')]
    ignored = sum(1 for n in hist for l in lines[n:section_end(n)]
                  if (c := split_row(l)) is not None and c[0] != '일시')
    rec = [n for n, t in heads if t == '기록']
    if not rec:
        return None, [], ignored
    start = rec[-1]
    rows = []
    for n in range(start + 1, section_end(start)):
        cells = split_row(lines[n])
        if cells is None or not cells or cells[0] == '일시':
            continue  # 구분선·헤더 행
        if len(cells) != 5:
            rows.append(GateRow(cells, ['기록 표는 5칸이어야 한다 (§5.1)']))
            continue
        problems = []
        if not cells[0]:
            problems.append('일시 칸이 비어 있다')
        if cells[2].upper() not in ('TRUE', 'FALSE', 'STALE'):
            problems.append('값은 true|false|STALE이어야 한다 (§5.1): "%s"' % cells[2])
        if cells[1] in USER_ONLY_GATES and 'USER' not in cells[3]:
            problems.append('%s 기록자는 USER만이다 (§5.2): "%s"' % (cells[1], cells[3]))
        if cells[1] in REVIEWER_USER_GATES and \
                not ('REVIEWER' in cells[3] or 'USER' in cells[3]):
            problems.append('%s 기록자는 REVIEWER|USER여야 한다 (§5.2): "%s"'
                            % (cells[1], cells[3]))
        if not cells[4]:
            problems.append('근거 칸이 비어 있다 (§5.1)')
        rows.append(GateRow(cells, problems))
    return rows, [], ignored


def gate_current(rows, gate):
    """같은 Gate의 맨 아래 유효 줄이 현재 값이다 (§5.1 append-only)."""
    for row in reversed(rows):
        if row.valid and row.gate == gate:
            return row
    return None


# --------------------------------------------------------------------- git

def git_out(root, args):
    try:
        return subprocess.run(['git', '-C', root] + args,
                              capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None


def changed_since(root, commit, files):
    """convention §5.3: 커밋 이후 변경(미커밋·미추적 포함) 파일 목록. None=확인 불가."""
    files = [f for f in files if f]
    if not commit or not files:
        return None
    r = git_out(root, ['cat-file', '-t', commit])
    if r is None or r.returncode != 0:
        return None
    out = []
    for args in (['diff', '--stat', commit, '--'] + files,
                 ['status', '--short', '--'] + files):
        r = git_out(root, args)
        if r is not None:
            out += [l for l in r.stdout.splitlines() if l.strip()]
    return out


def plan_files(root, change):
    """plan.md의 "변경할 파일" 후보(존재하는 repo 상대 경로)를 수집한다 (§5.3)."""
    if not change:
        return []
    text = read_text(root, os.path.join('specs', change, 'plan.md'))
    if not text:
        return []
    out = []
    for m in re.finditer(r'[\w.-]+(?:/[\w.-]+)+', text):
        p = m.group(0)
        if os.path.isfile(os.path.join(root, p)) and p not in out:
            out.append(p)
    return out


# ------------------------------------------------------------------ 계산

class Analyzer:
    def __init__(self, root):
        self.root = root
        self.reg = parse_registry(root)
        self.violations = []  # (파일, 메시지)
        self.reqs = []        # (파일, id, dims, status, notes)
        self.gates_seen = {}

    def violation(self, path, msg):
        self.violations.append((path, msg))

    def analyze_traceability(self, rel):
        text = read_text(self.root, rel) or ''
        change = None
        m = re.match(r'specs/([^/]+)/', rel)
        if m:
            change = m.group(1)
        entries, problems = parse_traceability(text)
        for p in problems:
            self.violation(rel, p)
        spec_reqs = self._spec_scope(change)
        by_id = {e['id']: e for e in entries}
        if spec_reqs is not None:
            for r in sorted(spec_reqs - set(by_id)):
                dims = {d: ('MISSING', 'spec.md가 선언했으나 항목이 없다 (§2 범위)')
                        for d in DIM_ORDER}
                self.reqs.append((rel, r, dims, 'NOT READY',
                                  ['traceability 항목 없음']))
            for r in sorted(set(by_id) - spec_reqs):
                self.violation(rel, 'spec.md 선언 밖의 REQ 항목: %s' % r)
        gates = self._load_gates(
            os.path.join(os.path.dirname(rel), 'gates.md') if change
            else 'docs/gates.md', project=change is None)
        for e in entries:
            self._compute(e, rel, change, gates)

    def _spec_scope(self, change):
        if not change:
            return None
        text = read_text(self.root, os.path.join('specs', change, 'spec.md'))
        if text is None:
            return None
        return find_ids(text, {'REQ'})

    def _load_gates(self, rel, project):
        text = read_text(self.root, rel)
        key = 'project' if project else rel
        if key in self.gates_seen:
            return self.gates_seen[key]
        info = {'rel': rel, 'rows': [], 'ignored': 0, 'missing': text is None}
        if text is not None:
            rows, _problems, ignored = parse_gates(text)
            info['rows'], info['ignored'] = rows, ignored
            for row in rows:
                if not row.valid:
                    for p in row.problems:
                        self.violation(rel, '기록 줄: %s — %s'
                                       % (' | '.join(row.cells), p))
        self.gates_seen[key] = info
        return info

    def _valid_links(self, entry, key, path, change):
        ok = []
        for tid in entry[key]:
            m = re.match(r'\b([A-Z]+)-\d{3,}\b', tid)
            pfx = m.group(1) if m else ''
            defdoc = DEF_DOC.get(pfx)
            if pfx == 'TASK':
                known = tid in self.reg.ids['TASK']
            elif defdoc:
                known = tid in self.reg.ids.get(pfx, set())
            else:
                known = False
            if known:
                ok.append(tid)
            else:
                where = ('specs/%s/tasks.md' % change) if pfx == 'TASK' \
                    else (defdoc or '정의 위치 미정')
                self.violation(path, 'dangling 참조 (§1·§2): %s — 정의 위치 %s에 없다'
                               % (tid, where))
        return ok

    def _compute(self, e, path, change, gates):
        reg = self.reg
        rid = e['id']
        na = {k: v for k, v in e['not_applicable'].items() if v}
        for k in e['not_applicable']:
            if k not in NA_ALLOWED:
                self.violation(path, 'not_applicable은 %s에만 허용된다 (§2): %s'
                               % (', '.join(NA_ALLOWED), k))
        detail = reg.req_detail.get(rid)
        notes = []
        if rid not in reg.ids['REQ']:
            self.violation(path, '등록되지 않은 REQ (§1): %s — '
                           'docs/02_requirements.md에 없다' % rid)
        dims = {}

        wf = self._valid_links(e, 'workflow', path, change)
        scr = self._valid_links(e, 'screen_api', path, change)
        data = self._valid_links(e, 'data', path, change)
        perm = self._valid_links(e, 'permission', path, change)
        errs = self._valid_links(e, 'error_cases', path, change)
        scr_ids = {t for t in scr if t.startswith('SCR-')}
        api_ids = {t for t in scr if t.startswith('API-')}

        # Requirement (§3)
        acc = e['acceptance']
        for ac in acc:
            if ac not in reg.ids['AC']:
                self.violation(path, 'dangling 참조 (§1·§2): %s — '
                               'docs/02_requirements.md에 없다' % ac)
        if not acc:
            dims['Requirement'] = ('MISSING', 'acceptance가 비어 있다')
        elif detail and detail['has_detail']:
            active = [a for a, retired in detail['acs'].items() if not retired]
            miss = [a for a in active if a not in acc]
            if miss:
                dims['Requirement'] = (
                    'MISSING', '등록된 활성 AC 중 빠진 것: %s' % ', '.join(miss))
            else:
                dims['Requirement'] = ('PASS', '활성 AC 전부 연결')
        else:
            dims['Requirement'] = ('PASS', 'AC 연결됨 (REQ 상세 블록이 없어 '
                                          '전체 커버는 수동 확인)')
            notes.append('REQ 상세 블록 부재 — AC 전체 커버 수동 확인 필요')

        # Workflow / Data (§3: 연결 또는 사유)
        for name, links, key in (('Workflow', wf, 'workflow'),
                                 ('Data', data, 'data')):
            if na.get(key):
                dims[name] = ('PASS', 'not_applicable 사유 있음')
            elif links:
                dims[name] = ('PASS', '연결 있음')
            else:
                dims[name] = ('MISSING', '연결도 사유도 없음')

        # Screen/API (§3: 화면·API 한쪽만이면 PARTIAL)
        if na.get('screen_api'):
            dims['Screen/API'] = ('PASS', 'not_applicable 사유 있음')
        elif not scr:
            dims['Screen/API'] = ('MISSING', '연결도 사유도 없음')
        elif bool(scr_ids) != bool(api_ids):
            dims['Screen/API'] = ('PARTIAL', '화면·API 중 한쪽만 연결됨')
        else:
            dims['Screen/API'] = ('PASS', '연결 있음')

        # Permission (§3)
        if na.get('permission'):
            dims['Permission'] = ('PASS', 'not_applicable 사유 있음')
        elif not perm:
            dims['Permission'] = ('MISSING', '연결도 사유도 없음')
        else:
            partial = []
            if detail and detail['has_detail'] and detail['perms']:
                unlinked = detail['perms'] - set(perm)
                if unlinked:
                    partial.append('등록된 PERM 중 미연결: %s'
                                   % ', '.join(sorted(unlinked)))
            for p in perm:
                if not reg.perm_server.get(p, False):
                    partial.append('%s 서버/API 검사 위치 없음 (06 문서)' % p)
            if partial:
                dims['Permission'] = ('PARTIAL', '; '.join(partial))
            else:
                dims['Permission'] = ('PASS', '연결 + 서버 검사 위치 확인')

        # Error Cases (§3)
        if na.get('error_cases'):
            dims['Error Cases'] = ('PASS', 'not_applicable 사유 있음')
        elif not errs:
            dims['Error Cases'] = ('MISSING', '연결도 사유도 없음')
        elif detail and detail['has_detail'] and detail['errs'] \
                and not set(detail['errs']) <= set(errs):
            miss = detail['errs'] - set(errs)
            dims['Error Cases'] = ('PARTIAL', '등록된 ERR 중 미연결: %s'
                                   % ', '.join(sorted(miss)))
        else:
            dims['Error Cases'] = ('PASS', '연결 있음')

        # Tests (§3)
        tests = self._valid_links(e, 'tests', path, change)
        required = set()
        for tcs in acc.values():
            required |= set(tcs)
        for p in perm:
            if p in reg.perm_tcs:
                required |= reg.perm_tcs[p]
            else:
                notes.append('%s 필수 권한 테스트가 06 문서에 미정의 — 수동 확인' % p)
        tests_missing = False
        for err in errs:
            tcs_e = {tc for tc, tg in reg.tc_targets.items() if err in tg}
            if not tcs_e:
                dims['Tests'] = ('MISSING', '%s의 테스트 TC가 없다 (§2)' % err)
                tests_missing = True
                break
            required |= tcs_e
        if not tests_missing:
            if not tests or not required <= set(tests):
                miss = sorted(required - set(tests))
                dims['Tests'] = ('MISSING', 'tests가 비었거나 필요한 TC 누락: %s'
                                 % ', '.join(miss))
            else:
                bad = sorted(tc for tc in required
                             if reg.effective_tc_result(tc) != 'PASS')
                if bad:
                    dims['Tests'] = (
                        'PARTIAL',
                        'PASS 증거가 없거나 실패한 TC: %s (%s)' %
                        (', '.join(bad),
                         ', '.join(reg.effective_tc_result(tc) for tc in bad)))
                else:
                    dims['Tests'] = ('PASS', '필요 TC 전부 실행 PASS (증거 확인)')

        # Implementation (§3)
        code_ok, code_bad = [], []
        for p in e['code']:
            (code_ok if os.path.isfile(os.path.join(self.root, p))
             else code_bad).append(p)
        for p in code_bad:
            self.violation(path, 'code 경로가 존재하지 않는다 (§2): %s' % p)
        tasks = self._valid_links(e, 'tasks', path, change)
        if not e['code']:
            dims['Implementation'] = ('MISSING', 'code가 비어 있다')
        elif code_bad:
            dims['Implementation'] = ('MISSING', '존재하지 않는 code 경로')
        elif tasks:
            tmap = self._task_status(change)
            if tmap is None:
                dims['Implementation'] = ('PARTIAL', 'tasks.md가 없어 완료 확인 불가')
            else:
                undone = [t for t in tasks if not tmap.get(t)]
                if undone:
                    dims['Implementation'] = ('PARTIAL', '미완료 TASK: %s'
                                              % ', '.join(undone))
                else:
                    dims['Implementation'] = ('PASS', 'TASK 전부 완료 + code 연결')
        else:
            dims['Implementation'] = ('PASS', 'code 연결 (연결된 TASK 없음)')

        # Review (§3: gates.md에서 계산 — convention §2)
        dims['Review'] = self._review_dim(gates, e, change)

        for d in DIM_ORDER:
            dims.setdefault(d, ('MISSING', '계산되지 않음'))
        if any(v == 'MISSING' for v, _ in dims.values()):
            status = 'NOT READY'
        elif any(v == 'PARTIAL' for v, _ in dims.values()):
            status = 'IN PROGRESS'
        else:
            status = 'DONE'
        self.reqs.append((path, rid, dims, status, notes))

    def _review_dim(self, gates, e, change):
        if gates['missing']:
            return ('PARTIAL', 'gates.md가 없어 유효한 기록이 없음 (UNKNOWN)')
        row = gate_current(gates['rows'], 'IMPLEMENTATION_REVIEW_PASS')
        if row is None:
            return ('PARTIAL', '유효한 IMPLEMENTATION_REVIEW_PASS 기록이 없다 '
                               '(UNKNOWN, §3·§5.1)')
        if row.value == 'STALE':
            return ('PARTIAL', '최근 기록이 STALE — 재판정 필요 (§5.3)')
        targets = list(e['code'])
        for tc in e['tests']:
            loc = self.reg.tc_code.get(tc, '')
            if loc and loc != 'MANUAL':
                targets.append(loc)
        targets += plan_files(self.root, change)
        changed = changed_since(self.root, row.commit, targets)
        if changed is None:
            return ('PARTIAL', '근거 커밋 %s 확인 불가 — 재판정 보류 (§5.3)'
                    % (row.commit or '없음'))
        if changed:
            return ('PARTIAL', '근거 커밋 이후 대상 파일 변경 — 재판정 필요 (§5.3): %s'
                    % ', '.join(changed[:5]))
        if row.value == 'FALSE':
            return ('MISSING', '유효한 기록 값이 false (§3)')
        return ('PASS', '유효한 기록 true, 커밋 %s 이후 대상 파일 변경 없음 (§5.3)'
                % row.commit)

    def _task_status(self, change):
        if not change:
            return {}
        text = read_text(self.root, os.path.join('specs', change, 'tasks.md'))
        if text is None:
            return None
        out = {}
        for line in text.splitlines():
            for tid in find_ids(line, {'TASK'}):
                out[tid] = bool(re.search(r'\b(DONE|완료)\b|\[x\]|✅', line,
                                          re.IGNORECASE))
        return out


# ------------------------------------------------------------------ 출력

def analyze(root):
    a = Analyzer(root)
    files = list(_specs_files(root, 'traceability.md'))
    if os.path.isfile(os.path.join(root, 'docs', 'traceability.md')):
        files.append('docs/traceability.md')
    for rel in files:
        a.analyze_traceability(rel)
    if not any(k == 'project' for k in a.gates_seen):
        a._load_gates('docs/gates.md', project=True)
    return a


def report(a):
    out = []
    for info in sorted(a.gates_seen.values(), key=lambda i: i['rel']):
        out.append('== Gate 기록: %s ==' % info['rel'])
        if info['missing']:
            out.append('  파일 없음 — Gate 값은 UNKNOWN이다 (§5.1)')
            continue
        if info['ignored']:
            out.append('  이력 구역 줄 %d개는 현재 값 계산에서 제외 (§5.1)'
                       % info['ignored'])
        for gate in sorted(REVIEWER_USER_GATES | USER_ONLY_GATES):
            row = gate_current(info['rows'], gate)
            if row is None:
                out.append('  %-44s UNKNOWN (유효한 기록 줄 없음)' % gate)
            else:
                out.append('  %-44s %s' % (gate, row.cells[2]))
                out.append('      %s | %s | 근거 커밋 %s'
                           % (row.cells[0], row.judge, row.commit or '없음'))
    for path, rid, dims, status, notes in a.reqs:
        out.append('== %s :: %s ==' % (path, rid))
        for d in DIM_ORDER:
            v, why = dims[d]
            out.append('  %-14s %-8s %s' % (d, v, why))
        out.append('  STATUS: %s' % status)
        for n in notes:
            out.append('  비고: %s' % n)
    if not a.reqs:
        out.append('== traceability ==')
        out.append('  traceability 항목이 없다 — REQ 상태는 계산 대상이 아니다. '
                   '이는 위반이 아니라 이 저장소의 정상 상태다.')
    counts = {}
    for _, _, _, status, _ in a.reqs:
        counts[status] = counts.get(status, 0) + 1
    out.append('== 요약 ==')
    out.append('  REQ 항목 %d건 (DONE %d / IN PROGRESS %d / NOT READY %d), '
               '구조 위반 %d건'
               % (len(a.reqs), counts.get('DONE', 0),
                  counts.get('IN PROGRESS', 0), counts.get('NOT READY', 0),
                  len(a.violations)))
    for path, msg in a.violations:
        out.append('  [위반] %s: %s' % (path, msg))
    return '\n'.join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Traceability Convention §3–§5 계산 (규칙의 단일 출처는 문서다)')
    parser.add_argument('root', nargs='?', default='.',
                        help='저장소 루트 (기본: 현재 디렉터리)')
    parser.add_argument('--self-test', action='store_true',
                        help='내장 픽스처로 §3–§5 계산을 시험한다')
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print('루트 디렉터리가 없다: %s' % root, file=sys.stderr)
        return 2
    a = analyze(root)
    print(report(a))
    return 1 if a.violations else 0


# -------------------------------------------------------------- self-test

def self_test():
    """§3 차원 판정·§4 상태 계산·§5 기록 유효성 사례를 내장 픽스처로 시험한다."""

    def dims_of(a, rid):
        for _, r, dims, status, _ in a.reqs:
            if r == rid:
                return status, {d: v for d, (v, _) in dims.items()}
        return None, {}

    failures = []

    def check(name, cond, detail=''):
        print('[%s] %s%s' % ('PASS' if cond else 'FAIL', name,
                             (' — ' + detail) if (detail and not cond) else ''))
        if not cond:
            failures.append(name)

    # 사례 1: 전 차원 PASS (커밋-핀 재판정 통과) → DONE
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, broken=False)
        a = analyze(tmp)
        status, dims = dims_of(a, 'REQ-001')
        check('정상 케이스 REQ-001 = DONE', status == 'DONE', str(dims))
        for d in DIM_ORDER:
            check('  차원 %s = PASS' % d, dims.get(d) == 'PASS', str(dims))
        check('정상 케이스 구조 위반 0건', not a.violations, str(a.violations))
        info = a.gates_seen.get('project')
        check('프로젝트 gates 부재 시 UNKNOWN 처리',
              info is not None and info['missing'])

    # 사례 2: NOT RUN TC와 STALE 기록 → PARTIAL → IN PROGRESS
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, stale_gate=True)
        a = analyze(tmp)
        status, dims = dims_of(a, 'REQ-002')
        check('NOT RUN TC → Tests PARTIAL', dims.get('Tests') == 'PARTIAL',
              str(dims))
        check('Tests PARTIAL → IN PROGRESS (§4)', status == 'IN PROGRESS')
        status1, dims1 = dims_of(a, 'REQ-001')
        check('STALE 기록 → Review PARTIAL (재판정 필요)',
              dims1.get('Review') == 'PARTIAL', str(dims1))
        check('무효 기록 줄 2건 탐지(AUTHOR 자기 승인·ACCEPTANCE REVIEWER)',
              len(a.violations) >= 2, str(a.violations))

    # 사례 3: dangling 참조와 허용되지 않은 not_applicable → 위반
    with tempfile.TemporaryDirectory() as tmp:
        _fixture(tmp, broken=True)
        a = analyze(tmp)
        msgs = ' | '.join(m for _, m in a.violations)
        check('dangling WF-999 탐지', 'WF-999' in msgs, msgs)
        check('not_applicable 차원 위반 탐지', 'not_applicable은' in msgs, msgs)
        status, dims = dims_of(a, 'REQ-002')
        check('dangling 링크는 연결로 인정하지 않음 → Workflow MISSING',
              dims.get('Workflow') == 'MISSING', str(dims))
        check('위반 포함 시 REQ-002 = NOT READY', status == 'NOT READY')
        check('spec 선언된 REQ-003 항목 없음 → NOT READY',
              any(r == 'REQ-003' for _, r, _, s, _ in a.reqs if s == 'NOT READY'))

    print('== self-test: %s ==' % ('전부 통과' if not failures
                                   else '%d건 실패' % len(failures)))
    return 2 if failures else 0


def _fixture(root, stale_gate=False, broken=False):
    """§3–§5 사례용 최소 저장소를 만든다.

    broken=False: REQ-001은 전 차원 PASS(게이트 유효 줄, 커밋-핀 재판정 통과),
    REQ-002는 TC-004 NOT RUN과 미완료 TASK로 PARTIAL.
    stale_gate=True: 기록 줄에 AUTHOR 자기 승인(무효)·ACCEPTANCE REVIEWER(무효)·
    STALE 맨 아래 줄을 둬 §5.1·§5.2 판정을 시험한다.
    broken=True: dangling WF-999와 not_applicable 위반, spec 선언만 있는 REQ-003을 둔다.
    """
    cid = '001-demo'
    w = lambda rel, s: _write(root, rel, s)
    w('docs/02_requirements.md', '''# 02 Requirements

## 요구사항 목록

| ID | 기능명 | 우선순위 | 상태 |
|---|---|---|---|
| REQ-001 | 로그인 | MUST | DRAFT |
| REQ-002 | 비밀번호 오류 안내 | MUST | DRAFT |
| REQ-003 | 로그아웃 | SHOULD | DRAFT |

## 요구사항 상세 (REQ마다 한 블록)

### REQ-001 로그인

| 항목 | 내용 |
|---|---|
| 예외 상황 | ERR-001 참조 |
| 권한 | PERM-001 참조 |

**완료조건 (Acceptance Criteria)**

| ID | 조건 | 검증 테스트 |
|---|---|---|
| AC-001 | 정상 계정으로 로그인된다 | TC-001 |
| AC-002 | 잘못된 비밀번호는 거부된다 | TC-002 |

### REQ-002 비밀번호 오류 안내

**완료조건 (Acceptance Criteria)**

| ID | 조건 | 검증 테스트 |
|---|---|---|
| AC-003 | 오류 안내가 보인다 | TC-004 |
''')
    w('docs/03_workflow.md', 'WF-001 로그인 흐름\n')
    w('docs/04_screens.md', 'SCR-001 로그인 화면\nAPI-001 POST /login\n')
    w('docs/05_data_model.md', 'DATA-001 사용자\n')
    w('docs/06_permissions.md', '''# 06 Permissions

## 검사 위치

| PERM | UI 처리 | 서버/API 검사 위치 |
|---|---|---|
| PERM-001 | 비활성 | API-001 (auth 모듈) |

## 필수 권한 테스트

| PERM | 정상 역할 | 권한 없음 |
|---|---|---|
| PERM-001 | TC-001 | TC-002 |
''')
    w('docs/08_error_cases.md', 'ERR-001 비밀번호 불일치\n')
    tc3 = 'FAIL' if broken else 'PASS'
    w('docs/09_test_cases.md', '''# 09 Test Cases

## 케이스 목록

| ID | 종류 | 대상 (AC / ERR / PERM) | 절차 | 기대 결과 | 테스트 코드 위치 | 결과 |
|---|---|---|---|---|---|---|
| TC-001 | 정상 | AC-001 | 입력 후 저장 | 로그인 됨 | tests/test_login.py | PASS |
| TC-002 | 예외 | AC-002 | 틀린 비밀번호 | 거부 | tests/test_login.py | PASS |
| TC-003 | 예외 | ERR-001 | 틀린 비밀번호 | 오류 표시 | tests/test_login.py | %s |
| TC-004 | 정상 | AC-003 | 오류 유도 | 안내 표시 | tests/test_login.py | NOT RUN |

## 실행 증거 (결과가 PASS 또는 FAIL인 TC마다 한 줄)

| TC | 결과 | 실행 일시 | 실행한 명령/절차 | 실행 시점 커밋 | 증거 경로 | 실행자 |
|---|---|---|---|---|---|---|
| TC-001 | PASS | 2026-10-09 10:00 | pytest tests/test_login.py | aaa0000 | evidence/tc1.log | tester |
| TC-002 | PASS | 2026-10-09 10:00 | pytest tests/test_login.py | aaa0000 | evidence/tc2.log | tester |
| TC-003 | %s | 2026-10-09 10:00 | pytest tests/test_login.py | aaa0000 | evidence/tc3.log | tester |
''' % (tc3, tc3))
    w('specs/%s/spec.md' % cid,
      '변경 범위 REQ: REQ-001, REQ-002%s\n' % (', REQ-003' if broken else ''))
    w('specs/%s/tasks.md' % cid,
      '| TASK-001 | 로그인 구현 | DONE |\n| TASK-002 | 안내 문구 | 진행 중 |\n')
    w('specs/%s/plan.md' % cid, '변경할 파일: src/auth.py, tests/test_login.py\n')
    na_inline = ('    not_applicable: {screen_api: "화면 변경 없음", '
                 'data: "데이터 변경 없음", permission: "PERM-001 검사 변경 없음", '
                 'error_cases: "ERR-001 처리 변경 없음"}\n')
    if broken:
        na_block = '    not_applicable:\n      tests: "사유 테스트"\n'
        wf2 = 'WF-999'
    else:
        na_block = ('    not_applicable:\n'
                    '      screen_api: "화면 변경 없음"\n'
                    '      data: "데이터 변경 없음"\n'
                    '      permission: "PERM-001 검사 변경 없음"\n'
                    '      error_cases: "ERR-001 처리 변경 없음"\n')
        wf2 = 'WF-001'
    w('specs/%s/traceability.md' % cid, '''# Traceability

```yaml
- id: REQ-001
  workflow:       [WF-001]
  screen_api:     [SCR-001, API-001]
  data:           [DATA-001]
  permission:     [PERM-001]
  error_cases:    [ERR-001]
  acceptance:
    AC-001: [TC-001]
    AC-002: [TC-002]
  tests:          [TC-001, TC-002, TC-003]
  tasks:          [TASK-001]
  code:           [src/auth.py]
  not_applicable: {}
```

```yaml
- id: REQ-002
  workflow:       [%s]
  screen_api:     []
  data:           []
  permission:     []
  error_cases:    []
  acceptance:
    AC-003: [TC-004]
  tests:          [TC-004]
  tasks:          [TASK-002]
  code:           [src/auth.py]
%s
```
''' % (wf2, na_inline if not broken and not stale_gate else na_block))
    w('specs/%s/review.md' % cid, '독립 리뷰 결과 예시\n')
    w('src/auth.py', '# implementation\n')
    w('tests/test_login.py', '# tests\n')
    _git_commit_all(root)
    commit = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip()
    if stale_gate:
        gate_rows = ('| 2026-10-08 | IMPLEMENTATION_REVIEW_PASS | true | '
                     'AUTHOR 본인 | 커밋 `bbb0000` 자기 승인 (무효) |\n'
                     '| 2026-10-09 | ACCEPTANCE | true | REVIEWER 리뷰어 | '
                     '커밋 `%s` 리뷰어 승인 (무효: USER만 가능) |\n'
                     '| 2026-10-09 | IMPLEMENTATION_REVIEW_PASS | STALE | '
                     'REVIEWER reviewer-1 | 커밋 `%s` 이후 변경 발생 |\n'
                     % (commit[:7], commit[:7]))
    else:
        gate_rows = ('| 2026-10-09 | IMPLEMENTATION_REVIEW_PASS | true | '
                     'REVIEWER reviewer-1 | 커밋 `%s` 리뷰 결과 specs/%s/review.md |\n'
                     % (commit[:7], cid))
    w('specs/%s/gates.md' % cid, '''# gates (change)

## 이력 (구 형식 8칸 — 현재 값 계산에서 제외된다)

| 일시 | Gate | 값 | 판정자 유형 | 판정자 | 판정 기준 | 근거 | 비고 |
|---|---|---|---|---|---|---|---|
| 2026-10-01 | IMPLEMENTATION_REVIEW_PASS | true | INDEPENDENT_REVIEWER | 옛 리뷰어 | 구 기준 | `aaa0000` | 이력 |

## 기록

| 일시 | Gate | 값 | 판정자 | 근거 |
|---|---|---|---|---|
%s''' % gate_rows)
    _git_commit_all(root)


def _write(root, rel, content):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)


def _git_commit_all(root):
    subprocess.run(['git', 'init', '-q'], cwd=root, check=False,
                   capture_output=True)
    subprocess.run(['git', '-C', root, 'config', 'user.email', 't@example.com'],
                   check=False, capture_output=True)
    subprocess.run(['git', '-C', root, 'config', 'user.name', 'tester'],
                   check=False, capture_output=True)
    subprocess.run(['git', '-C', root, 'add', '-A'], check=False,
                   capture_output=True)
    subprocess.run(['git', '-C', root, 'commit', '-qm', 'fixture'],
                   check=False, capture_output=True)


if __name__ == '__main__':
    sys.exit(main())
