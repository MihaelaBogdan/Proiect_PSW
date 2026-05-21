import os
import glob

replacements = {
    'x="genre"': 'x="genre", labels={"genre": "Gen Muzical"}',
    'x="popularity"': 'x="popularity", labels={"popularity": "Popularitate"}',
    'y="popularity"': 'y="popularity", labels={"popularity": "Popularitate"}',
    'x="energy"': 'x="energy", labels={"energy": "Energie"}',
    'y="energy"': 'y="energy", labels={"energy": "Energie"}',
    'x="danceability"': 'x="danceability", labels={"danceability": "Dansabilitate"}',
    'y="danceability"': 'y="danceability", labels={"danceability": "Dansabilitate"}',
    'x="year"': 'x="year", labels={"year": "Anul Lansării"}',
    'x="PC1"': 'x="PC1", labels={"PC1": "Componenta Principală 1"}',
    'y="PC2"': 'y="PC2", labels={"PC2": "Componenta Principală 2"}',
    '"Feature"': '"Caracteristică"',
    '"Importance"': '"Importanță"',
    "'Feature'": "'Caracteristică'",
    "'Importance'": "'Importanță'",
    'x="Model"': 'x="Model", labels={"Model": "Model de Predicție"}',
    'x="R-squared"': 'x="R-squared", labels={"R-squared": "Scor R-Pătrat"}',
    'y="R-squared"': 'y="R-squared", labels={"R-squared": "Scor R-Pătrat"}',
    'color="genre"': 'color="genre", labels={"genre": "Gen Muzical"}',
    'hover_data=["track_name", "artist_name", "popularity"]': 'hover_data={"track_name": True, "artist_name": True, "popularity": True}',
    'xaxis_title="An"': 'xaxis_title="Anul Lansării"',
    'yaxis_title="Valoare Medie"': 'yaxis_title="Valoarea Medie"',
    '"track_name"': '"Nume Piesă"',
    '"artist_name"': '"Nume Artist"',
    '"genre"': '"Gen Muzical"',
    '"popularity"': '"Popularitate"',
    '"duration_min"': '"Durată (min)"',
    '"tempo"': '"Tempo (BPM)"',
    '"loudness"': '"Volum (dB)"',
    '"instrumentalness"': '"Instrumentalitate"',
    '"acousticness"': '"Acusticitate"',
    '"speechiness"': '"Vocale"',
    '"liveness"': '"Live"',
    '"valence"': '"Valență (Pozitivitate)"',
    '"danceability"': '"Dansabilitate"',
    '"energy"': '"Energie"'
}

files = glob.glob('tabs/*.py')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Simple replace logic
    # To avoid double replacements we only replace if not already replaced
    # Actually just renaming the Dataframe columns before plotting is the easiest way.
