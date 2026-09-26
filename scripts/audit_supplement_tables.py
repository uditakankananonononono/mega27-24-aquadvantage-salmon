"""Audit published differential-expression summary tables, no sequence-level analysis."""
import hashlib,json
from pathlib import Path
import openpyxl
R=Path(__file__).resolve().parents[1]
result={'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
 'supplement_archive':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9168996/supplementaryFiles',
 'tables':{},'limits':['Tables are already processed differential-expression results, not sample-level count matrix','Cannot re-estimate uncertainty or reproduce edgeR/DESeq2 from these summary files','All temperatures derive from one cohort; no independent validation or fair new benchmark','Do not infer product-level growth/environmental safety or biological design'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
for name,contrast in [('S1','10.5 vs 16.5 C'),('S2','10.5 vs 13.5 C'),('S3','13.5 vs 16.5 C')]:
 p=R/f'data/sources/PMC9168996_Table{name}.xlsx'
 sheet=openpyxl.load_workbook(p,read_only=True,data_only=True).active
 records=list(sheet.values)
 header=[str(x) if x is not None else '' for x in records[4]]
 assert header[0]=='Transcript ID' and 'edgeR: q-value' in header and 'DESeq2: q-value' in header
 body=[r for r in records[5:] if r[0] is not None]
 ids=[str(x[0]) for x in body]
 assert len(ids)==len(set(ids))
 qi=header.index('edgeR: q-value'); qj=header.index('DESeq2: q-value')
 er=sum(isinstance(r[qi],(int,float)) and r[qi]<.05 for r in body)
 ds=sum(isinstance(r[qj],(int,float)) and r[qj]<.05 for r in body)
 fi=header.index('edgeR: FC'); fj=header.index('DESeq2: FC')
 both=sum(isinstance(r[qi],(int,float)) and r[qi]<.05 and isinstance(r[qj],(int,float)) and r[qj]<.05 for r in body)
 both_with_fc=sum(isinstance(r[qi],(int,float)) and r[qi]<.05 and isinstance(r[qj],(int,float)) and r[qj]<.05 and all(isinstance(r[k],(int,float)) and (r[k]>=1.5 or r[k]<=.66) for k in (fi,fj)) for r in body)
 result['tables'][name]={'contrast':contrast,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
  'data_rows':len(body),'unique_transcript_ids':len(ids),'edgeR_q_below_0.05':er,
  'DESeq2_q_below_0.05':ds,'both_q_below_0.05':both,'both_q_and_fold_change':both_with_fc,'columns_without_sequence':header[:-1]}
print(json.dumps(result,indent=2,sort_keys=True))
