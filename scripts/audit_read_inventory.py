"""Reconcile publication Table 1 read counts with ENA metadata, without downloading reads."""
import csv,hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
xml=R/'data/sources/pmc9168996.xml'; tsv=R/'data/sources/PRJNA766994_ena_payload_inventory.tsv'
soup=BeautifulSoup(xml.read_text(),'xml')
table=soup.find('table-wrap',id='T1')
assert table
published={}
for tr in table.find_all('tr'):
 cells=[x.get_text(' ',strip=True) for x in tr.find_all(['td','th'],recursive=False)]
 acc=next((c for c in cells if re.fullmatch(r'SRR\d+',c)),None)
 if not acc:continue
 index=cells.index(acc)
 count=int(cells[index+1].replace(',',''))
 published[acc]=count
records=list(csv.DictReader(tsv.open(newline=''),delimiter='\t'))
assert len(records)==18 and len(published)==18
assert len({r['run_accession'] for r in records})==18
rows=[]
for r in records:
 acc=r['run_accession'];paired=r['library_layout']=='PAIRED'
 bytes_=list(map(int,r['fastq_bytes'].split(';')))
 n=int(r['read_count']);bases=int(r['base_count'])
 rows.append({'run_accession':acc,'sample_accession':r['sample_accession'],
  'article_raw_reads':published[acc],'ena_read_count':n,'ena_base_count':bases,
  'paired':paired,'fastq_file_count':len(bytes_),'fastq_total_bytes':sum(bytes_),
  'article_matches_two_times_ena_read_count':published[acc]==2*n})
assert all(r['paired'] and r['fastq_file_count']==2 for r in rows)
print(json.dumps({'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
 'ena_report':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA766994&result=read_run&fields=run_accession%2Csample_accession%2Cread_count%2Cbase_count%2Cfastq_bytes%2Clibrary_layout&format=tsv',
 'source_sha256':{'article_xml':hashlib.sha256(xml.read_bytes()).hexdigest(),'ena_tsv':hashlib.sha256(tsv.read_bytes()).hexdigest()},
 'runs':len(rows),'unique_samples':len({r['sample_accession'] for r in rows}),
 'exact_article_twice_ena_match_count':sum(r['article_matches_two_times_ena_read_count'] for r in rows),
 'total_article_raw_reads':sum(r['article_raw_reads'] for r in rows),
 'total_ena_read_count':sum(r['ena_read_count'] for r in rows),
 'total_ena_base_count':sum(r['ena_base_count'] for r in rows),
 'total_fastq_bytes':sum(r['fastq_total_bytes'] for r in rows),
 'rows':rows,'limits':['ENA read_count is paired fragments; Table 1 counts individual reads/mates. Matching counts is metadata reconciliation, not raw-read analysis.','FASTQ payloads not downloaded or analyzed; no per-sample transcript abundance matrix or independent cohort obtained.','Single experimental cohort; no product-level growth or environmental conclusion.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
