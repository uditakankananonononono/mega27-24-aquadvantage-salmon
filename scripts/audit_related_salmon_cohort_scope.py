"""Classify tempting published salmon expression comparators by cohort and assay."""
from pathlib import Path
from lxml import etree
import json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/related_salmon_pubmed_24145116_31891812.medline.txt'
s=p.read_text()
assert 'PMID- 24145116' in s and 'PMID- 31891812' in s
assert '32K cDNA microarray' in s and 'juvenile growth rate was evaluated over a 45-day period' in s
assert 'families (AS11, AS26) and a slow-growing 3NGHTg' in s
assert 'kidney samples were collected before injection and 6, 24 and 48 h' in s
assert '10.5  degrees C, 13.5  degrees C, 16.5  degrees C' in s
root=etree.parse(str(R/'data/sources/pmc9168996.xml'))
text=[' '.join(q.itertext()) for q in root.xpath('//p')]
passage=next(x for x in text if 'In a subset of fish also assessed at 800' in x)
assert 'same overarching experiment as the current study' in passage
assert 'rsad2' in passage and '24' in passage
out={'pubmed_efetch_url':'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=24145116,31891812&rettype=medline&retmode=text',
     'medline_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'target_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
     'target_xml_sha256':hashlib.sha256((R/'data/sources/pmc9168996.xml').read_bytes()).hexdigest(),
     'same_experiment_source_passage':passage,
     'candidate_classifications':[
         {'pmid':'24145116','url':'https://pubmed.ncbi.nlm.nih.gov/24145116/',
          'topic':'family-specific juvenile growth and hepatic expression in GH-transgenic triploid Atlantic salmon',
          'relation':'separate published juvenile family comparison (AS11/AS26 vs AS25), 32K microarray and qPCR; not same temperature task or RNA-seq assay',
          'independent_same_task_validation':False},
         {'pmid':'31891812','url':'https://pubmed.ncbi.nlm.nih.gov/31891812/',
          'topic':'three-temperature antiviral response in AquAdvantage female triploid salmon',
          'relation':'subset of fish at 800 g from same overarching experiment according to target paper; injected pIC/PBS and assessed head-kidney qPCR at timepoints, rather than basal liver RNA-seq',
          'independent_same_task_validation':False}],
     'limits':['A separately published sample subset is not automatically an independent rearing cohort; source identifies shared overarching experiment.',
               'Different tissue, perturbation and assay prevent direct held-out gene-effect validation, although the 2019 result is relevant biological context.',
               'Neither abstract supplies individual expression matrix; no accession payload, fair comparator or independent discovery credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
