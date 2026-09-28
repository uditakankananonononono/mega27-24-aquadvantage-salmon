"""Provenance-aware descriptive endpoint-conflict certificate; no causal optimization."""
from pathlib import Path
import itertools,json,math,collections,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'results/temperature_endpoint_reversal.json'
a=json.loads(p.read_text())['published_values']
temps=['10.5C','13.5C','16.5C']
endpoints={'days_to_1500g':[a['days_to_1500_g'][k] for k in temps],
 'late_FCR':a['FCR_800_to_1500_g']['means_10_5_13_5_16_5'],
 'late_TGC':a['TGC_800_to_1500_g']['means_10_5_13_5_16_5']}
# All objectives transformed into higher-is-better benefit, without pooling raw measurement units.
benefits={k:[((max(v)-x)/(max(v)-min(v)) if k!='late_TGC' else (x-min(v))/(max(v)-min(v))) for x in v] for k,v in endpoints.items()}
assert all(min(v)==0 and max(v)==1 for v in benefits.values())
K=list(benefits)
vec=[tuple(benefits[k][i] for k in K) for i in range(3)]
def dominates(i,j):return all(x>=y-1e-12 for x,y in zip(vec[i],vec[j])) and any(x>y+1e-12 for x,y in zip(vec[i],vec[j]))
pareto=[temps[i] for i in range(3) if not any(dominates(j,i) for j in range(3) if j!=i)]
wins=collections.Counter(); ties=0
for i in range(101):
 for j in range(101-i):
  z=100-i-j
  weights=(i/100,j/100,z/100)
  scores=[sum(w*b for w,b in zip(weights,v)) for v in vec]
  m=max(scores); idx=[n for n,s in enumerate(scores) if abs(s-m)<1e-10]
  if len(idx)>1:ties+=1
  # Do not arbitrarily assign tie winners to a temperature.
  wins['|'.join(temps[n] for n in idx)]+=1
assert sum(wins.values())==5151
out={'source_url':a if False else 'https://memorial.scholaris.ca/bitstreams/a668d444-72ba-4897-91b9-d8b38ac6257d/download',
 'source_audit_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'objective_order':K,'temperature_order':temps,'published_mean_endpoints':endpoints,
 'minmax_benefits_by_temperature':dict(zip(temps,vec)),
 'pareto_nondominated':pareto,'dominated_pairs':[{'dominant':temps[i],'dominated':temps[j]} for i in range(3) for j in range(3) if i!=j and dominates(i,j)],
 'weight_grid_step':.01,'weight_vectors':5151,'winner_set_counts':dict(sorted(wins.items())),
 'tie_weight_vectors':ties,'calendar_only_winner':temps[endpoints['days_to_1500g'].index(min(endpoints['days_to_1500g']))],
 'interpretation':'The warmest group wins calendar time but loses late-interval FCR and TGC to the coolest; multiple nondominated treatments and preference-sensitive winners preclude a source-supported unique best temperature.',
 'limits':['Published group means are from one same-cohort study, with unknown joint fish-level uncertainty and no held-out validation.',
 'Weighted min-max scoring is a descriptive preference illustration, not a welfare, price, profit or causal recommendation.',
 'Temperature groups were sampled at different ages to a matched weight and fish were nested within tanks.',
 'Pareto methods and weighted sums are established prior art; no novel algorithm or new biological discovery is claimed.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
