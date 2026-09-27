import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_inventory_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_read_inventory.py')],text=True))
 assert actual==json.loads((R/'results/read_inventory.json').read_text())
 assert actual['runs']==actual['unique_samples']==actual['exact_article_twice_ena_match_count']==18
 assert actual['total_article_raw_reads']==2*actual['total_ena_read_count']
 assert all(r['article_matches_two_times_ena_read_count'] for r in actual['rows'])
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
