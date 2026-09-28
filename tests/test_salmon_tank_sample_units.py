import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_tank_units_replay():
    out=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_salmon_tank_sample_units.py')],text=True))
    assert out==json.loads((ROOT/'results/salmon_tank_sample_units.json').read_text())
    assert len(set(out['article_table_1_run_accessions']))==18
    assert out['selected_fraction_per_temperature']==6/21
    assert out['gate_credit']['fetched_and_used_accession_datasets']==0
