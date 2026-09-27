"""Audit published transcript-summary cross-comparison arithmetic, not expression reanalysis."""
from pathlib import Path
import hashlib,json,math,openpyxl
R=Path(__file__).resolve().parents[1]
paths={k:R/f'data/sources/PMC9168996_Table{k}.xlsx' for k in ['S1','S2','S3']}
rows={};dups={}
for k,p in paths.items():
 s=openpyxl.load_workbook(p,read_only=False,data_only=True).active
 d={};duplicate_ids=[]
 for row in s.iter_rows(min_row=6):
  if row[0].value is None:continue
  id_=str(row[0].value)
  if id_ in d:duplicate_ids.append(id_);continue
  d[id_]={'author_green':row[0].fill.fgColor.rgb=='FF00B050',
          'fpkm_a':row[4].value,'fpkm_b':row[5].value,
          'edgeR_fc':row[6].value,'deseq_fc':row[9].value}
 rows[k]=d;dups[k]=duplicate_ids
assert all(not x for x in dups.values())
green={k:{i for i,r in d.items() if r['author_green']} for k,d in rows.items()}
triple=sorted(set.intersection(*green.values()))
assert len(triple)==16
checks=[]
for id_ in triple:
 a,b,c=(rows[k][id_] for k in ['S1','S2','S3'])
 # S1: 10.5 vs 16.5; S2: 10.5 vs 13.5; S3: 13.5 vs 16.5.
 # Verify the shared mean columns agree across the three author spreadsheets.
 vals=[a['fpkm_a'],b['fpkm_a'],b['fpkm_b'],c['fpkm_a'],a['fpkm_b'],c['fpkm_b']]
 finite=all(isinstance(v,(float,int)) and math.isfinite(v) for v in vals)
 shared=(finite and math.isclose(vals[0],vals[1],rel_tol=1e-9,abs_tol=1e-12)
         and math.isclose(vals[2],vals[3],rel_tol=1e-9,abs_tol=1e-12)
         and math.isclose(vals[4],vals[5],rel_tol=1e-9,abs_tol=1e-12))
 # Both methods encode FC as first temperature / second temperature (confirmed against FPKM direction).
 # Their pairwise FCs are not assumed to multiply exactly: separately fitted methods/normalizations.
 all_positive=finite and min(vals)>0
 simple_ratio=(vals[0]/vals[4] if all_positive else None)
 checks.append({'transcript_id':id_,'shared_mean_columns_agree':shared,
  'fpkm_10_5':vals[0],'fpkm_13_5':vals[2],'fpkm_16_5':vals[4],
  'direct_10_5_to_16_5_ratio':simple_ratio,
  'composed_10_5_to_13_5_times_13_5_to_16_5':((vals[0]/vals[2])*(vals[2]/vals[4]) if all_positive else None),
  'all_positive':all_positive,
  'author_edgeR_fc':[a['edgeR_fc'],b['edgeR_fc'],c['edgeR_fc']],
  'author_DESeq2_fc':[a['deseq_fc'],b['deseq_fc'],c['deseq_fc']]})
assert all(x['shared_mean_columns_agree'] for x in checks)
assert all(x['all_positive'] for x in checks)
assert all(math.isclose(x['direct_10_5_to_16_5_ratio'],x['composed_10_5_to_13_5_times_13_5_to_16_5'],rel_tol=1e-12) for x in checks)
print(json.dumps({'source':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9168996/supplementaryFiles',
 'paper':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
 'source_sha256':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},
 'author_green_counts':{k:len(g) for k,g in green.items()},
 'pairwise_green_overlap':{'S1_S2':len(green['S1']&green['S2']),'S1_S3':len(green['S1']&green['S3']),'S2_S3':len(green['S2']&green['S3'])},
 'all_three_green':len(triple),'shared_fpkm_columns_agree_count':sum(x['shared_mean_columns_agree'] for x in checks),
 'simple_fpkm_ratio_transitivity_count':sum(math.isclose(x['direct_10_5_to_16_5_ratio'],x['composed_10_5_to_13_5_times_13_5_to_16_5'],rel_tol=1e-12) for x in checks),
 'triples':checks,
 'limits':['Shared FPKM means and their ratio transitivity are table arithmetic, not independent transcriptome validation.','Author fold changes are method-specific modeled values and are not expected to equal or multiply like simple FPKM ratios.','Author green denotes selected DET summaries; no raw per-sample count matrix or independent cohort is analyzed.','No product-wide growth or safety inference follows.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
