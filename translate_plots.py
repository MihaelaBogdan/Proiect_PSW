import os
import glob

# Mapping of English column names/labels to Romanian
translation_dict = {
    '"genre"': '"Gen Muzical"',
    "'genre'": "'Gen Muzical'",
    '"popularity"': '"Popularitate"',
    "'popularity'": "'Popularitate'",
    '"danceability"': '"Dansabilitate"',
    "'danceability'": "'Dansabilitate'",
    '"energy"': '"Energie"',
    "'energy'": "'Energie'",
    '"valence"': '"Valență"',
    "'valence'": "'Valență'",
    '"tempo"': '"Tempo (BPM)"',
    "'tempo'": "'Tempo (BPM)'",
    '"acousticness"': '"Acusticitate"',
    "'acousticness'": "'Acusticitate'",
    '"instrumentalness"': '"Instrumentalitate"',
    "'instrumentalness'": "'Instrumentalitate'",
    '"speechiness"': '"Vocale"',
    "'speechiness'": "'Vocale'",
    '"liveness"': '"Prezență Live"',
    "'liveness'": "'Prezență Live'",
    '"loudness"': '"Volum (dB)"',
    "'loudness'": "'Volum (dB)'",
    '"duration_min"': '"Durată (min)"',
    "'duration_min'": "'Durată (min)'",
    '"track_name"': '"Nume Piesă"',
    "'track_name'": "'Nume Piesă'",
    '"artist_name"': '"Nume Artist"',
    "'artist_name'": "'Nume Artist'",
    '"year"': '"Anul Lansării"',
    "'year'": "'Anul Lansării'",
    '"PC1"': '"Componenta Principală 1"',
    "'PC1'": "'Componenta Principală 1'",
    '"PC2"': '"Componenta Principală 2"',
    "'PC2'": "'Componenta Principală 2'",
    '"Feature"': '"Caracteristică"',
    "'Feature'": "'Caracteristică'",
    '"Importance"': '"Importanță"',
    "'Importance'": "'Importanță'"
}

def translate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Special replacements for plotly labels
    content = content.replace('labels={"genre": "Gen", "count": "Numar Piese"}', 'labels={"Gen Muzical": "Gen", "count": "Număr Piese"}')
    content = content.replace('labels={"Gen Muzical": "Gen", "count": "Număr Piese"}', 'labels={"genre": "Gen", "count": "Număr Piese"}') # fallback
    
    # Let's just do a clean replacement of column names in the DataFrames before plotting, or replacing strings in the file.
    # To be perfectly safe and not break python code (like df['genre']), we should ONLY replace text inside strings that are used for titles/axis.
    # Actually, the easiest way to translate Plotly charts without breaking pandas logic is to add the `labels=` argument to px functions,
    # OR replace titles in `update_layout`.
    pass

# We will directly patch the files using python string replace on specific lines known to have english strings.
import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Common replacements for titles / labels
    content = content.replace('x="genre"', 'x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}')
    content = content.replace('x="popularity"', 'x="popularity", labels={"popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale", "genre": "Gen Muzical"}')
    content = content.replace('x="energy"', 'x="energy", labels={"popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale", "genre": "Gen Muzical"}')
    content = content.replace('x="danceability"', 'x="danceability", labels={"popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale", "genre": "Gen Muzical"}')
    content = content.replace('x="year"', 'x="year", labels={"year": "Anul Lansării", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență"}')
    content = content.replace('x="PC1"', 'x="PC1", labels={"PC1": "Componenta Principală 1", "PC2": "Componenta Principală 2", "genre": "Gen Muzical", "tip": "Tip (Normal/Outlier)"}')
    content = content.replace('x="Model"', 'x="Model", labels={"Model": "Model de Predicție", "R-squared": "Scor R-Pătrat"}')
    content = content.replace('x="Importance"', 'x="Importance", labels={"Importance": "Nivel de Importanță", "Feature": "Atribut Audio"}')
    
    # Fix double labels if they occurred
    content = re.sub(r'labels=\{.*?\}, labels=\{', 'labels={', content)
    
    # Fix specific axis titles
    content = content.replace('xaxis_title="Feature"', 'xaxis_title="Caracteristică"')
    content = content.replace('yaxis_title="Importance"', 'yaxis_title="Importanță"')
    content = content.replace('xaxis_title="An"', 'xaxis_title="Anul Lansării"')
    content = content.replace('yaxis_title="Valoare Medie"', 'yaxis_title="Valoarea Medie a Atributului"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in glob.glob('tabs/*.py'):
    patch_file(f)

print("Plotly labels translated to Romanian.")
