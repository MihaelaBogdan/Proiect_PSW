"""
app.py — Spotify Tracks Analysis Dashboard
==========================================
Aplicație Streamlit multi-pagină pentru analiza platformei Spotify.
Rulați cu:  streamlit run app.py
"""

import streamlit as st

# ── Configurare pagină (trebuie să fie prima comandă Streamlit) ─────────────
st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizat ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #0d0d0d 0%, #1a1a2e 100%);
  }
  [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
  [data-testid="stSidebar"] .stRadio label { font-size: 15px; }

  /* Main background */
  .stApp { background: #0a0a0f; color: #e8e8f0; }

  /* Cards */
  .metric-card {
      background: linear-gradient(135deg, #1e1e2e 0%, #252540 100%);
      border: 1px solid rgba(29,185,84,0.3);
      border-radius: 16px;
      padding: 20px 24px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(29,185,84,0.08);
      transition: transform 0.2s, box-shadow 0.2s;
  }
  .metric-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 30px rgba(29,185,84,0.18);
  }
  .metric-value {
      font-size: 2.2rem; font-weight: 700;
      background: linear-gradient(90deg, #1db954, #1ed760);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .metric-label { font-size: 0.85rem; color: #a0a0b0; margin-top: 6px; text-transform: uppercase; letter-spacing: 1px; }

  /* Section header */
  .section-header {
      font-size: 1.5rem; font-weight: 600;
      color: #1db954;
      border-left: 4px solid #1db954;
      padding-left: 12px; margin: 24px 0 16px;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab"] {
      background: #1a1a2e; border-radius: 8px 8px 0 0;
      color: #a0a0b0; font-weight: 500;
  }
  .stTabs [aria-selected="true"] {
      background: linear-gradient(90deg,#1db954,#1ed760) !important;
      color: #000 !important;
  }

  /* DataFrame */
  .dataframe { font-size: 13px; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0a0f; }
  ::-webkit-scrollbar-thumb { background: #1db954; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Importuri module ─────────────────────────────────────────────────────────
from tabs import (
    tab_overview,
    tab_preprocessing,
    tab_statistics,
    tab_clustering,
    tab_regression,
    tab_classification,
    tab_advanced,
)

# ── Sidebar navigation ───────────────────────────────────────────────────────
st.sidebar.markdown("## 🎵 Spotify Analytics")
st.sidebar.markdown("---")

PAGES = {
    "🏠  Overview & Date":          "overview",
    "🔧  Preprocesare Date":         "preprocessing",
    "📊  Statistici Descriptive":    "statistics",
    "🔵  Clustering (K-Means)":      "clustering",
    "📈  Regresie Multiplă":         "regression",
    "🤖  Clasificare (Logistic)":    "classification",
    "🌐  Analiză Avansată":          "advanced",
}

page_label = st.sidebar.radio("Navigare", list(PAGES.keys()))
page = PAGES[page_label]

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:12px; color:#666; text-align:center; padding:10px;'>
Proiect Analiză Date<br>
Spotify Tracks Dataset<br>
<span style='color:#1db954'>Python • Streamlit • ML</span>
</div>
""", unsafe_allow_html=True)

# ── Rutare pagini ─────────────────────────────────────────────────────────────
if page == "overview":
    tab_overview.render()
elif page == "preprocessing":
    tab_preprocessing.render()
elif page == "statistics":
    tab_statistics.render()
elif page == "clustering":
    tab_clustering.render()
elif page == "regression":
    tab_regression.render()
elif page == "classification":
    tab_classification.render()
elif page == "advanced":
    tab_advanced.render()
