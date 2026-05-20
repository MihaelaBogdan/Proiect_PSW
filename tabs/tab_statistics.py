"""
tab_statistics.py — Grupări, Agregări și Statistici Deschise
"""
import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("# 📊 Statistici Descriptive & Grupări")
    
    if "processed_data" not in st.session_state:
        st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
        return
        
    df = st.session_state.processed_data
    
    st.subheader("1. Agregări de date cu Pandas (groupby)")
    st.write("Calculăm media popularității și a energiei pentru fiecare gen muzical.")
    
    # Utilizarea funcțiilor de grup
    grouped_df = df.groupby('genre').agg(
        Popularitate_Medie=('popularity', 'mean'),
        Energie_Medie=('energy', 'mean'),
        Numar_Piese=('track_id', 'count')
    ).reset_index().sort_values(by='Popularitate_Medie', ascending=False)
    
    st.dataframe(grouped_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Reprezentare Grafică: Popularitate Medie per Gen")
        fig1 = px.bar(grouped_df, x='genre', y='Popularitate_Medie', color='genre', template="plotly_dark")
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.write("Reprezentare Grafică: Energie Medie per Gen")
        fig2 = px.bar(grouped_df, x='genre', y='Energie_Medie', color='genre', template="plotly_dark")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
