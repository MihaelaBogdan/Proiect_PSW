"""
data_loader.py — Încarcă și cache-uiește datasetul Spotify
"""
import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data() -> pd.DataFrame:
    # Caută fișierul atât în directorul curent de lucru, cât și în cel în care se află scriptul
    paths_to_try = [
        "spotify_tracks.csv",
        os.path.join(os.path.dirname(__file__), "spotify_tracks.csv")
    ]
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception:
                pass
                
    st.error("❌ Fișierul `spotify_tracks.csv` nu a fost găsit. Rulați `generate_dataset.py` mai întâi.")
    st.stop()

AUDIO_FEATURES = [
    "danceability", "energy", "valence", "tempo",
    "acousticness", "instrumentalness", "speechiness",
    "liveness", "loudness",
]

NUMERIC_COLS = AUDIO_FEATURES + ["popularity", "duration_min", "duration_ms"]

GENRE_COLORS = {
    "pop":       "#1db954",
    "rock":      "#e91e63",
    "hip-hop":   "#ff9800",
    "electronic":"#00bcd4",
    "r&b":       "#9c27b0",
    "jazz":      "#3f51b5",
    "classical": "#795548",
    "country":   "#8bc34a",
    "latin":     "#ff5722",
    "metal":     "#607d8b",
    "folk":      "#cddc39",
    "blues":     "#2196f3",
    "reggae":    "#4caf50",
    "soul":      "#ff4081",
    "indie":     "#00e5ff",
}
