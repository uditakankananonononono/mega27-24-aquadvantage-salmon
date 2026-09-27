"""Screen an independent Atlantic salmon heat study for comparable expression data."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
 'study_2014_title': ('pmc4046827.xml', 'Transcriptional responses to temperature and low oxygen stress in Atlantic salmon'),
 'study_2022_title': ('pmc9168996.xml', 'RNA-Seq Analysis of the Growth Hormone Transgenic Female Triploid Atlantic Salmon'),
}
NEEDLES = {
 'pooled_libraries': 'By using pooled samples, and two different library construction methods',
 'nonquantitative': 'have not attempted to compare the libraries quantitatively',
 'heat_setting': 'chronic high temperature (19°C)',
 'transgenic_target': 'growth hormone transgenic female triploid',
}

def replay():
 evidence = {}
 for key, (name, title) in TARGETS.items():
  raw = (ROOT / 'data/sources' / name).read_bytes()
  soup = BeautifulSoup(raw, 'xml')
  text = soup.get_text(' ', strip=True)
  if title.casefold() not in text.casefold():
   raise ValueError('Primary title mismatch: ' + key)
  evidence[key] = {'url': ('https://pmc.ncbi.nlm.nih.gov/articles/PMC4046827/' if key == 'study_2014_title' else 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9168996/'), 'sha256': hashlib.sha256(raw).hexdigest(), 'title': title}
 soup14 = BeautifulSoup((ROOT / 'data/sources/pmc4046827.xml').read_bytes(), 'xml')
 passages = [p.get_text(' ', strip=True) for p in soup14.find_all('p')] + [a.get_text(' ', strip=True) for a in soup14.find_all('abstract')]
 matched = {}
 for key, needle in NEEDLES.items():
  if key == 'transgenic_target':
   soup22 = BeautifulSoup((ROOT / 'data/sources/pmc9168996.xml').read_bytes(), 'xml')
   candidates = [a.get_text(' ', strip=True) for a in soup22.find_all('abstract')] + [p.get_text(' ', strip=True) for p in soup22.find_all('p')]
  else:
   candidates = passages
  hits = [p for p in candidates if needle.casefold() in p.casefold()]
  if not hits: raise ValueError('Source passage absent: ' + key)
  matched[key] = hits[0]
 return {
  'evidence': evidence,
  'source_passages': matched,
  'comparison': {'2014': 'Atlantic salmon 19°C chronic heat and low oxygen, pooled/SSH and normalized cDNA libraries; authors say not quantitative comparisons', '2022': 'female triploid growth-hormone-transgenic Atlantic salmon, 10.5/13.5/16.5°C, 18 hepatic RNA-seq libraries'},
  'eligibility': {'independent_population': True, 'same_organism': True, 'same_transgenic_cohort_or_product': False, 'matching_temperature_exposure': False, 'per_sample_quantitative_expression_comparable': False, 'eligible_as_held_out_same_task_cohort': False},
  'limits': ['Different population, treatment levels, library construction and measurement estimands; do not treat orthologous themes as transcript-level cross-validation.', 'The 2014 study is a useful context/negative comparator candidate, not an independent quantitative held-out validation set for the 2022 transgenic temperature data.', 'No raw expression cohort, efficacy, environmental safety, accession gate or discovery is established by this screen.'],
  'gate_credit': {'applied_external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'substantive_paper_pages':0},
 }

if __name__ == '__main__':
 print(json.dumps(replay(), sort_keys=True, indent=2))
