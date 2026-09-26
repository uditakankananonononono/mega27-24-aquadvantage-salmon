"""Reconcile the paper's concordant DET totals to original spreadsheet formatting."""
from pathlib import Path
from collections import Counter
import hashlib,json,openpyxl
R=Path(__file__).resolve().parents[1]
result={'paper':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
 'supplement':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9168996/supplementaryFiles',
 'paper_reported_concordant_det':{'S1':1750,'S2':172,'S3':52},'tables':{},
 'limits':['Author green spreadsheet formatting exactly encodes the article’s concordant list; it is not independent reanalysis','Exact reciprocal lower cutoff 1/1.5 reproduces author green fills across these source tables; this does not prove the authors applied that exact code or clarify why printed legend says <=0.66','Spreadsheets contain selected summary DETs, not full per-sample counts; no out-of-study benchmark or independent biological discovery'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
for k in ['S1','S2','S3']:
 p=R/f'data/sources/PMC9168996_Table{k}.xlsx'
 s=openpyxl.load_workbook(p,read_only=False,data_only=True).active
 counts=Counter(); nonliteral=0; reciprocal_disagreements=0; reciprocal_pass=0
 for row in s.iter_rows(min_row=6):
  if row[0].value is None:continue
  color=row[0].fill.fgColor.rgb
  counts[color]+=1
  q1,q2,fc1,fc2=[row[i].value for i in [8,11,6,9]]
  if color=='FF00B050' and not (all(isinstance(q,(float,int)) and q<.05 for q in [q1,q2]) and all(isinstance(fc,(float,int)) and (fc<=.66 or fc>=1.5) for fc in [fc1,fc2])): nonliteral+=1
  meets_reciprocal=(all(isinstance(q,(float,int)) and q<.05 for q in [q1,q2]) and all(isinstance(fc,(float,int)) and (fc<=1/1.5 or fc>=1.5) for fc in [fc1,fc2]))
  reciprocal_pass+=meets_reciprocal
  reciprocal_disagreements+=(meets_reciprocal!=(color=='FF00B050'))
 assert counts['FF00B050']==result['paper_reported_concordant_det'][k]
 assert reciprocal_disagreements==0 and reciprocal_pass==counts['FF00B050']
 result['tables'][k]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
  'green_concordant':counts['FF00B050'],'yellow_only_DESeq2':counts['FFFFFF00'],
  'red_only_edgeR':counts['FFFF0000'],'green_rows_not_matching_literal_both_q_and_FC':nonliteral,'exact_reciprocal_1_5_lower_bound_matches_green_rows':reciprocal_pass,'exact_reciprocal_1_5_rule_disagreements':reciprocal_disagreements}
print(json.dumps(result,indent=2,sort_keys=True))
