import streamlit as st
import plotly.express as px

from src.analysis import add_changes, load_data
from src.scoring import strategic_score

st.set_page_config(page_title="UK Economic & Strategic Intelligence", page_icon="🇬🇧", layout="wide")

st.title("🇬🇧 UK Economic & Strategic Intelligence")
st.caption("A lightweight decision-intelligence dashboard for macroeconomic and strategic analysis")

try:
    df = load_data()
    df = strategic_score(add_changes(df))
except Exception as exc:
    st.error(f"Data validation error: {exc}")
    st.stop()

latest = df.iloc[-1]
prev = df.iloc[-2]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("GDP growth", f"{latest.gdp_growth_pct:.1f}%", f"{latest.gdp_growth_pct - prev.gdp_growth_pct:+.1f} pp")
c2.metric("Inflation", f"{latest.cpi_pct:.1f}%", f"{latest.cpi_pct - prev.cpi_pct:+.1f} pp")
c3.metric("Unemployment", f"{latest.unemployment_pct:.1f}%", f"{latest.unemployment_pct - prev.unemployment_pct:+.1f} pp")
c4.metric("Bank Rate", f"{latest.bank_rate_pct:.2f}%", f"{latest.bank_rate_pct - prev.bank_rate_pct:+.2f} pp")
c5.metric("Strategic balance", f"{latest.strategic_balance:.1f}/100")

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Economic trajectory")
    metric = st.selectbox("Indicator", ["gdp_growth_pct", "cpi_pct", "unemployment_pct", "employment_pct", "average_weekly_earnings_growth_pct", "productivity_growth_pct"])
    labels = {
        "gdp_growth_pct": "GDP growth (%)", "cpi_pct": "Inflation (%)", "unemployment_pct": "Unemployment (%)",
        "employment_pct": "Employment rate (%)", "average_weekly_earnings_growth_pct": "Earnings growth (%)", "productivity_growth_pct": "Productivity growth (%)"
    }
    fig = px.line(df, x="year", y=metric, markers=True, title=labels[metric])
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Strategic signal")
    score_df = df[["year", "opportunity_score", "pressure_score", "strategic_balance"]].melt("year", var_name="signal", value_name="score")
    fig = px.line(score_df, x="year", y="score", color="signal", markers=True, range_y=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Financial & external indicators")
financial = df[["year", "bank_rate_pct", "gbp_usd", "gbp_eur", "trade_balance_gbp_bn", "public_sector_net_debt_pct_gdp"]]
st.dataframe(financial, use_container_width=True, hide_index=True)

st.subheader("Executive interpretation")
if latest.strategic_balance >= 60:
    st.success("Current model signal: relatively stronger strategic balance in the available baseline.")
elif latest.strategic_balance >= 40:
    st.warning("Current model signal: mixed conditions; opportunity and pressure indicators are balanced.")
else:
    st.error("Current model signal: elevated pressure relative to the available baseline.")

with st.expander("Methodology & data integrity"):
    st.write("Opportunity, pressure and strategic-balance scores are model-derived indicators, not official statistics. The repository is being rebuilt around an authoritative ONS/Bank of England source registry. The starter CSV is a development baseline and must be replaced/validated against the registered primary-source series before the project is presented as an official-data analysis.")
    st.write("Primary planned sources: Office for National Statistics (ONS) and Bank of England (BoE). International context: World Bank, IMF and OECD.")
