"""Reconcile two published growth endpoints from the same salmon thesis cohort."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'data/sources/ignatz2019_thesis.pdf'
URL='https://memorial.scholaris.ca/bitstreams/a668d444-72ba-4897-91b9-d8b38ac6257d/download'

def replay():
 raw=PDF.read_bytes()
 if not raw.startswith(b'%PDF-'): raise ValueError('Archived thesis is not PDF')
 text=subprocess.check_output(['pdftotext','-layout',str(PDF),'-'],text=True)
 p=re.search(r'Fish reached an average weight of 1500 g in 382 days at 16\.5°C, followed by 418 and\s+475 days for fish reared at 13\.5°C and 10\.5°C, respectively\.',text)
 if not p:raise ValueError('Published grow-out passage not found')
 # Table 2-2 row order is 10.5, 13.5, 16.5 C; strip superscript group letters.
 table=text[text.rindex('Table 2-2. Thermal-unit growth coefficient'):text.index('2.4.2 Whole body & fillet composition',text.rindex('Table 2-2. Thermal-unit growth coefficient'))]
 # isolate table sections rather than match later 1500 rows when searching 800.
 start800=re.search(r'(?m)^\s*800 g\s*$',table).start()
 start1500=re.search(r'(?m)^\s*1500 g\s*$',table).start()
 eight=table[start800:start1500]
 fifteen=table[start1500:]
 def row(block,label):
  m=re.search(r'^\s*'+label+r'\s+(\d+\.\d+)\w*\s+(\d+\.\d+)\s+(\d+\.\d+)\w*\s+(\d+\.\d+)\s+(\d+\.\d+)\w*\s+(\d+\.\d+)',block,re.M)
  if not m:raise ValueError('Missing '+label)
  n=[float(x) for x in m.groups()]
  return {'means_10_5_13_5_16_5':n[::2],'sems_10_5_13_5_16_5':n[1::2]}
 a={'days_to_1500_g':{'10.5C':475,'13.5C':418,'16.5C':382}, 'TGC_500_to_800_g':row(eight,'TGC'), 'FCR_500_to_800_g':row(eight,'FCR'), 'TGC_800_to_1500_g':row(fifteen,'TGC'), 'FCR_800_to_1500_g':row(fifteen,'FCR')}
 assert a['TGC_800_to_1500_g']['means_10_5_13_5_16_5']==[2.09,1.86,1.43]
 assert a['FCR_800_to_1500_g']['means_10_5_13_5_16_5']==[.86,.87,1.01]
 return {'source':URL,'source_sha256':hashlib.sha256(raw).hexdigest(),'source_passage':p.group(),'source_table':'Table 2-2, thesis pages 48–49; downloaded PDF pages differ from thesis pagination','published_values':a,'descriptive_contrast':{'days_16_5_minus_10_5':382-475,'TGC_late_16_5_minus_10_5':1.43-2.09,'FCR_late_16_5_minus_10_5':1.01-.86},'interpretation':'Within the same underlying temperature cohort, the warmest group reaches 1500g sooner but has lower late-interval thermal-unit growth coefficient and higher late-interval feed conversion ratio than the coolest group; endpoint choice changes the ranking.','limits':['This result is in the original thesis and is not newly discovered or independent validation of the 2022 transcript study, whose authors cite the related growth experiment.','Time-to-weight, temperature-normalized interval growth and feed efficiency answer different questions; no single best temperature follows without an explicit objective and life stage.','The thesis gives aggregate means and SEM, not individual fish-level repeated trajectories in this audit; no independent model fit, causal inference, comparator win or product safety claim.'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}

if __name__=='__main__':print(json.dumps(replay(),sort_keys=True,indent=2))
