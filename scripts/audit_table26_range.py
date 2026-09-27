"""Replay printed Table 2-6 fillet-nutrient rows as a bounded source-context check."""
from pathlib import Path
import hashlib, json, re, subprocess
root = Path(__file__).resolve().parents[1]
pdf = root / 'data/sources/ignatz2019_thesis.pdf'
txt = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
sec = txt.split('Table 2-6. Nutrient utilization:')[-1].split('2.4.4 Fillet colour', 1)[0]
body = sec.split('Variables', 1)[1]
pat = r'^\s*(Σ ω3|DHA|EPA|Lys|Met|His|P|Ca)( RE \(%\)| \[mg \(°C·d\)-1\])\s+(.+)$'
periods = {}
for idx, period in enumerate([2, 3]):
    s = body.split(f'Period {period} (', 1)[1]
    if period == 2:
        s = s.split('Period 3 (', 1)[0]
    rows = {}
    for line in s.splitlines():
        m = re.match(pat, line)
        if not m:
            continue
        key = m.group(1) + (' RE' if 'RE' in m.group(2) else ' deposition')
        nums = re.findall(r'(-?\d+\.\d+)(?:[A-Za-z]+)?', m.group(3))
        assert len(nums) == 6, (period, key, line, nums)
        rows[key] = [float(v) for v in nums[::2]]
    assert len(rows) == 16, (period, len(rows))
    periods[str(period)] = rows
nutes = ['Σ ω3', 'DHA', 'EPA', 'Lys', 'Met', 'His', 'P', 'Ca']
re_above = [{'period': p, 'nutrient': n, 'temp_C': t, 'printed_re_pct': v}
            for p, rows in periods.items() for n in nutes
            for t, v in zip((10.5, 13.5, 16.5), rows[n + ' RE']) if v > 100]
deltas = {n: {str(t): round(periods['3'][n + ' deposition'][i] - periods['2'][n + ' deposition'][i], 2)
              for i, t in enumerate((10.5, 13.5, 16.5))} for n in nutes}
out = {'source_url': 'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
 'source_file': pdf.name, 'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
 'printed_thesis_pages': '60-62', 'table_2_6_means': periods,
 'checks': {'row_count': sum(map(len, periods.values())), 'mean_cell_count': 96,
            'retention_efficiencies_above_100': re_above,
            'period3_minus_period2_deposition': deltas},
 'limits': ['Printed treatment means only; no tank-level replicates or intake denominators recovered, so retention efficiencies cannot be independently recomputed.',
            'The caption reports n=3 and significance letters; no statistical reanalysis is made.',
            'Any above-100% retention values are flagged as printed, not declared impossible; composition and intake denominators may differ.',
            'Descriptive table replay only; no husbandry, feed, or product recommendation follows.'],
 'gate_credit': {'external_services': 0, 'fetched_and_used_accession_datasets': 0, 'audited_derivations': 0, 'paper_pages': 0}}
print(json.dumps(out, indent=2, sort_keys=True))
