import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_replay_table26():
    actual = json.loads(subprocess.check_output(['python3', str(ROOT / 'scripts/audit_table26_range.py')], text=True))
    assert actual == json.loads((ROOT / 'results/table26_range.json').read_text())
    assert actual['checks']['row_count'] == 32
    assert actual['checks']['mean_cell_count'] == 96
