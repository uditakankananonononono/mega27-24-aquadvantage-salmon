import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_source_thesis_replays_opposed_rankings():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_temperature_endpoint_reversal.py')],text=True))
 assert actual==json.loads((ROOT/'results/temperature_endpoint_reversal.json').read_text())
 c=actual['descriptive_contrast']
 assert c['days_16_5_minus_10_5']==-93
 assert c['TGC_late_16_5_minus_10_5']<0
 assert c['FCR_late_16_5_minus_10_5']>0
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
