# 🏙️ Jeddah Property Investment Scorecard

> A Python-based real estate evaluation tool that scores Jeddah residential properties on investment potential using rental yield benchmarking, price analysis, Vision 2030 strategic alignment, and supply-side risk — deployed as a live Streamlit web application.

---

# Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
](https://jeddahrealestatescorecard-9ftuvu4etzu9kcgbi3opo5.streamlit.app)

---

## 📌 Overview

This tool replicates the evaluation framework used by real estate analysts at firms like JLL, CBRE, and Cavendish Maxwell to assess residential property investments in Jeddah, Saudi Arabia.

It evaluates any property across **four weighted dimensions**:

| Dimension | Weight | What it measures |
|---|---|---|
| Rental Yield | 40% | Gross yield vs district and city averages |
| Price Value | 25% | Price/sqm vs district benchmark |
| Vision 2030 Alignment | 20% | Proximity to strategic development zones |
| Supply Safety | 15% | Protection from new-unit pipeline dilution |

Output: a **composite Investment Score (0–100)** with a **BUY / HOLD / AVOID** verdict and analyst rationale.

---

## 📊 Data Sources

All benchmarks sourced from publicly available institutional research:

- **Cavendish Maxwell** — KSA Residential Real Estate Market Performance H1 2025
- **JLL** — KSA Living Market Dynamics Q2 2025
- **GAStat** — Real Estate Price Index Q4 2025
- **Mordor Intelligence** — Jeddah Commercial Real Estate Report, January 2026
- **Global Property Guide** — Saudi Arabia Rental Yield Survey Q1 2026
- **REGA / Ejar Platform** — Transaction and rental market data

---

## 🏘️ Districts Covered

15 Jeddah districts including:
- Al-Shati (Corniche), Al-Zahra, Al-Nahdah
- Jeddah Central Zone, Al-Hamra, Al-Rawdah
- Obhur Al-Shamaliyah, Al-Murjan, Al-Basateen
- Al-Balad (Historic), Al-Salamah, Al-Faisaliyah
- Mishrifah, Al-Marwah, Al-Khalidiyah

---

## 🚀 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/jeddah-property-scorecard.git
cd jeddah-property-scorecard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📓 Google Colab Notebook

The analysis logic is also available as a standalone Google Colab notebook (`jeddah_real_estate_scorecard.ipynb`) that includes:
- Full district reference data with sources
- Interactive property evaluation
- 4-panel scorecard dashboard (Plotly)
- District matrix bubble chart
- Batch portfolio comparison tool

---

## 🗂️ Repository Structure

```
├── app.py                              # Streamlit web application
├── jeddah_real_estate_scorecard.ipynb  # Google Colab notebook
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 💼 Context

Built as part of a data analytics portfolio targeting Vision 2030-aligned roles in KSA — specifically within real estate advisory, institutional investment analysis, and economic research functions.

**Skills demonstrated:** Python (Pandas, Plotly), financial ratio analysis, market benchmarking, Streamlit deployment, data sourcing from institutional research.

---

## ⚠️ Disclaimer

For informational and portfolio demonstration purposes only. Not financial advice. District benchmarks are sourced from publicly available market research and reflect conditions as of H1 2025 – Q1 2026.
