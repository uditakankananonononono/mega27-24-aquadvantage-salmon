"""Printed Table 2-7 means replay, restricted to arithmetic, no fish-level inference."""
from pathlib import Path
import hashlib, json, re, subprocess
root = Path(__file__).resolve().parents[1]
pdf = root/'data/sources/ignatz2019_thesis.pdf'
text = subprocess.check_output(['pdftotext','-layout',str(pdf),'-'], text=True)
section = text.split('Table 2-7. Fillet yield, total astaxanthin concentration')[-1].split('2.4.5 Regression models')[0]
rows = {}
for key, line_start in [('fillet_yield_pct','Fillet yield (%)'),('astaxanthin_ug_per_g','Total astaxanthin'),('salmo_fan_score','DSM SalmoFan')]:
    line = next(l for l in section.splitlines() if l.strip().startswith(line_start))
    cells = re.findall(r'(-?\d+\.\d+)([ab]*)\s+(\d+\.\d+)\s+(\d+)', line)
    assert len(cells) == 3, (key, line, cells)
    rows[key] = {str(t): {'mean':float(v),'sem':float(sem),'n':int(n),'letter':letter or None}
                 for t,(v,letter,sem,n) in zip((10.5,13.5,16.5),cells)}
f = rows['fillet_yield_pct']
diff = {str(t): round((f[str(t)]['mean']/f['16.5']['mean']-1)*100,2) for t in (10.5,13.5)}
out = {'source_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
       'source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(), 'printed_thesis_page':63,
       'table_2_7':rows, 'fillet_yield_relative_to_16_5_pct':diff,
       'fillet_yield_absolute_percentage_points':{str(t):round(f[str(t)]['mean']-f['16.5']['mean'],2) for t in (10.5,13.5)},
       'printed_prose_claim_pct':{'10.5':7,'13.5':4},
       'finding':'The nearby prose says fillet yields were higher by 7% and 4%. The printed means differ by 7.16 and 4.48 percentage points, respectively, whereas the relative increases over the 16.5 C mean are 13.74% and 8.60%. The prose is consistent with roughly rounded absolute percentage-point differences, not relative percent increases; its exact rounding convention is not specified.',
       'limits':['Table means, SEM, n and letters transcribed only; no fish-level measurements or statistical reanalysis',
                 'The descriptive percentage gap is not proof of an author error or a treatment recommendation',
                 'No externally valid commercial yield or product comparison is established'],
       'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
