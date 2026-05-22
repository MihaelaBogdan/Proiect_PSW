"""
tab_preprocessing.py — Curățare, Codificare, Scalare
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder

def render():
  st.markdown("#  Preprocesare Date")
  st.markdown("În această secțiune tratăm valorile lipsă, codificăm datele categorice și scalăm variabilele numerice.")
  
  if "raw_data" not in st.session_state:
    st.session_state.raw_data = pd.read_csv("spotify_tracks.csv")
  
  df = st.session_state.raw_data.copy()
  
  st.subheader("1. Tratarea valorilor lipsă și extreme")
  col1, col2 = st.columns(2)
  
  with col1:
    st.write("Valori lipsă inițiale:")
    st.dataframe(df.isna().sum()[df.isna().sum() > 0])
    
  # Tratare valori lipsă
  df['danceability'] = df['danceability'].fillna(df['danceability'].median())
  df['energy'] = df['energy'].fillna(df['energy'].median())
  df['tempo'] = df['tempo'].fillna(df['tempo'].median())
  df['popularity'] = df['popularity'].fillna(df['popularity'].median())
  
  # Tratare valori extreme (ex: tempo > 200, popularity > 100)
  df.loc[df['tempo'] > 200, 'tempo'] = df['tempo'].median()
  df.loc[df['popularity'] > 100, 'popularity'] = 100
  df.loc[df['loudness'] < -60, 'loudness'] = df['loudness'].median()
  
  with col2:
    st.write("După tratare (imputare cu mediană):")
    st.dataframe(df.isna().sum()[df.isna().sum() > 0])
    st.success("Valorile lipsă și extreme au fost tratate!")

  st.subheader("2. Codificare Date (Label Encoding)")
  st.write("Transformăm genurile muzicale în valori numerice folosind `LabelEncoder`.")
  le = LabelEncoder()
  df['genre_encoded'] = le.fit_transform(df['genre'])
  
  st.dataframe(df[['genre', 'genre_encoded']].drop_duplicates().head(5))
  
  st.subheader("3. Scalare Date")
  scaler_type = st.selectbox("Alege metoda de scalare pentru caracteristicile audio:", ["StandardScaler", "MinMaxScaler"])
  
  features_to_scale = ['danceability', 'energy', 'tempo', 'loudness', 'valence']
  
  if scaler_type == "StandardScaler":
    scaler = StandardScaler()
  else:
    scaler = MinMaxScaler()
    
  df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
  
  st.write(f"Date scalate cu {scaler_type}:")
  st.dataframe(df[features_to_scale].head())
  
  st.session_state.processed_data = df
  st.success("Datele au fost preprocesate și salvate în sesiune pentru analizele următoare!")
