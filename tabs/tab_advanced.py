"""
tab_advanced.py — Analiză Avansată: Vizualizare PCA, Outlier Detection, Regresie Avansată
Cerințe acoperite:
 - și altele (scikit-learn: PCA, IsolationForest)
 - vizualizări suplimentare Streamlit
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def render():
  st.markdown("# Analiză Avansată")

  if "processed_data" not in st.session_state:
    st.warning(" Te rog să rulezi mai întâi **Preprocesarea Datelor** (tab-ul )!")
    return

  df = st.session_state.processed_data.copy()
  audio_feats = ["danceability", "energy", "valence", "tempo",
          "acousticness", "instrumentalness", "speechiness", "liveness"]

  # ── 1. PCA 2D ─────────────────────────────────────────────────────────────
  st.subheader("1. Reducerea dimensionalității — PCA 2D")
  st.write("Reducem cele 8 caracteristici audio la **2 componente principale** cu `sklearn.decomposition.PCA` "
       "pentru a vizualiza spațiul muzical.")

  X = df[audio_feats].dropna()
  sc = StandardScaler()
  X_scaled = sc.fit_transform(X)

  pca = PCA(n_components=2)
  components = pca.fit_transform(X_scaled)
  var_exp = pca.explained_variance_ratio_

  df_pca = df.loc[X.index].copy()
  df_pca["PC1"] = components[:, 0]
  df_pca["PC2"] = components[:, 1]

  fig_pca = px.scatter(
    df_pca, x="PC1", y="PC2", color="genre",
    hover_data=["track_name", "artist_name", "popularity"],
    title=f"PCA 2D — Varianta explicată: PC1={var_exp[0]:.1%}, PC2={var_exp[1]:.1%}",
    template="plotly_dark", opacity=0.7,
  )
  st.plotly_chart(fig_pca, use_container_width=True)

  st.info(f" PCA explică **{sum(var_exp):.1%}** din varianța totală cu doar 2 componente.")

  # ── 2. Loadings PCA ───────────────────────────────────────────────────────
  st.subheader("2. Contribuția variabilelor la componentele principale (Loadings)")
  loadings = pd.DataFrame(
    pca.components_.T,
    index=audio_feats,
    columns=["PC1", "PC2"]
  ).round(3)
  fig_load = px.bar(loadings, barmode="group",
           title="PCA Loadings — Contribuția fiecărei caracteristici",
           template="plotly_dark", color_discrete_sequence=["#1db954", "#e91e63"])
  st.plotly_chart(fig_load, use_container_width=True)
  st.dataframe(loadings, use_container_width=True)

  # ── 3. Detecție Outliers (Isolation Forest) ───────────────────────────────
  st.subheader("3. Detecție automată a Outlierilor — Isolation Forest")
  st.write("Folosim `IsolationForest` din scikit-learn pentru a identifica piesele "
       "cu caracteristici audio atipice (anomalii).")

  contamination = st.slider("Proporție estimată de outlieri:", 0.01, 0.15, 0.05, 0.01)
  iso = IsolationForest(contamination=contamination, random_state=42)
  df_pca["outlier"] = iso.fit_predict(X_scaled)
  df_pca["tip"] = df_pca["outlier"].map({1: "Normal", -1: "Outlier"})

  n_out = (df_pca["outlier"] == -1).sum()
  st.metric("Outlieri detectați", n_out, f"{n_out/len(df_pca):.1%} din date")

  fig_out = px.scatter(
    df_pca, x="PC1", y="PC2", color="tip",
    color_discrete_map={"Normal": "#1db954", "Outlier": "#e91e63"},
    hover_data=["track_name", "artist_name", "genre"],
    title="Outlieri detectați cu Isolation Forest (spațiu PCA)",
    template="plotly_dark", opacity=0.7,
  )
  st.plotly_chart(fig_out, use_container_width=True)

  st.subheader("Piesele outlier identificate")
  outliers_df = df_pca[df_pca["outlier"] == -1][
    ["track_name", "artist_name", "genre", "popularity",
     "tempo", "loudness", "instrumentalness"]
  ].head(20)
  st.dataframe(outliers_df, use_container_width=True)

  # ── 4. Violinplot popularitate ────────────────────────────────────────────
  st.subheader("4. Distribuție popularitate per gen — Violin Plot")
  fig_vio = px.violin(
    df, x="genre", y="popularity", color="genre",
    box=True, points="outliers",
    title="Violin Plot: Distribuția popularității per gen muzical",
    template="plotly_dark",
  )
  fig_vio.update_layout(showlegend=False, xaxis_tickangle=-30)
  st.plotly_chart(fig_vio, use_container_width=True)

  # ── 5. Scatter matrix ─────────────────────────────────────────────────────
  st.subheader("5. Scatter Matrix (Pair Plot) — relații între variabile")
  cols_sel = st.multiselect(
    "Selectează variabilele pentru scatter matrix:",
    audio_feats + ["popularity"],
    default=["danceability", "energy", "valence", "popularity"],
  )
  if len(cols_sel) >= 2:
    fig_scat = px.scatter_matrix(
      df.sample(min(500, len(df)), random_state=42),
      dimensions=cols_sel, color="genre",
      title="Scatter Matrix — caracteristici audio",
      template="plotly_dark",
      opacity=0.5,
    )
    fig_scat.update_layout(height=600)
    st.plotly_chart(fig_scat, use_container_width=True)
