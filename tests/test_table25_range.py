import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_replay_table25():
 actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_table25_range.py')],text=True))
 assert actual==json.loads((ROOT/'results/table25_range.json').read_text())
 assert actual['checks']['row_count']==18
 assert actual['checks']['mean_cell_count']==54
 assert len(actual['checks']['retention_efficiencies_above_100'])==2
 assert actual['checks']['protein_and_lipid_deposition_increase_at_each_temperature']
