"""Cross-equation arithmetic audit of printed thesis Tables 2-2 and 2-3.

Pure printed-number replay: applies the thesis's own Equations 1-4 (FCR, k, HSI,
VSI) and the TGC definition to the printed means, checks what is and is not
replayable from the document, and checks Table 2-3 component sums against the
printed dry-matter percentage. No biological inference.
"""
from pathlib import Path
import hashlib, json, subprocess
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'data/sources/ignatz2019_thesis.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()

# Table 2-2 printed means (SEM omitted from replay but recorded). Intervals per caption:
# values at 800 g cover 500-800 g; values at 1500 g cover 800-1500 g.
T22={'800':{'interval_g':[500,800],
   'TGC':{10.5:2.31,13.5:1.45,16.5:1.37},'FI':{10.5:4.47,13.5:4.51,16.5:5.13},
   'FCR':{10.5:0.81,13.5:0.87,16.5:0.94},'k':{10.5:1.25,13.5:1.26,16.5:1.31},
   'HSI':{10.5:0.91,13.5:0.97,16.5:0.91},'VSI':{10.5:6.96,13.5:7.29,16.5:7.82}},
 '1500':{'interval_g':[800,1500],
   'TGC':{10.5:2.09,13.5:1.86,16.5:1.43},'FI':{10.5:6.01,13.5:6.86,16.5:7.31},
   'FCR':{10.5:0.86,13.5:0.87,16.5:1.01},'k':{10.5:1.32,13.5:1.36,16.5:1.40},
   'HSI':{10.5:0.94,13.5:1.07,16.5:1.00},'VSI':{10.5:7.08,13.5:8.38,16.5:8.86}}}
TEMPS=[10.5,13.5,16.5]

# Table 2-3 printed means (% as-is) with n values.
T23={
 '300':{10.5:{'DM':32.72,'protein':17.48,'lipid':11.77,'ash':1.99,'n':12},
        13.5:{'DM':34.15,'protein':17.42,'lipid':13.43,'ash':2.07,'n':12},
        16.5:{'DM':34.90,'protein':17.49,'lipid':14.33,'ash':2.02,'n':12}},
 '500':{10.5:{'DM':33.51,'protein':17.18,'lipid':13.02,'ash':2.14,'n':12},
        13.5:{'DM':35.36,'protein':17.78,'lipid':14.51,'ash':2.03,'n':12},
        16.5:{'DM':35.86,'protein':18.31,'lipid':14.26,'ash':2.22,'n':12}},
 '800':{10.5:{'DM':35.74,'protein':17.79,'lipid':15.11,'ash':2.20,'n':12},
        13.5:{'DM':36.27,'protein':17.59,'lipid':15.68,'ash':2.10,'n':10},
        16.5:{'DM':36.10,'protein':17.60,'lipid':15.78,'ash':2.01,'n':13}},
 '1500':{10.5:{'DM':36.70,'protein':17.89,'lipid':16.22,'ash':2.01,'n':12},
         13.5:{'DM':38.02,'protein':18.11,'lipid':16.81,'ash':2.01,'n':12},
         16.5:{'DM':38.95,'protein':17.98,'lipid':18.22,'ash':2.01,'n':12}}}

out={'source_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
     'source_file':pdf.name,'sha256':sha,'checks':{},'limits':[],'gate_credit':{}}

# --- Table 2-2 cross-equation replay -------------------------------------
t22={}
for weight,blk in T22.items():
    w0,w1=blk['interval_g']; gain=w1-w0
    cube_delta=(w1**(1/3.0)-w0**(1/3.0))*1000.0
    per={}
    for T in TEMPS:
        fcr=blk['FCR'][T]; fi=blk['FI'][T]; tgc=blk['TGC'][T]
        feed_per_fish_g=fcr*gain                       # Equation 1 rearranged (dry matter)
        fcr_days=feed_per_fish_g/fi                    # valid only if FI is g/fish/day (unit not printed)
        tgc_days=cube_delta/(T*tgc)                    # TGC definition rearranged
        per[str(T)]={'printed_TGC':tgc,'printed_FI':fi,'printed_FCR':fcr,
            'implied_feed_per_fish_g':round(feed_per_fish_g,2),
            'fcr_implied_days_if_FI_g_per_fish_day':round(fcr_days,2),
            'tgc_implied_days':round(tgc_days,2),
            'day_estimate_residual':round(tgc_days-fcr_days,2)}
    t22[weight]={'interval_g':[w0,w1],'cube_root_delta_times_1000':round(cube_delta,4),'per_temperature':per}
out['checks']['table_2_2_cross_equation']=t22
out['checks']['table_2_2_day_estimates_agree_within_2d_only_at_10_5C']=all(
    abs(t22[w]['per_temperature']['10.5']['day_estimate_residual'])<2.0 for w in t22)
out['checks']['table_2_2_max_abs_day_residual_other_temps']=round(max(
    abs(t22[w]['per_temperature'][str(T)]['day_estimate_residual'])
    for w in t22 for T in (13.5,16.5)),2)
out['checks']['fi_units_printed_in_caption_or_methods']=False
out['checks']['k_hsi_vsi_replayable_from_printed_inputs']=False

# --- Table 2-3 component-sum replay ---------------------------------------
t23={}
all_ok=True
for weight,cells in T23.items():
    per={}
    for T in TEMPS:
        c=cells[T]
        comp=c['protein']+c['lipid']+c['ash']
        other=round(c['DM']-comp,2)
        ok=other>=0
        all_ok=all_ok and ok
        per[str(T)]={'printed_DM':c['DM'],'printed_protein':c['protein'],'printed_lipid':c['lipid'],
            'printed_ash':c['ash'],'n':c['n'],'component_sum':round(comp,2),
            'other_dry_matter_fraction':other,'implied_moisture_pct':round(100-c['DM'],2),
            'components_within_dry_matter':ok}
    t23[weight]=per
out['checks']['table_2_3_component_sums']=t23
out['checks']['table_2_3_all_cells_components_within_dry_matter']=all_ok
out['checks']['table_2_3_other_dry_matter_range_pct']=[
    min(t23[w][str(T)]['other_dry_matter_fraction'] for w in t23 for T in TEMPS),
    max(t23[w][str(T)]['other_dry_matter_fraction'] for w in t23 for T in TEMPS)]

out['limits']=[
 'Arithmetic replay of printed table means only; no growth, husbandry, or product-level inference',
 'FI units are not printed in the Table 2-2 caption or the methods equations section; the day estimates derived from FCR are valid only if FI is dry-matter g/fish/day, so the day-estimate residuals at 13.5 and 16.5 C are an unresolved consistency question, not a demonstrated error',
 'TGC-implied days use the cube-root TGC definition with the printed treatment setpoint as the interval temperature; daily logs are not printed',
 'k, HSI and VSI are not replayable: fork lengths and liver/viscera weights appear nowhere as printed numbers',
 'Table 2-3 check is a mass-balance screen (protein+lipid+ash must not exceed printed dry matter); the residual is other dry matter, not an error term',
 'Standard-error columns and significance letters are transcribed context, not replayed statistics']
out['gate_credit']={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
print(json.dumps(out,indent=2,sort_keys=True))
