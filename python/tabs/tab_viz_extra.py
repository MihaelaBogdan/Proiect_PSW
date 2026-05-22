"""
tab_viz_extra.py - Vizualizari Avansate (3D, Sunburst, Treemap)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render():
    st.markdown("# Vizualizări Avansate și Interactive")

    if "processed_data" not in st.session_state:
        st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
        return

    df = st.session_state.processed_data.copy()

    # Creăm decenii pentru vizualizări ierarhice dacă nu există
    if 'decade' not in df.columns:
        df['decade'] = (df['year'] // 10) * 10

    # --- 1. Treemap (Harta Ierarhică a Genurilor) ---
    st.subheader("1. Treemap: Structura Genurilor și Popularitatea")
    st.write("Mărimea dreptunghiului reprezintă numărul de piese, iar culoarea indică popularitatea medie.")
    
    treemap_data = df.groupby('genre').agg(
        Număr_Piese=('track_id', 'count'),
        Popularitate_Medie=('popularity', 'mean')
    ).reset_index()

    fig_tree = px.treemap(treemap_data, 
                          path=['genre'], 
                          values='Număr_Piese',
                          color='Popularitate_Medie', 
                          color_continuous_scale='Viridis',
                          title="Treemap Genuri Muzicale",
                          labels={"genre": "Gen Muzical", "Număr_Piese": "Număr Piese", "Popularitate_Medie": "Popularitate Medie"})
    st.plotly_chart(fig_tree, use_container_width=True)


    # --- 2. Sunburst Chart ---
    st.subheader("2. Sunburst Chart: Evoluția Ierarhică (Deceniu  Gen  Explicit)")
    st.write("Navighează ierarhic dând click pe componentele cercului pentru a explora structura datelor.")
    
    # Filtram pentru claritate
    sunburst_df = df[df['genre'].isin(df['genre'].value_counts().head(8).index)]
    sunburst_df['Explicit_Label'] = sunburst_df['explicit'].map({1: 'Explicit', 0: 'Curat'})
    
    fig_sunburst = px.sunburst(sunburst_df, 
                               path=['decade', 'genre', 'Explicit_Label'], 
                               values='popularity',
                               color='energy', 
                               color_continuous_scale='RdBu_r',
                               title="Sunburst: Distribuția Popularității și Energiei",
                               labels={"decade": "Deceniu", "genre": "Gen Muzical", "energy": "Energie"})
    st.plotly_chart(fig_sunburst, use_container_width=True)


    # --- 3. Scatter 3D Interactiv ---
    st.subheader("3. Scatter Plot 3D: Exploram spațiul 3D al muzicii")
    st.write("Analizăm modul în care 3 variabile principale interacționează în spațiu tridimensional.")
    
    # Luăm un eșantion pentru performanță
    sample_df = df.sample(n=min(1000, len(df)), random_state=42)
    
    fig_3d = px.scatter_3d(sample_df, 
                           x='danceability', 
                           y='energy', 
                           z='popularity',
                           color='genre',
                           hover_name='track_name',
                           title="3D Scatter: Dansabilitate vs Energie vs Popularitate",
                           labels={"danceability": "Dansabilitate", "energy": "Energie", "popularity": "Popularitate", "genre": "Gen Muzical"},
                           opacity=0.7)
    fig_3d.update_layout(scene=dict(bgcolor='#0a0a0f'), template="plotly_dark")
    st.plotly_chart(fig_3d, use_container_width=True)


    # --- 4. Density Contour (Harta Topografică 2D) ---
    st.subheader("4. Density Contour: Harta de Densitate 2D (Tempo vs Energie)")
    st.write("Arată zonele de concentrare maximă a pieselor, similar cu o hartă topografică.")
    
    fig_contour = px.density_contour(df, 
                                     x="tempo", 
                                     y="energy", 
                                     color="genre",
                                     title="Densitate 2D: Unde se concentrează genurile?",
                                     labels={"tempo": "Tempo (BPM)", "energy": "Energie", "genre": "Gen Muzical"})
    fig_contour.update_traces(contours_coloring="fill", contours_showlabels=True)
    st.plotly_chart(fig_contour, use_container_width=True)


    # --- 5. Polar/Radar Chart (Top Artiști) ---
    st.subheader("5. Polar Radar Chart: Profilul Acustic al Top 3 Artiști")
    st.write("Comparăm semnătura acustică (amprenta muzicală) a celor mai populari artiști.")
    
    top_artists = df.groupby('artist_name')['popularity'].mean().nlargest(3).index
    artist_df = df[df['artist_name'].isin(top_artists)]
    
    metrics = ['danceability', 'energy', 'valence', 'acousticness', 'liveness', 'speechiness']
    artist_means = artist_df.groupby('artist_name')[metrics].mean().reset_index()

    fig_radar = go.Figure()
    for i, row in artist_means.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[metrics].values.tolist() + [row[metrics].values.tolist()[0]], # close the polygon
            theta=[m.capitalize() for m in metrics] + [metrics[0].capitalize()],
            fill='toself',
            name=row['artist_name']
        ))
        
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Amprenta Acustică (Radar Chart)",
        template="plotly_dark"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
