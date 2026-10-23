"""Independently verify this fan comparison from original MCP CSV, not UI ID lists.

Run: python3 docs/research/verify_fan_comparison.py
Original downloaded CSV is supplied by --source; outputs go under ignored reports/.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path('/private/tmp/atp-discovery-external/charting-m-points-2020s.csv'))
parser.add_argument('--out', type=Path, default=Path('reports/discovery/fan-evidence/source-audit.json'))
args = parser.parse_args()
key = '20230910-M-US_Open-F-Novak_Djokovic-Daniil_Medvedev'
with args.source.open(encoding='utf-8-sig', newline='') as handle:
    match = [row for row in csv.DictReader(handle) if row['match_id'] == key]
assert len(match) == 215
assert [int(r['Pt']) for r in match] == list(range(1, 216))
records = [r for r in match if r['Set1'] == '1' and r['Set2'] == '0']
frozen_path = Path('gui/margins-experiment/tactical-demo/source-points.json')
frozen = json.loads(frozen_path.read_text())
assert records == frozen
assert len(records) == 110
assert hashlib.sha256(frozen_path.read_bytes()).hexdigest() == 'eb6f8cf0b7c3766f92f70424d9ec870a79a325e06360b4cba67b5444e62b1b5e'

# Tokenize character by character, unlike the frontend regular expression.
stroke_letters = set('fbrsvzopuylmhijktq')
annotated = []
for row in records:
    assert all(row[field] for field in ['Pt', 'Set1', 'Set2', 'Gm1', 'Gm2', 'Pts', 'Svr', 'PtWinner', '1st'])
    assert row['Svr'] in ('1', '2') and row['PtWinner'] in ('1', '2')
    code = (row['2nd'] or row['1st']).lstrip('c')
    assert code[0] in '456'
    tokens = []
    for char in code:
        if char in stroke_letters:
            tokens.append(char)
        elif tokens:
            tokens[-1] += char
    server = int(row['Svr'])
    shots = [(3-server if i % 2 == 0 else server, token) for i, token in enumerate(tokens)]
    own_drops = [(i, token) for i, (actor, token) in enumerate(shots) if actor == 1 and token[0] in 'uy']
    sv = server == 1 and code[1:2] == '+'
    assert not (sv and own_drops)
    prior = any(actor == 2 and token[0] in 'uy' for actor, token in shots[:own_drops[0][0]]) if own_drops else False
    annotated.append({'id': int(row['Pt']), 'server': server, 'winner': int(row['PtWinner']), 'kind': 'sv' if sv else 'drop' if own_drops else 'other', 'drop_tokens': [t for _, t in own_drops], 'counter_drop': prior})

cohorts = {}
for scope in ['all', 'serve']:
    selected = [r for r in annotated if scope == 'all' or r['server'] == 1]
    cohorts[scope] = {}
    for kind in ['sv', 'drop', 'other']:
        group = [r for r in selected if r['kind'] == kind]
        cohorts[scope][kind] = {'ids': [r['id'] for r in group], 'n': len(group), 'won': sum(r['winner'] == 1 for r in group)}
    assert sum(g['n'] for g in cohorts[scope].values()) == (110 if scope == 'all' else 52)
assert [(cohorts[s][k]['won'], cohorts[s][k]['n']) for s in ['all', 'serve'] for k in ['sv', 'drop', 'other']] == [(11, 11), (3, 11), (44, 88), (11, 11), (1, 5), (25, 36)]
wins = [r for r in annotated if r['server'] == 1 and r['kind'] == 'drop' and r['winner'] == 1]
assert len(wins) == 1 and wins[0]['id'] == 84 and wins[0]['counter_drop'] and wins[0]['drop_tokens'] == ['u-37']
# A let's approach and a faulted first-serve approach must not leak into classification.
assert next(r for r in annotated if r['id'] == 121)['kind'] == 'drop'
assert next(r for r in annotated if r['id'] == 145)['kind'] == 'other'
result = {'match_id': key, 'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(), 'all_fields_match': True, 'cohorts': cohorts, 'points': annotated, 'missingness': {k: sum(not r[k] for r in records) for k in records[0]}, 'limits': 'Second set selected for the existing story, not randomly sampled. No timestamps or measured coordinates. Approach code is optional. Empty second serve means no second serve recorded; empty Notes means no annotation. No causal treatment comparison.'}
args.out.parent.mkdir(parents=True, exist_ok=True)
args.out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'cohorts': cohorts, 'missingness': result['missingness']}, indent=2))
