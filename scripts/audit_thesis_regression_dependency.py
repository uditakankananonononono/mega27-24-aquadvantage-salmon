"""Re-express two published thesis equations algebraically, without model validation."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
pdf=R/'data/sources/ignatz2019_thesis.pdf'
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
section=text.split('2.4.5 Regression models')[-1].split('2.5 Discussion')[0]
markers=['BL (%) = 12.082(±0.849) + 0.203(±0.040)T + 0.020(±0.003)LI - 0.073(±0.022)PL',
         'LI = 1.179(±7.922) + 0.112(±0.005)BW + 1.484(±0.288)PL',
         'r2 = 0.940','r2 = 0.986','p = 0.4201','p = 0.115']
assert all(m in section for m in markers)
intercept=12.082+0.020*1.179
bw=0.020*0.112
pl=-0.073+0.020*1.484
out={'source_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
     'source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
     'printed_thesis_page':64,'source_markers':markers,
     'printed_models':{'equation9':'BL (%) = 12.082 + 0.203*T + 0.020*LI - 0.073*PL',
                       'equation10':'LI = 1.179 + 0.112*BW + 1.484*PL',
                       'equation9_reported_r_squared':0.940,'equation10_reported_r_squared':0.986},
     'literal_point_estimate_substitution':{'intercept':round(intercept,6),'T_coefficient':0.203,
                                             'BW_coefficient':round(bw,6),'PL_coefficient':round(pl,6),
                                             'expression':'BL (%) = 12.10558 + 0.203*T + 0.00224*BW - 0.04332*PL'},
     'interpretation':'BW is excluded as a direct Equation 9 predictor in the printed fit but re-enters indirectly through the Equation 10 LI estimate. The two printed R-squared values cannot be multiplied or combined to claim accuracy of the chained predictor.',
     'limits':['Symbolic point-estimate substitution only; no individual data, refit, uncertainty propagation or external validation',
               'The thesis units and population define the original fits; coefficients here are not advice or portable product predictions',
               'No causal effect, fair comparator, novel discovery or gate credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
