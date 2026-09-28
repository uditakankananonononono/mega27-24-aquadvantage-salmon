"""Audit source unit hierarchy and calendar-time aliasing for the published RNA-seq experiment."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/sources/pmc9168996.xml'
s=BeautifulSoup(p.read_text(),'xml')
def one(needle):
    hits=[x.get_text(' ',strip=True) for x in s.find_all('p') if needle in x.get_text(' ',strip=True)]
    assert len(hits)==1,(needle,len(hits))
    return hits[0]
rearing=one('tanks at 10.5°C, 13.5°C, and 16.5°C')
selection=one('Twenty-one liver samples were collected per rearing temperature')
libraries=one('A total of 18 stranded PE100 libraries')
assert 'in triplicate' in rearing and '10, 11, and 12\u00a0months' in rearing
assert 'two samples per tank ( n = 6 per temperature treatment)' in selection
assert '±1 standard deviation' in selection and 'randomly chosen' in selection
assert 'six RNA samples per rearing temperature' in libraries
# The exact SRR-to-tank mapping is not printed in this table, even though the methods describe 2 fish per tank.
t=s.find('table-wrap',id='T1');assert t is not None
text=t.get_text(' ',strip=True)
runs=re.findall(r'\bSRR\d+\b',text)
assert len(runs)==18 and len(set(runs))==18
out={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'rearing_quote':rearing,'selection_quote':selection,'sequencing_quote':libraries,
     'article_table_1_run_accessions':runs,'temperature_count':3,
     'tanks_per_temperature':3,'selected_fish_per_tank':2,
     'fish_rna_libraries_per_temperature':6,'fish_rna_libraries_total':18,
     'initial_liver_samples_per_temperature':21,
     'selected_fraction_per_temperature':6/21,
     'temperature_to_approximate_sampling_month':{'16.5 C':10,'13.5 C':11,'10.5 C':12},
     'finding':'The published design contains three tanks per temperature and two selected fish per tank; 18 fish RNA libraries are nested within nine tanks, not 18 independently assigned temperature units. Sampling calendar/age differs approximately 10/11/12 months for the warm/middle/cool groups because fish were size matched.',
     'limits':['The article methods do not print a Table 1 SRR-to-tank assignment; no tank-aware model is fitted or independence quantified here.',
               'Tank-level clustering does not by itself refute the authors differential-expression findings; it limits a naive independent-fish inference.',
               'Temperature, time-to-size, and age-at-sampling are bundled in this size-matched design, so their separate causal effects are not identified by this contrast.',
               'The 18 Table 1 accessions are run identifiers only; no FASTQ payload is individually fetched and used in this audit.',
               'No comparator win, new biology, independently audited derivation or paper-page credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,sort_keys=True,indent=2))
