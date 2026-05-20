"""
tab_clustering.py — Clusterizare cu Scikit-Learn
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def render():
    st.markdown("# 🔵 Clusterizare (K-Means)")
    
    if "processed_data" not in st.session_state:
        st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
        return
        
    df = st.session_state.processed_data
    
    st.write("Vom grupa piesele în clustere folosind caracteristici audio.")
    
    features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
    X = df[features]
    
    n_clusters = st.slider("Număr de clustere (K)", min_value=2, max_value=10, value=4)
    
    if st.button("Rulează K-Means"):
        with st.spinner("Antrenare model K-Means..."):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            df['Cluster'] = kmeans.fit_predict(X)
            
            # Reducem la 2 dimensiuni pentru vizualizare
            pca = PCA(n_components=2)
            pca_components = pca.fit_transform(X)
            
            df['PCA1'] = pca_components[:, 0]
            df['PCA2'] = pca_components[:, 1]
            
            st.success("Clusterizare completă!")
            
            fig = px.scatter(df, x='PCA1', y='PCA2', color=df['Cluster'].astype(str),
                             hover_data=['track_name', 'artist_name', 'genre'],
                             template="plotly_dark", title="Vizualizare Clustere (PCA)")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Caracteristicile mediilor pe fiecare cluster")
            cluster_means = df.groupby('Cluster')[features].mean()
            st.dataframe(cluster_means)
