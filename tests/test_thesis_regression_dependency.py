from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_symbolic_regression_dependency():
    actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_thesis_regression_dependency.py')],text=True))
    assert actual==json.loads((ROOT/'results/thesis_regression_dependency.json').read_text())
    assert actual['literal_point_estimate_substitution']['BW_coefficient']==0.00224
    assert actual['literal_point_estimate_substitution']['PL_coefficient']==-0.04332
