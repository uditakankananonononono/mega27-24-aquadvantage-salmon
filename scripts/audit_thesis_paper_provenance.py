"""Audit whether thesis and cited article are independent source cohorts."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1]
a=R/'data/sources/pmc9168996.xml';p=R/'data/sources/ignatz2019_thesis.pdf'
s=BeautifulSoup(a.read_bytes(),'xml')
paragraphs=[x.get_text(' ',strip=True) for x in s.find_all('p')]
markers={
 'same_fish_fillets':'Fillet samples were collected concurrently during each sampling period from the same fish sampled for liver transcript expression.',
 'related_growth_work':'Ignatz et al. (2020b)',
 'same_overarching_experiment':'same overarching experiment as the current study',
 'distinct_cohort_claim':'a distinct independent validation cohort',
}
found={k:any(v in para for para in paragraphs) for k,v in markers.items()}
assert found['same_fish_fillets'] and found['related_growth_work'] and found['same_overarching_experiment'] and not found['distinct_cohort_claim']
ref=next(r.get_text(' ',strip=True) for r in s.find_all('ref') if '10.1016/j.aquaculture.2019.734896' in r.get_text(' ',strip=True))
assert 'Ignatz' in ref and '2020b' in ref
pdfinfo=subprocess.check_output(['pdfinfo',str(p)],text=True)
out={'article_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
     'thesis_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
     '2020b_doi':'10.1016/j.aquaculture.2019.734896',
     'article_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),
     'thesis_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'article_marker_checks':found,'cited_reference':ref,
     'finding':'The transcriptomics paper explicitly says fillet composition came from the same fish used for liver expression and cites the 2020b growth/composition report. It also describes another immune-response subset as drawn from the same overarching experiment. Thus thesis/growth/composition and transcriptomics measures are related rather than independent held-out cohorts.',
     'limits':['Citation/prose-level provenance audit only; participant-level crosswalk is not present in the article',
               'The thesis includes many endpoints across growth stages and cannot be reduced to the same 18 expression libraries',
               'No independent biological replication, model benchmark, causal or husbandry claim follows'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
