from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_decision_certificate():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/multiendpoint_decision_certificate.py')],text=True))
 assert x==json.loads((R/'results/multiendpoint_decision_certificate.json').read_text())
 assert x['pareto_nondominated']==['10.5C','13.5C','16.5C']
 assert sum(x['winner_set_counts'].values())==5151
 assert x['calendar_only_winner']=='16.5C'
 assert x['gate_credit']['audited_derivations']==0
