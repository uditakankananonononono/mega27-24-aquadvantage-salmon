from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
def test_related_salmon_cohort_scope():
    result=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_related_salmon_cohort_scope.py')],text=True))
    assert result==json.loads((R/'results/related_salmon_cohort_scope.json').read_text())
    assert [x['independent_same_task_validation'] for x in result['candidate_classifications']]==[False,False]
    assert result['gate_credit']['fetched_and_used_accession_datasets']==0
