"""Locate source passages limiting fillet/transcript 'external validation' claims."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/pmc9168996.xml'
s=BeautifulSoup(p.read_bytes(),'xml')
text=[q.get_text(' ',strip=True) for q in s.find_all('p')]
markers={
 'same_fish':'Fillet samples were collected concurrently during each sampling period from the same fish sampled for liver transcript expression.',
 'figure8_all_fish':'Figure 8A shows the degree of correlation among the expression profiles of all nine target transcripts',
 'figure8_pca':'Principal component analysis (PCA) of the same multivariate dataset',
 'previous_same_experiment':'Previous findings from this experiment have also shown',
}
for k,v in markers.items():assert any(v in paragraph for paragraph in text),k
out={'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'marker_presence':{k:True for k in markers},
     'classification':{'fillet_and_liver_measured_on_same_fish':True,
                       'figure8_correlation_external_test':False,
                       'figure8_pca_independent_cohort':False,
                       'eligible_for_held_out_same_task_validation_from_this_paper_alone':False},
     'finding':'The paper explicitly pairs fillet and liver measurements on the same fish; its Figure 8 correlations and PCA use these within-cohort measurements. They are useful source context but cannot substitute for a held-out independent cohort when evaluating a new predictor.',
     'limits':['Prose-level provenance; no digitization of Figure 8 or reanalysis of individual fish',
               'Within-fish paired measurements can be scientifically informative, but are not external validation',
               'No performance, husbandry, product-safety, biological discovery or gate-credit claim'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
