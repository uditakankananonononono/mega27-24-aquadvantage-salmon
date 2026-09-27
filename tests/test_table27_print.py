from pathlib import Path
import json, subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_table27_print():
    a=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_table27_print.py')],text=True))
    assert a==json.loads((ROOT/'results/table27_print.json').read_text())
    assert a['fillet_yield_absolute_percentage_points']=={'10.5':7.16,'13.5':4.48}
    assert a['fillet_yield_relative_to_16_5_pct']=={'10.5':13.74,'13.5':8.6}
