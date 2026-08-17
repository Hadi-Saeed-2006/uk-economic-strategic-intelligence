# 🇬🇧 UK Economic & Strategic Intelligence

> **A decision-intelligence dashboard for understanding the UK's macroeconomy, financial conditions, trade position and strategic outlook.**

## 🎯 Project objective

This project turns authoritative UK economic indicators into a compact, auditable intelligence product. It is designed to answer:

- How is the UK economy performing?
- What is happening to inflation, wages and employment?
- How are monetary and financial conditions changing?
- What are the UK's trade and external-sector signals?
- Which indicators represent opportunity, pressure or strategic risk?

## 🧭 Intelligence layers

| Layer | Focus |
|---|---|
| Growth | GDP and economic activity |
| Prices | CPI/CPIH and inflation pressure |
| Labour | Employment, unemployment and earnings |
| Monetary | Bank Rate and financial conditions |
| Productivity | Output and productivity signals |
| Trade | Exports, imports and trade balance |
| Fiscal | Public finances and debt context |
| Strategic | Composite opportunity/risk interpretation |

## 📊 Core indicators

The canonical data model is designed around 2020–2025 annual observations where available, with source metadata retained for auditability.

Primary sources:

- **Office for National Statistics (ONS)** — GDP, CPI/CPIH, earnings, labour market, productivity and trade
- **Bank of England (BoE)** — Bank Rate and GBP exchange-rate series
- **World Bank / IMF / OECD** — international context and benchmarking

## 🧠 Intelligence methodology

The project separates three things:

1. **Observed statistics** — sourced from official institutions.
2. **Derived indicators** — calculated from the observed data, such as growth rates, changes and normalized scores.
3. **Strategic interpretation** — an explainable synthesis of economic opportunity and pressure.

No composite score is presented as an official government statistic.

## 🖥️ Planned dashboard

The Streamlit application will provide:

- Executive UK economic overview
- GDP and growth analysis
- Inflation and purchasing-power signals
- Labour-market analysis
- Bank Rate and GBP analysis
- Trade and external-sector view
- Regional/structural context where data quality permits
- Opportunity / pressure scorecards
- Historical trend charts
- Source and methodology panel

## 🛠️ Technology

Python · Pandas · NumPy · Plotly · Streamlit · GitHub Actions

## 📁 Repository structure

```text
uk-economic-strategic-intelligence/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── uk_macro.csv
├── src/
│   ├── analysis.py
│   └── scoring.py
└── .github/
    └── workflows/
        └── validate.yml
```

## ⚠️ Data integrity

The project does not fabricate live economic values. Any unavailable indicator is left explicitly unavailable rather than silently replaced with an invented number. Derived scores are labelled as model outputs.

## 🔭 Roadmap

### Foundation
- [x] Repository structure
- [x] Methodology specification
- [ ] Canonical UK macro dataset
- [ ] Data validation

### Intelligence
- [ ] Economic trend engine
- [ ] Opportunity/pressure scoring
- [ ] Executive insights

### Product
- [ ] Streamlit dashboard
- [ ] Automated validation
- [ ] Deployment
- [ ] Recruiter-facing documentation

## 👤 Author

**Hadi Shaikh** — Data Science student building practical analytics and decision-intelligence products.
