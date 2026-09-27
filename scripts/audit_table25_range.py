"""Replay printed Table 2-5 row means as a bounded source-context check."""
from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[1]
pdf=root/'data/sources/ignatz2019_thesis.pdf'
txt=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
sec=txt.split('Table 2-5. Nutrient utilization:',2)[-1].split('Table 2-6. Nutrient utilization:',1)[0]
assert 'Period 1 (300 - 500 g)' in sec and 'Period 3 (800 - 1500 g)' in sec
pat=r'^\s*(Protein|Lipid|Ash)( RE \(%\)| \[mg \(°C·d\)-1\])\s+(.+)$'
periods={}
for idx,period in enumerate([1,2,3]):
 s=sec.split(f'Period {period} (',1)[1]
 s=s.split(f'Period {period+1} (',1)[0] if period<3 else s
 rows={}
 for line in s.splitlines():
  m=re.match(pat,line)
  if not m:continue
  key=m.group(1)+(' RE' if 'RE' in m.group(2) else ' deposition')
  nums=re.findall(r'(?<!\w)(\d+\.\d+)(?:[A-Za-z]+)?',m.group(3))
  assert len(nums)==6,(period,key,line,nums)
  rows[key]=[float(v) for v in nums[::2]]
 assert len(rows)==6,(period,rows)
 periods[str(period)]=rows
re_above=[{'period':p,'nutrient':n,'temp_C':t,'printed_re_pct':v} for p,rows in periods.items() for n in ('Protein','Lipid','Ash') for t,v in zip((10.5,13.5,16.5),rows[n+' RE']) if v>100]
trends={n:{str(t):[periods[str(p)][n+' deposition'][i] for p in (1,2,3)] for i,t in enumerate((10.5,13.5,16.5))} for n in ('Protein','Lipid','Ash')}
out={'source_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
 'source_file':pdf.name,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
 'printed_thesis_pages':'59-60','table_2_5_means':periods,
 'checks':{'row_count':sum(map(len,periods.values())),'mean_cell_count':54,
           'retention_efficiencies_above_100':re_above,
           'deposition_by_growth_period':trends,
           'protein_and_lipid_deposition_increase_at_each_temperature':all(all(a<b for a,b in zip(vals,vals[1:])) for n in ('Protein','Lipid') for vals in trends[n].values())},
 'limits':['Printed treatment means only; no tank-level replicates or feed nutrient intake recovered, so retention efficiencies cannot be independently recomputed.',
           'The Table 2-5 caption reports n=3 and significance letters; no statistical reanalysis is made.',
           'The printed above-100% lipid retention for period 1 at two temperatures is flagged as reported, not declared impossible or a defect; composition and intake denominators may differ.',
           'No growth, feed, husbandry or nutritional recommendation follows from this descriptive table replay.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
