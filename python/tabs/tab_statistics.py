"""
tab_statistics.py — Statistici Descriptive, Grupări, Agregări, Corelații
Cerințe acoperite:
 - prelucrări statistice cu pandas
 - funcții de grup (groupby, agg, transform)
 - vizualizări Streamlit (heatmap, boxplot, histogram)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


def render():
  st.markdown("# Statistici Descriptive & Grupări")

  if "processed_data" not in st.session_state:
    st.warning(" Te rog să rulezi mai întâi **Preprocesarea Datelor** (tab-ul )!")
    return

  df = st.session_state.processed_data.copy()

  # ── 1. describe() ────────────────────────────────────────────────────────
  st.subheader("1. Statistici descriptive generale (pandas describe)")
  numeric_cols = ["popularity", "danceability", "energy", "valence",
          "tempo", "acousticness", "instrumentalness",
          "speechiness", "liveness", "loudness", "duration_min"]
  desc = df[numeric_cols].describe().round(4)
  st.dataframe(desc.style.background_gradient(cmap="Greens"), use_container_width=True)
  st.caption("Rândurile arată: count, mean, std, min, 25%, 50%, 75%, max pentru fiecare coloană numerică.")

  # ── 2. groupby + agg ─────────────────────────────────────────────────────
  st.subheader("2. Agregări cu pandas groupby")
  st.write("Calculăm mai multe statistici agregate pentru fiecare gen muzical, "
       "utilizând funcțiile de grup: `mean`, `median`, `std`, `count`, `min`, `max`.")

  grouped = df.groupby("genre").agg(
    Popularitate_Medie = ("popularity",    "mean"),
    Popularitate_Mediana= ("popularity",    "median"),
    Energie_Medie    = ("energy",      "mean"),
    Dansabilitate_Medie = ("danceability",   "mean"),
    Valenta_Medie    = ("valence",      "mean"),
    Tempo_Mediu     = ("tempo",       "mean"),
    Durata_Medie_min  = ("duration_min",   "mean"),
    Nr_Piese      = ("track_id",     "count"),
    Nr_Artisti_Unici  = ("artist_name",    "nunique"),
    Explicit_Procent  = ("explicit",     "mean"),
  ).reset_index().sort_values("Popularitate_Medie", ascending=False).round(3)

  st.dataframe(grouped, use_container_width=True)

  col1, col2 = st.columns(2)
  with col1:
    fig = px.bar(grouped, x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}, y="Popularitate_Medie",
           color="genre", text_auto=".1f",
           title="Popularitate Medie per Gen",
           template="plotly_dark")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    fig2 = px.scatter(grouped, x="Energie_Medie", y="Popularitate_Medie",
             size="Nr_Piese", color="genre",
             text="genre", title="Energie vs. Popularitate (per Gen)",
             template="plotly_dark")
    fig2.update_traces(textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)

  # ── 3. transform — popularitate relativă ─────────────────────────────────
  st.subheader("3. Funcția transform — Popularitate relativă față de media genului")
  st.write("Folosim `groupby().transform('mean')` pentru a calcula cât de populară "
       "este fiecare piesă față de media genului ei.")
  df["pop_medie_gen"] = df.groupby("genre")["popularity"].transform("mean")
  df["pop_relativa"] = (df["popularity"] - df["pop_medie_gen"]).round(2)

  top_relative = df[["track_name", "artist_name", "genre",
            "popularity", "pop_medie_gen", "pop_relativa"]]\
    .sort_values("pop_relativa", ascending=False).head(10)
  st.dataframe(top_relative, use_container_width=True)
  st.caption("pop_relativa > 0 = piesa e mai populară decât media genului ei.")

  # ── 4. Distribuții ────────────────────────────────────────────────────────
  st.subheader("4. Distribuții ale variabilelor audio")
  feat_sel = st.selectbox("Alege caracteristica:", 
              ["popularity", "danceability", "energy", "valence",
               "tempo", "acousticness", "speechiness", "liveness"])
  col3, col4 = st.columns(2)
  with col3:
    fig_hist = px.histogram(df, x=feat_sel, nbins=50, color_discrete_sequence=["#1db954"],
                title=f"Histogramă: {feat_sel}", template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)
  with col4:
    fig_box = px.box(df, x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}, y=feat_sel, color="genre",
             title=f"Boxplot: {feat_sel} per gen",
             template="plotly_dark")
    fig_box.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

  # ── 5. Matrice de corelație ───────────────────────────────────────────────
  st.subheader("5. Matrice de corelație (Pearson)")
  st.write("Corelațiile dintre caracteristicile audio — `df.corr()` cu pandas.")
  corr_cols = ["popularity", "danceability", "energy", "valence",
         "tempo", "acousticness", "instrumentalness",
         "speechiness", "liveness", "loudness"]
  corr_matrix = df[corr_cols].corr().round(3)

  fig_heat = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Heatmap Corelație Pearson",
    template="plotly_dark",
    aspect="auto"
  )
  fig_heat.update_layout(height=500)
  st.plotly_chart(fig_heat, use_container_width=True)

  # ── 6. Top artiști ────────────────────────────────────────────────────────
  st.subheader("6. Top 15 artiști după popularitate medie")
  top_artists = (
    df.groupby("artist_name")
     .agg(Pop_Medie=("popularity", "mean"),
        Nr_Piese=("track_id", "count"))
     .query("Nr_Piese >= 3")
     .sort_values("Pop_Medie", ascending=False)
     .head(15)
     .reset_index()
     .round(1)
  )
  fig_art = px.bar(top_artists, x="Pop_Medie", y="artist_name",
           orientation="h", color="Pop_Medie",
           color_continuous_scale="Greens",
           text="Pop_Medie",
           title="Top 15 Artiști (min. 3 piese)",
           template="plotly_dark")
  fig_art.update_layout(yaxis=dict(categoryorder="total ascending"), showlegend=False)
  st.plotly_chart(fig_art, use_container_width=True)

  # ── 7. Evoluție popularitate în timp ──────────────────────────────────────
  st.subheader("7. Evoluția popularității în timp (deceniu)")
  df["decade"] = (df["year"] // 10) * 10
  trend = df.groupby(["decade", "genre"])["popularity"].mean().reset_index()
  genres_sel = st.multiselect("Filtrează genuri:", sorted(df["genre"].unique()),
                default=["pop", "rock", "hip-hop", "electronic"])
  trend_filtered = trend[trend["genre"].isin(genres_sel)]
  fig_trend = px.line(trend_filtered, x="decade", y="popularity", color="genre",
            markers=True, title="Popularitate Medie per Deceniu",
            template="plotly_dark")
  st.plotly_chart(fig_trend, use_container_width=True)
