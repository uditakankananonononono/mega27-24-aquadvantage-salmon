import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_color_matches_reported_concordance_not_literal_cutoff():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/reconcile_author_highlights.py')],text=True))
 assert actual==json.loads((R/'results/reconcile_author_highlights.json').read_text())
 assert [actual['tables'][i]['green_concordant'] for i in ['S1','S2','S3']]==[1750,172,52]
 assert [actual['tables'][i]['green_rows_not_matching_literal_both_q_and_FC'] for i in ['S1','S2','S3']]==[17,1,1]
