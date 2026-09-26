import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_published_summary_tables_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_supplement_tables.py')],text=True))
 expected=json.loads((R/'results/supplement_tables_audit.json').read_text())
 assert actual==expected
 assert all(v['both_q_below_0.05']<=min(v['edgeR_q_below_0.05'],v['DESeq2_q_below_0.05']) for v in actual['tables'].values())
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
