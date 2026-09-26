"""Verify published triploid-salmon RNA-seq run metadata; no sequence or phenotype analysis."""
from pathlib import Path
import csv, hashlib, json
from xml.etree import ElementTree as ET
R=Path(__file__).resolve().parents[1]
article=R/'data/sources/pmc9168996.xml'
published=R/'data/sources/published_sra_runs.tsv'
ena=R/'data/sources/PRJNA766994_ena_runs.tsv'
with published.open() as f: p=[x['run_accession'] for x in csv.DictReader(f,delimiter='\t')]
with ena.open() as f: e=list(csv.DictReader(f,delimiter='\t'))
r=ET.parse(article).getroot()
t=next(t for t in r.findall('.//table-wrap') if 'Trimming and alignment metrics' in ''.join(t.itertext()))
assert all(run in ' '.join(t.itertext()) for run in p)
assert len(p)==18 and len(set(p))==18
assert len(e)==18 and len({row['run_accession'] for row in e})==18
assert set(p)=={row['run_accession'] for row in e}
assert {row['study_accession'] for row in e}=={'PRJNA766994'}
result={'source_article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
 'ena_report':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA766994&result=read_run&fields=run_accession%2Cexperiment_accession%2Csample_accession%2Cstudy_accession&format=tsv',
 'sha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (article,published,ena)},
 'study':'PRJNA766994','article_run_count':len(p),'ena_run_count':len(e),'published_runs_match_ena':set(p)=={row['run_accession'] for row in e},
 'runs':sorted(e,key=lambda x:x['run_accession']),
 'limits':['One study, not 18 independent experimental studies','Only run metadata and publication fetched, not sequencing payloads or raw phenotypes','Do not infer fitness, growth advantage, environmental safety or genomic engineering directions from this screen'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
