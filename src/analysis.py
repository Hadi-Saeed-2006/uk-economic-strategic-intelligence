from __future__ import annotations

import pandas as pd


def load_data(path: str = "data/uk_macro.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"year", "gdp_growth_pct", "cpi_pct", "unemployment_pct", "employment_pct", "average_weekly_earnings_growth_pct", "bank_rate_pct", "gbp_usd", "gbp_eur", "productivity_growth_pct", "trade_balance_gbp_bn", "public_sector_net_debt_pct_gdp"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df.sort_values("year").reset_index(drop=True)


def add_changes(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ["gdp_growth_pct", "cpi_pct", "unemployment_pct", "bank_rate_pct", "public_sector_net_debt_pct_gdp"]:
        out[f"{col}_change"] = out[col].diff()
    return out
