import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_growth_composition_tables():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_growth_composition_tables.py')],text=True))
 assert d==json.loads((R/'results/growth_composition_table_audit.json').read_text())
 assert d['checks']['table_2_3_all_cells_components_within_dry_matter'] is True
 lo,hi=d['checks']['table_2_3_other_dry_matter_range_pct']
 assert 0.0<lo<=hi<3.0
 assert d['checks']['table_2_2_day_estimates_agree_within_2d_only_at_10_5C'] is True
 assert d['checks']['table_2_2_max_abs_day_residual_other_temps']>4.0
 assert d['checks']['fi_units_printed_in_caption_or_methods'] is False
 assert d['checks']['k_hsi_vsi_replayable_from_printed_inputs'] is False
 for w in ('800','1500'):
  for T in ('10.5','13.5','16.5'):
   cell=d['checks']['table_2_2_cross_equation'][w]['per_temperature'][T]
   assert cell['implied_feed_per_fish_g']>0
 assert all(v==0 for v in d['gate_credit'].values())
