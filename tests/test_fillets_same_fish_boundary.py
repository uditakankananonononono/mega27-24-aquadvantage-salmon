import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_same_fish_boundary():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_fillets_same_fish_boundary.py')],text=True))
 assert x==json.loads((ROOT/'results/fillets_same_fish_boundary.json').read_text())
 assert x['classification']['fillet_and_liver_measured_on_same_fish']
 assert not x['classification']['figure8_correlation_external_test']
