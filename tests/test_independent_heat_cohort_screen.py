import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_primary_source_screen_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/screen_independent_heat_cohort.py')],text=True))
 assert actual==json.loads((ROOT/'results/independent_heat_cohort_screen.json').read_text())
 assert actual['eligibility']['independent_population']
 assert not actual['eligibility']['eligible_as_held_out_same_task_cohort']
 assert not actual['eligibility']['per_sample_quantitative_expression_comparable']
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
