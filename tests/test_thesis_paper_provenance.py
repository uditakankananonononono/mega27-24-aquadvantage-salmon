from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_thesis_paper_provenance():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_thesis_paper_provenance.py')],text=True))
 assert x==json.loads((ROOT/'results/thesis_paper_provenance.json').read_text())
 assert x['article_marker_checks']['same_fish_fillets']
 assert x['article_marker_checks']['same_overarching_experiment']
