"""Replay printed degree-day accounting in the thesis growth tables; arithmetic only."""
from pathlib import Path
import hashlib, json, statistics, subprocess
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'data/sources/ignatz2019_thesis.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
# Table 2-1 cumulative degree days (C.d) by month post-first feeding, transcribed from the printed table
DD={10.5:[514,834,1160,1467,1797,2158,2434,2736,3106,3387,3778,4065,4353,4709,5013,5175],
    13.5:[614,1011,1415,1802,2226,2696,2987,3454,3929,4314,4792,5161,5557,5838],
    16.5:[718,1212,1719,2179,2646,3186,3624,4078,4652,5095,5677,6118,6565]}
DAYS_TO_1500={10.5:475,13.5:418,16.5:382}   # printed in results text
START_TEMP=13.0        # fry held at 13 C per methods
FEED_INTRO_DAYS=14     # introduced to feed over 14 days per methods
CALENDAR_MONTH=30.44   # average calendar month length in days
TOL=0.5                # printed temperature tolerance +-0.5 C
out={'source_url':'https://memorial.scholaris.ca/items/eef8b6b0-8b69-499a-a6a3-2bf0e1567743',
     'source_file':pdf.name,'sha256':sha,'checks':{},'limits':[],'gate_credit':{}}
m1={};term={};cad={}
for T,dds in DD.items():
    ramp=(START_TEMP+T)/2.0
    pred1=FEED_INTRO_DAYS*START_TEMP+ramp+31*T
    span=FEED_INTRO_DAYS+1+(dds[0]-FEED_INTRO_DAYS*START_TEMP-ramp)/T
    m1[str(T)]={'printed_cdd':dds[0],'predicted_cdd_from_methods_timeline':round(pred1,2),
                'residual_cdd':round(dds[0]-pred1,2),'within_tolerance_band':abs(dds[0]-pred1)<=TOL*46,
                'implied_month1_span_days':round(span,2)}
    days=DAYS_TO_1500[T]
    pred_final=days*T+FEED_INTRO_DAYS*START_TEMP+ramp
    term[str(T)]={'printed_days_to_1500g':days,'printed_final_cdd':dds[-1],
                  'predicted_final_cdd':round(pred_final,2),'residual_cdd':round(dds[-1]-pred_final,2),
                  'tolerance_band_cdd':round(TOL*days,1),
                  'within_tolerance_band':abs(dds[-1]-pred_final)<=TOL*days}
    incs=[dds[i]-dds[i-1] for i in range(1,len(dds))]
    de=[round(x/T,2) for x in incs]          # day-equivalents per printed month
    nonterm=de[:-1]                          # last printed month is partial (terminal)
    band=(CALENDAR_MONTH*(1-TOL/T),CALENDAR_MONTH*(1+TOL/T))
    outside=[x for x in nonterm if not (band[0]<=x<=band[1])]
    cad[str(T)]={'monthly_increments_day_equivalents':de,'nonterminal_min':min(nonterm),
                 'nonterminal_max':max(nonterm),'nonterminal_mean':round(statistics.mean(nonterm),2),
                 'calendar_month_constant_setpoint_band':[round(band[0],1),round(band[1],1)],
                 'nonterminal_months_outside_band':len(outside),'nonterminal_months':len(nonterm)}
out['checks']['month1_replay']=m1
out['checks']['terminal_replay']=term
out['checks']['month_cadence']=cad
out['checks']['dash_pattern_consistent']={str(T):{'months_printed':len(dds),'days_to_1500g':DAYS_TO_1500[T],
    'days_over_calendar_month':round(DAYS_TO_1500[T]/CALENDAR_MONTH,2)} for T,dds in DD.items()}
out['checks']['tgc_values_replayable_from_printed_inputs']=False
out['limits']=['Arithmetic replay of printed numbers only; no growth biology, line, or product-level inference',
 'Monthly mean weights are shown only graphically (Figure 2-1), so the printed TGC values cannot be replayed from printed numeric inputs; the document alone cannot verify them',
 'Month-1 and terminal replays assume the printed methods timeline (14-day 13 C feed introduction, 24-h ramp, then setpoint); the day-count anchor for days-to-1500 g is not explicitly printed and is inferred from the close numeric match',
 'Individual month increments behave like sampling intervals, not constant-temperature calendar months; daily temperature logs are not printed, so per-month calendar consistency cannot be resolved from the document',
 'Residuals within the printed +-0.5 C tolerance do not prove the underlying logs; they show the printed aggregates are mutually consistent']
out['gate_credit']={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
print(json.dumps(out,indent=2,sort_keys=True))
