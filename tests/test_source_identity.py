import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_published_runs_match_ena_without_dataset_inflation():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/check_source_identity.py')],text=True))
 expected=json.loads((R/'results/source_identity.json').read_text())
 assert actual==expected
 assert actual['article_run_count']==18 and actual['published_runs_match_ena']
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
