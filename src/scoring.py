from __future__ import annotations

import numpy as np
import pandas as pd


def _minmax(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(50.0, index=series.index)
    return 100 * (series - lo) / (hi - lo)


def strategic_score(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Opportunity signals: stronger growth/productivity, lower inflation/unemployment/debt pressure.
    growth = _minmax(out["gdp_growth_pct"])
    productivity = _minmax(out["productivity_growth_pct"])
    employment = _minmax(out["employment_pct"])
    inflation_stability = 100 - _minmax((out["cpi_pct"] - 2.0).abs())
    labour_stability = 100 - _minmax(out["unemployment_pct"])
    fiscal_headroom = 100 - _minmax(out["public_sector_net_debt_pct_gdp"])
    out["opportunity_score"] = (0.30 * growth + 0.20 * productivity + 0.20 * employment + 0.15 * inflation_stability + 0.15 * labour_stability).round(1)
    out["pressure_score"] = (0.55 * _minmax(out["cpi_pct"]) + 0.25 * _minmax(out["unemployment_pct"]) + 0.20 * _minmax(out["public_sector_net_debt_pct_gdp"])).round(1)
    out["strategic_balance"] = (0.75 * out["opportunity_score"] + 0.25 * fiscal_headroom - 0.35 * out["pressure_score"]).clip(0, 100).round(1)
    return out
