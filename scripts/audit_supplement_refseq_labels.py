"""Check printed RefSeq label reuse across selected transcript-summary tables."""
from pathlib import Path
import hashlib,json,openpyxl,collections
R=Path(__file__).resolve().parents[1]
records=[];info={}
for n in ('S1','S2','S3'):
 p=R/f'data/sources/PMC9168996_Table{n}.xlsx'
 sh=openpyxl.load_workbook(p,read_only=True,data_only=True).active
 rows=sh.values
 for _ in range(4):next(rows)
 header=next(rows)
 assert header[2]=='RefSeq mRNA Assession'
 body=[]
 for r in rows:
  if r[0] is None:continue
  body.append((str(r[0]),str(r[2]).strip() if r[2] is not None else ''))
 info[n]={'row_count':len(body),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
          'missing_refseq_labels':sum(not ref for _,ref in body)}
 records.extend((n,transcript,ref) for transcript,ref in body if ref)
refmap=collections.defaultdict(set)
for n,transcript,ref in records:refmap[ref].add(transcript)
shared={ref:sorted(ids) for ref,ids in refmap.items() if len(ids)>1}
reuse=sorted(shared.items(),key=lambda z:(-len(z[1]),z[0]))
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
     'supplement_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9168996/supplementaryFiles',
     'tables':info,'unique_refseq_label_count':len(refmap),
     'refseq_labels_mapping_multiple_transcript_ids':len(shared),
     'max_transcript_ids_per_refseq_label':max(map(len,refmap.values())),
     'top_reused_labels':[{'refseq_label':ref,'transcript_ids':ids[:12],'transcript_count':len(ids)} for ref,ids in reuse[:10]],
     'finding':'These author-processed supplementary tables contain transcript IDs and RefSeq mRNA labels. A RefSeq label can map to multiple transcript IDs in the selected tables, so RefSeq labels are not a one-to-one denominator for counting independent transcript observations.',
     'limits':['Printed labels only; no RefSeq record individually fetched or annotation independently verified',
               'The same transcript can appear across multiple contrast tables and is deduplicated before counting',
               'No expression, genotype, product or biological-discovery inference'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
