import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_degree_day_replay():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/replay_thesis_degree_days.py')],text=True))
 assert d==json.loads((R/'results/thesis_degree_day_replay.json').read_text())
 m1=d['checks']['month1_replay']
 assert all(v['within_tolerance_band'] for v in m1.values())
 assert all(45.0<=v['implied_month1_span_days']<=47.0 for v in m1.values())
 term=d['checks']['terminal_replay']
 assert all(v['within_tolerance_band'] for v in term.values())
 assert abs(term['13.5']['residual_cdd'])<1.0
 assert d['checks']['tgc_values_replayable_from_printed_inputs'] is False
 assert all(v==0 for v in d['gate_credit'].values())
