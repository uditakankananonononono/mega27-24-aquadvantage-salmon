from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_refseq_label_inventory():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_supplement_refseq_labels.py')],text=True))
 assert x==json.loads((ROOT/'results/supplement_refseq_labels.json').read_text())
 assert x['unique_refseq_label_count']==3436
 assert x['refseq_labels_mapping_multiple_transcript_ids']==614
