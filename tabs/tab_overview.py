"""
tabs/tab_overview.py — Pagina 1: Prezentare generală a dataset-ului
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data, GENRE_COLORS


def render():
  df = load_data()

  st.markdown("# Spotify Tracks — Prezentare Generală")
  st.markdown(
    "Analiză completă a unui dataset cu **5.000 de piese Spotify** cuprinzând "
    "15 genuri muzicale, caracteristici audio și metadate de popularitate."
  )

  # ── KPI Cards ────────────────────────────────────────────────────────────
  c1, c2, c3, c4, c5 = st.columns(5)
  kpis = [
    (c1, len(df), "Piese totale"),
    (c2, df["genre"].nunique(), "Genuri"),
    (c3, df["artist_name"].nunique(), "Artiști"),
    (c4, f"{df['year'].min()}–{df['year'].max()}", "Interval ani"),
    (c5, f"{df['popularity'].mean():.1f}", "Popularitate medie"),
  ]
  for col, val, label in kpis:
    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{val}</div>
      <div class='metric-label'>{label}</div>
    </div>
    """, unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)

  # ── Row 1: Distribuție genuri + Timeline ─────────────────────────────────
  col1, col2 = st.columns(2)

  with col1:
    st.markdown("<div class='section-header'>Distribuție pe genuri</div>", unsafe_allow_html=True)
    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["genre", "count"]
    fig_genre = px.bar(
      genre_counts,
      x="count", y="genre",
      orientation="h",
      color="genre",
      color_discrete_map=GENRE_COLORS,
      text="count",
      template="plotly_dark",
    )
    fig_genre.update_traces(textposition="outside")
    fig_genre.update_layout(
      showlegend=False,
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      height=420,
      yaxis=dict(categoryorder="total ascending"),
      margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_genre, use_container_width=True)

  with col2:
    st.markdown("<div class='section-header'>Piese lansate per deceniu</div>", unsafe_allow_html=True)
    df["decade"] = (df["year"] // 10) * 10
    decade_genre = df.groupby(["decade", "genre"]).size().reset_index(name="count")
    fig_time = px.area(
      decade_genre,
      x="decade", y="count", color="genre",
      color_discrete_map=GENRE_COLORS,
      template="plotly_dark",
    )
    fig_time.update_layout(
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      height=420,
      legend=dict(orientation="h", y=-0.25, x=0),
      margin=dict(l=20, r=20, t=20, b=60),
    )
    st.plotly_chart(fig_time, use_container_width=True)

  # ── Row 2: Popularitate + Radar ──────────────────────────────────────────
  col3, col4 = st.columns(2)

  with col3:
    st.markdown("<div class='section-header'>Popularitate medie per gen</div>", unsafe_allow_html=True)
    pop_genre = df.groupby("genre")["popularity"].mean().reset_index().sort_values("popularity", ascending=False)
    fig_pop = px.funnel(
      pop_genre,
      x="popularity", y="genre",
      color="genre",
      color_discrete_map=GENRE_COLORS,
      template="plotly_dark",
    )
    fig_pop.update_layout(
      showlegend=False,
      plot_bgcolor="rgba(0,0,0,0)",
      paper_bgcolor="rgba(0,0,0,0)",
      height=420,
      margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_pop, use_container_width=True)

  with col4:
    st.markdown("<div class='section-header'>Profil audio mediu per gen</div>", unsafe_allow_html=True)
    radar_feats = ["danceability", "energy", "valence", "acousticness", "liveness", "speechiness"]
    genre_sel = st.multiselect(
      "Selectați genuri pentru radar:",
      options=sorted(df["genre"].unique()),
      default=["pop", "rock", "jazz", "electronic"],
      key="radar_genres",
    )
    if genre_sel:
      fig_radar = go.Figure()
      for g in genre_sel:
        vals = df[df["genre"] == g][radar_feats].mean().tolist()
        vals += [vals[0]]
        fig_radar.add_trace(go.Scatterpolar(
          r=vals,
          theta=radar_feats + [radar_feats[0]],
          fill="toself",
          name=g,
          line_color=GENRE_COLORS.get(g, "#ffffff"),
          opacity=0.7,
        ))
      fig_radar.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
              radialaxis=dict(visible=True, range=[0, 1], color="#666")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        height=420,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
      )
      st.plotly_chart(fig_radar, use_container_width=True)

  # ── Dataset Preview ───────────────────────────────────────────────────────
  st.markdown("<div class='section-header'>Preview Dataset</div>", unsafe_allow_html=True)
  col_search, col_filter = st.columns([3, 1])
  with col_search:
    search = st.text_input(" Caută artist sau piesă:", placeholder="Ex: Taylor Swift")
  with col_filter:
    genre_filter = st.selectbox("Filtrează gen:", ["Toate"] + sorted(df["genre"].unique()))

  df_view = df.copy()
  if search:
    mask = (df_view["artist_name"].str.contains(search, case=False, na=False) |
        df_view["track_name"].str.contains(search, case=False, na=False))
    df_view = df_view[mask]
  if genre_filter != "Toate":
    df_view = df_view[df_view["genre"] == genre_filter]

  display_cols = ["track_name", "artist_name", "genre", "year", "popularity",
          "danceability", "energy", "valence", "tempo", "duration_min"]
  st.dataframe(
    df_view[display_cols].rename(columns={
      "track_name": "Piesă", "artist_name": "Artist", "genre": "Gen",
      "year": "An", "popularity": "Popularitate", "danceability": "Dansabilitate",
      "energy": "Energie", "valence": "Valență", "tempo": "Tempo (BPM)",
      "duration_min": "Durată (min)"
    }).style.format({
      "Popularitate": "{:.0f}",
      "Dansabilitate": "{:.3f}", "Energie": "{:.3f}",
      "Valență": "{:.3f}", "Tempo (BPM)": "{:.1f}",
      "Durată (min)": "{:.2f}",
    }).background_gradient(subset=["Popularitate"], cmap="Greens"),
    use_container_width=True,
    height=350,
  )
  st.caption(f" {len(df_view):,} piese afișate din {len(df):,} total")

  # ── Structura dataset ─────────────────────────────────────────────────────
  with st.expander(" Structura completă a dataset-ului"):
    col_info = pd.DataFrame({
      "Coloană": df.columns,
      "Tip date": df.dtypes.astype(str).values,
      "Valori lipsă": df.isnull().sum().values,
      "Valori unice": [df[c].nunique() for c in df.columns],
      "Exemplu": [str(df[c].iloc[0]) for c in df.columns],
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)
