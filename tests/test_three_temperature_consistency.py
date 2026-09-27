import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_three_temperature_source_consistency_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/three_temperature_consistency.py')],text=True))
 assert actual==json.loads((R/'results/three_temperature_consistency.json').read_text())
 assert actual['all_three_green']==16
 assert actual['shared_fpkm_columns_agree_count']==16
 assert actual['simple_fpkm_ratio_transitivity_count']==16
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
