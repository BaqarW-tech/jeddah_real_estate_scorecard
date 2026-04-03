import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Jeddah Property Scorecard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
  }

  .stApp {
    background: #0f1117;
    color: #e8e8e8;
  }

  .main-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #2a3550;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }

  .main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    border-radius: 50%;
  }

  .main-header h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #e2e8f0;
    margin: 0 0 0.3rem 0;
  }

  .main-header p {
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0;
    font-weight: 300;
  }

  .badge {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63b3ed;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-family: 'Syne', sans-serif;
  }

  .metric-card {
    background: #1e2535;
    border: 1px solid #2a3550;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
  }

  .metric-card .label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 4px;
  }

  .metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e2e8f0;
  }

  .metric-card .sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 2px;
  }

  .verdict-buy   { color: #4ade80; font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; }
  .verdict-hold  { color: #fbbf24; font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; }
  .verdict-avoid { color: #f87171; font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; }

  .rationale-box {
    background: #1a2035;
    border-left: 3px solid #63b3ed;
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: #cbd5e1;
    line-height: 1.6;
    margin-top: 1rem;
  }

  .source-note {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid #1e2535;
    font-style: italic;
  }

  .stSelectbox label, .stNumberInput label, .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  div[data-testid="stSidebar"] {
    background: #131720;
    border-right: 1px solid #1e2535;
  }

  .stButton > button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.8rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.04em;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .stButton > button:hover { opacity: 0.88; }

  .footer-note {
    text-align: center;
    color: #334155;
    font-size: 0.72rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1e2535;
  }
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────
DISTRICT_DATA = {
    'Al-Shati (Corniche)':       [5800, 7200, 7.8, 9.5, 4.0],
    'Al-Zahra':                  [5200, 6500, 7.5, 8.5, 3.5],
    'Al-Nahdah':                 [4800, 6000, 7.6, 8.0, 4.5],
    'Obhur Al-Shamaliyah':       [5500, 7000, 7.2, 8.8, 7.0],
    'Al-Murjan':                 [5300, 6800, 7.4, 8.6, 7.5],
    'Al-Basateen':               [4600, 5800, 8.0, 7.5, 6.5],
    'Jeddah Central Zone':       [5600, 7100, 8.2, 10.0, 5.0],
    'Al-Hamra':                  [5100, 6400, 7.9, 8.2, 3.0],
    'Al-Rawdah':                 [4400, 5600, 8.1, 7.0, 2.5],
    'Al-Salamah':                [4200, 5300, 8.3, 6.5, 2.0],
    'Al-Balad (Historic)':       [3800, 4900, 6.5, 7.8, 3.5],
    'Al-Faisaliyah':             [4000, 5100, 8.5, 6.0, 2.0],
    'Mishrifah':                 [3900, 5000, 8.6, 5.5, 2.5],
    'Al-Marwah':                 [4300, 5500, 8.2, 6.8, 3.0],
    'Al-Khalidiyah':             [4700, 5900, 7.7, 7.2, 3.5],
}

CITY_BENCHMARKS = {
    'apt_price_sqm': 4376, 'villa_price_sqm': 5114,
    'avg_yield': 7.89, 'apt_yoy_growth': 1.8,
    'villa_yoy_growth': 2.5, 'rental_yoy_apts': 4.7,
}

WEIGHTS = {'rental_yield': 0.40, 'price_value': 0.25, 'vision2030': 0.20, 'supply_risk': 0.15}

# ─── SCORING ENGINE ───────────────────────────────────────────────
def score_rental_yield(y, avg):
    r = y / avg
    if r >= 1.15: return 100
    elif r >= 1.05: return 85
    elif r >= 0.95: return 65
    elif r >= 0.85: return 45
    else: return 25

def score_price_value(psqm, bench):
    r = psqm / bench
    if r <= 0.90: return 100
    elif r <= 0.97: return 80
    elif r <= 1.03: return 60
    elif r <= 1.10: return 40
    else: return 20

def get_verdict(score):
    if score >= 72: return ('BUY', '🟢', 'Strong investment fundamentals. Yield above district average, favourable price positioning, and Vision 2030 tailwinds support capital appreciation.')
    elif score >= 52: return ('HOLD', '🟡', 'Adequate fundamentals with mixed signals. Consider negotiating price or waiting for a stronger entry point. Monitor supply pipeline.')
    else: return ('AVOID', '🔴', 'Weak risk-adjusted return. Price premium or below-average yield reduces margin of safety. Explore alternative districts.')

def evaluate(district, prop_type, size_sqm, price_sar, rent_sar):
    d = DISTRICT_DATA[district]
    bench = d[0] if prop_type == 'Apartment' else d[1]
    avg_yield, v2030, supply = d[2], d[3], d[4]
    psqm = price_sar / size_sqm
    gross_yield = (rent_sar * 12 / price_sar) * 100

    sy = score_rental_yield(gross_yield, avg_yield)
    sp = score_price_value(psqm, bench)
    sv = v2030 * 10
    ss = (10 - supply) * 10

    composite = sy*0.40 + sp*0.25 + sv*0.20 + ss*0.15
    verdict, icon, rationale = get_verdict(composite)

    city_bench = CITY_BENCHMARKS['apt_price_sqm'] if prop_type == 'Apartment' else CITY_BENCHMARKS['villa_price_sqm']

    return {
        'gross_yield': round(gross_yield, 2), 'avg_yield': avg_yield,
        'psqm': round(psqm), 'bench': bench, 'city_bench': city_bench,
        'vs_bench': round((psqm/bench - 1)*100, 1),
        'sy': sy, 'sp': sp, 'sv': sv, 'ss': ss,
        'composite': round(composite, 1),
        'verdict': verdict, 'icon': icon, 'rationale': rationale,
        'annual_rent': rent_sar * 12, 'v2030': v2030, 'supply': supply
    }

# ─── HEADER ───────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <span class="badge">Vision 2030</span>
  <span class="badge">KSA Real Estate</span>
  <span class="badge">REGA Data</span>
  <h1>🏙️ Jeddah Property Investment Scorecard</h1>
  <p>Evaluate residential properties against district benchmarks, rental yield, and Vision 2030 strategic alignment</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏠 Property Details")
    st.markdown("<hr style='border-color:#1e2535;margin:0.5rem 0 1rem'>", unsafe_allow_html=True)

    district = st.selectbox("District", list(DISTRICT_DATA.keys()), index=0)
    prop_type = st.radio("Property Type", ["Apartment", "Villa"], horizontal=True)
    size_sqm = st.number_input("Size (sqm)", min_value=30, max_value=2000, value=120, step=5)
    price_sar = st.number_input("Asking Price (SAR)", min_value=100_000, max_value=50_000_000, value=750_000, step=10_000)
    rent_sar = st.number_input("Expected Monthly Rent (SAR)", min_value=500, max_value=200_000, value=5_200, step=100)

    st.markdown("<br>", unsafe_allow_html=True)
    evaluate_btn = st.button("▶ Evaluate Property")

    st.markdown("---")
    st.markdown("**📊 Scoring Weights**")
    st.markdown("""
    <div style='font-size:0.78rem; color:#64748b; line-height:2'>
    Rental Yield &nbsp;&nbsp;&nbsp; 40%<br>
    Price Value &nbsp;&nbsp;&nbsp;&nbsp; 25%<br>
    Vision 2030 &nbsp;&nbsp;&nbsp;&nbsp; 20%<br>
    Supply Safety &nbsp; 15%
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#475569'>
    <b>Data Sources</b><br>
    Cavendish Maxwell H1 2025<br>
    JLL KSA Living Q2 2025<br>
    GAStat RE Price Index<br>
    Mordor Intelligence 2026
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN OUTPUT ─────────────────────────────────────────────────
r = evaluate(district, prop_type, size_sqm, price_sar, rent_sar)

verdict_class = {'BUY': 'verdict-buy', 'HOLD': 'verdict-hold', 'AVOID': 'verdict-avoid'}[r['verdict']]
verdict_colors = {'BUY': '#4ade80', 'HOLD': '#fbbf24', 'AVOID': '#f87171'}
vc = verdict_colors[r['verdict']]

# ── ROW 1: Verdict + Key Metrics ───────────────────────────────
col_v, col_m = st.columns([1, 3])

with col_v:
    st.markdown(f"""
    <div class="metric-card" style="text-align:center; padding: 2rem 1rem;">
      <div class="label">Investment Verdict</div>
      <div class="{verdict_class}">{r['icon']} {r['verdict']}</div>
      <div style="font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; color:{vc}; margin:0.5rem 0">
        {r['composite']}
      </div>
      <div style="color:#64748b; font-size:0.78rem">out of 100</div>
    </div>
    """, unsafe_allow_html=True)

with col_m:
    mc1, mc2, mc3, mc4 = st.columns(4)
    yield_color = '#4ade80' if r['gross_yield'] >= r['avg_yield'] else '#f87171'
    bench_color = '#4ade80' if r['vs_bench'] <= 0 else '#f87171'

    with mc1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">Gross Rental Yield</div>
          <div class="value" style="color:{yield_color}">{r['gross_yield']}%</div>
          <div class="sub">District avg: {r['avg_yield']}% | City: {CITY_BENCHMARKS['avg_yield']}%</div>
        </div>""", unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">Price / sqm</div>
          <div class="value">SAR {r['psqm']:,}</div>
          <div class="sub" style="color:{bench_color}">{r['vs_bench']:+.1f}% vs district avg (SAR {r['bench']:,})</div>
        </div>""", unsafe_allow_html=True)

    with mc3:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">Annual Rental Income</div>
          <div class="value">SAR {r['annual_rent']:,}</div>
          <div class="sub">SAR {rent_sar:,}/month</div>
        </div>""", unsafe_allow_html=True)

    with mc4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">Vision 2030 Score</div>
          <div class="value" style="color:#63b3ed">{r['v2030']}/10</div>
          <div class="sub">Supply risk: {r['supply']}/10</div>
        </div>""", unsafe_allow_html=True)

# Rationale
st.markdown(f"""
<div class="rationale-box">
  📋 <strong>Analyst Note:</strong> {r['rationale']}
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ROW 2: Charts ────────────────────────────────────────────────
chart_bg = '#1e2535'
axis_color = '#475569'
grid_color = '#2a3550'
text_color = '#94a3b8'

tab1, tab2, tab3 = st.tabs(["📊 Scorecard", "🗺️ District Matrix", "📈 Market Benchmarks"])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode='gauge+number',
            value=r['composite'],
            title={'text': 'Investment Score', 'font': {'color': text_color, 'size': 14, 'family': 'Syne'}},
            number={'font': {'color': vc, 'size': 40, 'family': 'Syne'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': axis_color, 'tickfont': {'color': axis_color}},
                'bar': {'color': vc, 'thickness': 0.25},
                'bgcolor': chart_bg,
                'bordercolor': grid_color,
                'steps': [
                    {'range': [0, 52],  'color': '#2d1b1b'},
                    {'range': [52, 72], 'color': '#2d2510'},
                    {'range': [72, 100],'color': '#1a2d1a'},
                ],
            }
        ))
        fig_gauge.update_layout(
            height=280, paper_bgcolor=chart_bg,
            font={'color': text_color},
            margin=dict(t=50, b=10, l=30, r=30)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with c2:
        # Score breakdown
        dims   = ['Rental Yield', 'Price Value', 'Vision 2030', 'Supply Safety']
        scores = [r['sy'], r['sp'], r['sv'], r['ss']]
        bar_colors = ['#4ade80' if s >= 65 else '#fbbf24' if s >= 45 else '#f87171' for s in scores]

        fig_bar = go.Figure(go.Bar(
            x=dims, y=scores, marker_color=bar_colors,
            text=[f'{s:.0f}' for s in scores], textposition='outside',
            textfont={'color': text_color}
        ))
        fig_bar.update_layout(
            title={'text': 'Score by Dimension', 'font': {'color': text_color, 'family': 'Syne', 'size': 14}},
            height=280, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
            yaxis=dict(range=[0, 120], gridcolor=grid_color, tickfont={'color': axis_color}),
            xaxis=dict(tickfont={'color': axis_color}),
            margin=dict(t=50, b=10, l=20, r=20), showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig_price = go.Figure(go.Bar(
            x=['This Property', 'District Avg', 'City Avg'],
            y=[r['psqm'], r['bench'], r['city_bench']],
            marker_color=['#a78bfa', '#3b82f6', '#475569'],
            text=[f'SAR {v:,}' for v in [r['psqm'], r['bench'], r['city_bench']]],
            textposition='outside', textfont={'color': text_color}
        ))
        fig_price.update_layout(
            title={'text': 'Price / sqm Comparison', 'font': {'color': text_color, 'family': 'Syne', 'size': 14}},
            height=260, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
            yaxis=dict(gridcolor=grid_color, tickfont={'color': axis_color}, tickprefix='SAR '),
            xaxis=dict(tickfont={'color': axis_color}),
            margin=dict(t=50, b=10), showlegend=False
        )
        st.plotly_chart(fig_price, use_container_width=True)

    with c4:
        fig_yield = go.Figure(go.Bar(
            x=['This Property', 'District Avg', 'City Avg'],
            y=[r['gross_yield'], r['avg_yield'], CITY_BENCHMARKS['avg_yield']],
            marker_color=['#4ade80', '#3b82f6', '#475569'],
            text=[f"{v:.2f}%" for v in [r['gross_yield'], r['avg_yield'], CITY_BENCHMARKS['avg_yield']]],
            textposition='outside', textfont={'color': text_color}
        ))
        fig_yield.update_layout(
            title={'text': 'Rental Yield Comparison', 'font': {'color': text_color, 'family': 'Syne', 'size': 14}},
            height=260, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
            yaxis=dict(gridcolor=grid_color, tickfont={'color': axis_color}, ticksuffix='%', range=[0, 12]),
            xaxis=dict(tickfont={'color': axis_color}),
            margin=dict(t=50, b=10), showlegend=False
        )
        st.plotly_chart(fig_yield, use_container_width=True)

with tab2:
    pt_key = 'apt' if prop_type == 'Apartment' else 'villa'
    idx = 0 if prop_type == 'Apartment' else 1

    dists, yields, v2030s, prices, supplies = [], [], [], [], []
    for d, vals in DISTRICT_DATA.items():
        dists.append(d)
        prices.append(vals[idx])
        yields.append(vals[2])
        v2030s.append(vals[3])
        supplies.append(vals[4])

    fig_bubble = px.scatter(
        x=yields, y=v2030s, size=prices, color=supplies,
        color_continuous_scale='RdYlGn_r',
        text=dists,
        labels={'x': 'Avg Gross Yield (%)', 'y': 'Vision 2030 Score', 'color': 'Supply Risk', 'size': 'Price/sqm'},
        title='Jeddah District Matrix — Yield vs Vision 2030 Alignment',
        height=520
    )
    fig_bubble.update_traces(
        textposition='top center',
        textfont={'color': '#cbd5e1', 'size': 9, 'family': 'DM Sans'},
        marker={'line': {'color': '#2a3550', 'width': 1}}
    )
    # Highlight selected district
    if district in dists:
        i = dists.index(district)
        fig_bubble.add_trace(go.Scatter(
            x=[yields[i]], y=[v2030s[i]],
            mode='markers',
            marker={'size': 22, 'color': 'rgba(0,0,0,0)', 'line': {'color': vc, 'width': 3}},
            showlegend=False, name='Selected'
        ))

    fig_bubble.add_hline(y=7.5, line_dash='dash', line_color='#475569', opacity=0.5)
    fig_bubble.add_vline(x=7.9, line_dash='dash', line_color='#475569', opacity=0.5)
    fig_bubble.add_annotation(x=8.5, y=9.8, text='⭐ High Yield + High V2030', showarrow=False,
                               font=dict(color='#4ade80', size=10, family='Syne'))
    fig_bubble.update_layout(
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        font={'color': text_color},
        xaxis=dict(gridcolor=grid_color, tickfont={'color': axis_color}),
        yaxis=dict(gridcolor=grid_color, tickfont={'color': axis_color}),
        coloraxis_colorbar=dict(tickfont={'color': text_color}, title={'font': {'color': text_color}})
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

with tab3:
    # All districts ranked
    all_r = []
    for d in DISTRICT_DATA:
        vals = DISTRICT_DATA[d]
        bench = vals[0] if prop_type == 'Apartment' else vals[1]
        all_r.append({'District': d, 'Yield %': vals[2], 'V2030': vals[3],
                      'Supply Risk': vals[4], 'Price/sqm': bench})

    df_all = pd.DataFrame(all_r).sort_values('Yield %', ascending=True)

    fig_rank = go.Figure()
    fig_rank.add_trace(go.Bar(
        y=df_all['District'], x=df_all['Yield %'],
        orientation='h',
        marker_color=['#3b82f6' if d == district else '#2a3550' for d in df_all['District']],
        text=[f"{v:.1f}%" for v in df_all['Yield %']],
        textposition='outside', textfont={'color': text_color}
    ))
    fig_rank.add_vline(x=CITY_BENCHMARKS['avg_yield'], line_dash='dash', line_color='#fbbf24',
                       annotation_text=f"City avg {CITY_BENCHMARKS['avg_yield']}%",
                       annotation_font_color='#fbbf24')
    fig_rank.update_layout(
        title={'text': 'Gross Rental Yield by District', 'font': {'color': text_color, 'family': 'Syne', 'size': 14}},
        height=480, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        xaxis=dict(gridcolor=grid_color, tickfont={'color': axis_color}, ticksuffix='%'),
        yaxis=dict(tickfont={'color': axis_color, 'size': 10}),
        margin=dict(l=10, r=60), showlegend=False
    )
    st.plotly_chart(fig_rank, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────
st.markdown("""
<div class="source-note">
  Data Sources: Cavendish Maxwell KSA Residential Market H1 2025 · JLL KSA Living Market Dynamics Q2 2025 ·
  GAStat Real Estate Price Index Q4 2025 · Mordor Intelligence Jeddah Commercial RE Report Jan 2026 ·
  Global Property Guide Q1 2026 · REGA / Ejar Platform.<br>
  ⚠️ For informational purposes only. Not financial advice. Benchmarks sourced from publicly available market research.
</div>
""", unsafe_allow_html=True)
