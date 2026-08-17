import pandas as pd
import streamlit as st
import plotly.express as px

from src.analysis import add_changes, load_data
from src.scoring import strategic_score

st.set_page_config(page_title="UK Economic & Strategic Intelligence", page_icon="🇬🇧", layout="wide")

st.title("🇬🇧 UK Economic & Strategic Intelligence")
st.caption("Decision intelligence for UK macroeconomic, financial and strategic conditions")

try:
    df = strategic_score(add_changes(load_data()))
except Exception as exc:
    st.error(f"Data validation error: {exc}")
    st.stop()

latest = df.iloc[-1]
prev = df.iloc[-2]

st.info("**Data status:** 2025 annual indicators are used where annual data is appropriate. Regional labour data uses ONS rolling three-month LFS estimates; source periods are shown explicitly.")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("GDP growth", f"{latest.gdp_growth_pct:.1f}%", f"{latest.gdp_growth_pct - prev.gdp_growth_pct:+.1f} pp")
c2.metric("CPI", f"{latest.cpi_pct:.1f}%", f"{latest.cpi_pct - prev.cpi_pct:+.1f} pp")
c3.metric("Unemployment", f"{latest.unemployment_pct:.1f}%", f"{latest.unemployment_pct - prev.unemployment_pct:+.1f} pp")
c4.metric("Bank Rate", f"{latest.bank_rate_pct:.2f}%", f"{latest.bank_rate_pct - prev.bank_rate_pct:+.2f} pp")
c5.metric("Strategic balance", f"{latest.strategic_balance:.1f}/100")
st.caption("Reference year: 2025 for the displayed macro baseline. Financial indicators retain their source-period definitions.")

st.divider()

st.subheader("🗺️ UK 4D Regional Intelligence Map")
st.caption("4D = geographic position + indicator intensity + time. Use the animation controls to move between ONS regional labour-market periods.")

try:
    regional = pd.read_csv("data/uk_regional_map.csv")
    required = {"period", "region", "employment_rate_pct", "unemployment_rate_pct", "inactivity_rate_pct", "latitude", "longitude"}
    missing = required - set(regional.columns)
    if missing:
        raise ValueError(f"Missing map columns: {sorted(missing)}")

    map_metric = st.selectbox(
        "Map intelligence layer",
        ["unemployment_rate_pct", "employment_rate_pct", "inactivity_rate_pct"],
        format_func=lambda x: {"unemployment_rate_pct": "Unemployment rate (%)", "employment_rate_pct": "Employment rate (%)", "inactivity_rate_pct": "Economic inactivity rate (%)"}[x],
    )
    regional["period"] = regional["period"].astype(str)
    regional["metric"] = regional[map_metric]

    # MapLibre-based scatter_map is more robust on Streamlit Cloud than the older geo renderer.
    fig_map = px.scatter_map(
        regional.sort_values("period"),
        lat="latitude",
        lon="longitude",
        color="metric",
        size="metric",
        animation_frame="period",
        animation_group="region",
        hover_name="region",
        hover_data={
            "metric": ":.1f",
            "employment_rate_pct": ":.1f",
            "unemployment_rate_pct": ":.1f",
            "inactivity_rate_pct": ":.1f",
            "latitude": False,
            "longitude": False,
        },
        zoom=4.6,
        center={"lat": 54.5, "lon": -2.5},
        height=650,
        title="UK regional labour-market intelligence over time",
    )
    fig_map.update_layout(margin={"l": 0, "r": 0, "t": 60, "b": 0})
    fig_map.update_traces(marker={"opacity": 0.85})
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Source: Office for National Statistics Labour Force Survey. Regional LFS estimates are official statistics in development and contain sampling uncertainty; short-term movements should be interpreted cautiously.")
except Exception as exc:
    st.error(f"Regional 4D map could not be rendered: {exc}")

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Economic trajectory")
    metric = st.selectbox("Indicator", ["gdp_growth_pct", "cpi_pct", "unemployment_pct", "employment_pct", "average_weekly_earnings_growth_pct", "productivity_growth_pct"])
    labels = {"gdp_growth_pct": "GDP growth (%)", "cpi_pct": "CPI inflation (%)", "unemployment_pct": "Unemployment (%)", "employment_pct": "Employment rate (%)", "average_weekly_earnings_growth_pct": "Average earnings growth (%)", "productivity_growth_pct": "Productivity growth (%)"}
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
    st.success("Model signal: relatively stronger strategic balance within the historical baseline.")
elif latest.strategic_balance >= 40:
    st.warning("Model signal: mixed conditions; opportunity and pressure indicators are relatively balanced.")
else:
    st.error("Model signal: elevated pressure relative to the historical baseline.")

with st.expander("Methodology, sources & data integrity"):
    st.write("Opportunity, pressure and strategic-balance scores are model-derived indicators, not official statistics. They normalize the available historical baseline and should not be interpreted as forecasts or government assessments.")
    st.write("Primary sources: Office for National Statistics (ONS) and Bank of England (BoE). International context: World Bank, IMF and OECD. See data/SOURCES.md for the source registry and reference-period notes.")
    st.write("The 4D map uses regional ONS LFS labour-market observations. ONS classifies these as official statistics in development and notes sampling variability, so the map is an analytical visualization rather than a precise regional forecast.")
