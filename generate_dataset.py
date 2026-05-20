"""
generate_dataset.py
-------------------
Generează un dataset realist tip Spotify cu ~5000 de piese muzicale.
Structura este identică cu Spotify Tracks Dataset de pe Kaggle.
Rulați o singură dată pentru a crea fișierul spotify_tracks.csv.
"""

import numpy as np
import pandas as pd
import random

np.random.seed(42)
random.seed(42)

N = 5000  # număr de piese

GENRES = [
    "pop", "rock", "hip-hop", "electronic", "r&b",
    "jazz", "classical", "country", "latin", "metal",
    "folk", "blues", "reggae", "soul", "indie",
]

ARTISTS_BY_GENRE = {
    "pop": ["Taylor Swift", "Ed Sheeran", "Ariana Grande", "Harry Styles", "Dua Lipa",
            "Billie Eilish", "Justin Bieber", "Selena Gomez", "Katy Perry", "Bruno Mars"],
    "rock": ["Imagine Dragons", "Foo Fighters", "The Killers", "Arctic Monkeys", "Muse",
             "Linkin Park", "Green Day", "Red Hot Chili Peppers", "Pearl Jam", "Nirvana"],
    "hip-hop": ["Drake", "Kendrick Lamar", "J. Cole", "Travis Scott", "Post Malone",
                "Cardi B", "Nicki Minaj", "Eminem", "Jay-Z", "Kanye West"],
    "electronic": ["Daft Punk", "Calvin Harris", "Martin Garrix", "The Chainsmokers",
                   "Avicii", "Marshmello", "Skrillex", "Deadmau5", "Zedd", "Kygo"],
    "r&b": ["The Weeknd", "SZA", "Frank Ocean", "Beyoncé", "Usher",
            "Alicia Keys", "John Legend", "H.E.R.", "Khalid", "H.E.R."],
    "jazz": ["Miles Davis", "John Coltrane", "Duke Ellington", "Thelonious Monk",
             "Charlie Parker", "Louis Armstrong", "Herbie Hancock", "Bill Evans", "Chet Baker", "Dave Brubeck"],
    "classical": ["Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach",
                  "Frédéric Chopin", "Franz Schubert", "Claude Debussy", "Pyotr Tchaikovsky",
                  "Johannes Brahms", "Antonio Vivaldi", "Sergei Rachmaninoff"],
    "country": ["Luke Bryan", "Blake Shelton", "Carrie Underwood", "Chris Stapleton",
                "Morgan Wallen", "Zac Brown Band", "Keith Urban", "Miranda Lambert",
                "Tim McGraw", "Kenny Chesney"],
    "latin": ["Bad Bunny", "J Balvin", "Shakira", "Maluma", "Ozuna",
              "Daddy Yankee", "Nicky Jam", "Anuel AA", "Karol G", "Ricky Martin"],
    "metal": ["Metallica", "Iron Maiden", "Slayer", "Megadeth", "Black Sabbath",
              "Pantera", "Judas Priest", "Slipknot", "System of a Down", "Lamb of God"],
    "folk": ["Bob Dylan", "Simon & Garfunkel", "Joni Mitchell", "Neil Young", "Fleet Foxes",
             "Bon Iver", "Sufjan Stevens", "Iron & Wine", "The Lumineers", "Mumford & Sons"],
    "blues": ["B.B. King", "Muddy Waters", "Robert Johnson", "John Lee Hooker",
              "Stevie Ray Vaughan", "Eric Clapton", "Buddy Guy", "Taj Mahal", "Keb' Mo'", "Gary Clark Jr."],
    "reggae": ["Bob Marley", "Peter Tosh", "Jimmy Cliff", "Toots and the Maytals",
               "Burning Spear", "Steel Pulse", "Culture", "Gregory Isaacs", "Desmond Dekker", "Lee Scratch Perry"],
    "soul": ["Marvin Gaye", "Aretha Franklin", "Otis Redding", "Al Green", "Sam Cooke",
             "Ray Charles", "Stevie Wonder", "James Brown", "Curtis Mayfield", "Wilson Pickett"],
    "indie": ["Tame Impala", "Radiohead", "Vampire Weekend", "The National", "Alt-J",
              "Arcade Fire", "Modest Mouse", "Beach House", "Real Estate", "Car Seat Headrest"],
}

SONG_WORDS = [
    "Love", "Night", "Dreams", "Fire", "Heart", "Soul", "Fade", "Rise",
    "Broken", "Lost", "Found", "Light", "Dark", "Rain", "Sun", "Moon",
    "Star", "Gold", "Silver", "Blue", "Red", "Black", "White", "Wild",
    "Free", "Alive", "Gone", "Stay", "Run", "Fly", "Fall", "Dance",
    "Cry", "Smile", "Kiss", "Touch", "Feel", "Breathe", "Whisper", "Shout",
    "Forever", "Never", "Always", "Sometimes", "Maybe", "Today", "Yesterday",
]

def random_track_name():
    n = random.choice([1, 2, 3])
    return " ".join(random.sample(SONG_WORDS, n))

# Audio features with genre-specific distributions
def audio_features_for_genre(genre):
    params = {
        "pop":       dict(danceability=(0.72, 0.10), energy=(0.68, 0.12), valence=(0.60, 0.15),
                          tempo=(118, 15), acousticness=(0.15, 0.12), instrumentalness=(0.01, 0.02),
                          speechiness=(0.06, 0.04), liveness=(0.13, 0.07), loudness=(-5.5, 2.0),
                          duration_ms=(200000, 30000), key_bias=range(12), mode_bias=0.65),
        "rock":      dict(danceability=(0.55, 0.12), energy=(0.82, 0.10), valence=(0.50, 0.18),
                          tempo=(130, 20), acousticness=(0.08, 0.10), instrumentalness=(0.05, 0.08),
                          speechiness=(0.05, 0.03), liveness=(0.17, 0.08), loudness=(-4.0, 2.5),
                          duration_ms=(230000, 45000), key_bias=range(12), mode_bias=0.60),
        "hip-hop":   dict(danceability=(0.78, 0.08), energy=(0.65, 0.12), valence=(0.55, 0.18),
                          tempo=(95, 18), acousticness=(0.12, 0.10), instrumentalness=(0.03, 0.05),
                          speechiness=(0.22, 0.10), liveness=(0.14, 0.07), loudness=(-5.0, 2.0),
                          duration_ms=(215000, 35000), key_bias=range(12), mode_bias=0.55),
        "electronic":dict(danceability=(0.80, 0.08), energy=(0.82, 0.10), valence=(0.55, 0.18),
                          tempo=(128, 10), acousticness=(0.05, 0.07), instrumentalness=(0.55, 0.30),
                          speechiness=(0.05, 0.03), liveness=(0.13, 0.06), loudness=(-5.5, 2.0),
                          duration_ms=(250000, 60000), key_bias=range(12), mode_bias=0.55),
        "r&b":       dict(danceability=(0.70, 0.10), energy=(0.58, 0.12), valence=(0.52, 0.18),
                          tempo=(100, 16), acousticness=(0.22, 0.14), instrumentalness=(0.02, 0.04),
                          speechiness=(0.09, 0.05), liveness=(0.13, 0.07), loudness=(-6.5, 2.5),
                          duration_ms=(225000, 35000), key_bias=range(12), mode_bias=0.58),
        "jazz":      dict(danceability=(0.48, 0.12), energy=(0.45, 0.12), valence=(0.55, 0.18),
                          tempo=(115, 25), acousticness=(0.60, 0.20), instrumentalness=(0.35, 0.25),
                          speechiness=(0.04, 0.02), liveness=(0.18, 0.10), loudness=(-12.0, 4.0),
                          duration_ms=(300000, 90000), key_bias=range(12), mode_bias=0.50),
        "classical": dict(danceability=(0.30, 0.10), energy=(0.28, 0.12), valence=(0.40, 0.18),
                          tempo=(95, 30), acousticness=(0.88, 0.10), instrumentalness=(0.85, 0.12),
                          speechiness=(0.03, 0.01), liveness=(0.10, 0.06), loudness=(-18.0, 6.0),
                          duration_ms=(400000, 150000), key_bias=range(12), mode_bias=0.55),
        "country":   dict(danceability=(0.60, 0.10), energy=(0.62, 0.12), valence=(0.62, 0.15),
                          tempo=(120, 18), acousticness=(0.35, 0.15), instrumentalness=(0.01, 0.02),
                          speechiness=(0.05, 0.03), liveness=(0.15, 0.08), loudness=(-6.0, 2.5),
                          duration_ms=(215000, 30000), key_bias=[0, 2, 5, 7, 9], mode_bias=0.75),
        "latin":     dict(danceability=(0.78, 0.08), energy=(0.72, 0.10), valence=(0.70, 0.15),
                          tempo=(105, 15), acousticness=(0.18, 0.12), instrumentalness=(0.02, 0.04),
                          speechiness=(0.10, 0.05), liveness=(0.14, 0.07), loudness=(-5.5, 2.0),
                          duration_ms=(215000, 30000), key_bias=range(12), mode_bias=0.65),
        "metal":     dict(danceability=(0.45, 0.12), energy=(0.90, 0.06), valence=(0.35, 0.15),
                          tempo=(145, 25), acousticness=(0.04, 0.06), instrumentalness=(0.12, 0.15),
                          speechiness=(0.07, 0.04), liveness=(0.18, 0.09), loudness=(-3.5, 2.0),
                          duration_ms=(280000, 60000), key_bias=[0, 2, 3, 5, 7, 9, 10], mode_bias=0.40),
        "folk":      dict(danceability=(0.50, 0.12), energy=(0.48, 0.12), valence=(0.52, 0.18),
                          tempo=(112, 18), acousticness=(0.65, 0.18), instrumentalness=(0.05, 0.08),
                          speechiness=(0.04, 0.02), liveness=(0.14, 0.08), loudness=(-10.0, 3.0),
                          duration_ms=(230000, 50000), key_bias=range(12), mode_bias=0.65),
        "blues":     dict(danceability=(0.55, 0.10), energy=(0.55, 0.12), valence=(0.45, 0.18),
                          tempo=(110, 20), acousticness=(0.45, 0.18), instrumentalness=(0.08, 0.10),
                          speechiness=(0.05, 0.03), liveness=(0.20, 0.10), loudness=(-9.0, 3.0),
                          duration_ms=(250000, 50000), key_bias=[0, 2, 5, 7, 10], mode_bias=0.45),
        "reggae":    dict(danceability=(0.72, 0.08), energy=(0.55, 0.10), valence=(0.68, 0.15),
                          tempo=(80, 10), acousticness=(0.30, 0.14), instrumentalness=(0.04, 0.06),
                          speechiness=(0.08, 0.04), liveness=(0.16, 0.08), loudness=(-8.0, 2.5),
                          duration_ms=(240000, 40000), key_bias=range(12), mode_bias=0.60),
        "soul":      dict(danceability=(0.65, 0.10), energy=(0.60, 0.12), valence=(0.58, 0.18),
                          tempo=(105, 18), acousticness=(0.35, 0.15), instrumentalness=(0.02, 0.04),
                          speechiness=(0.06, 0.03), liveness=(0.18, 0.09), loudness=(-8.0, 3.0),
                          duration_ms=(220000, 35000), key_bias=range(12), mode_bias=0.60),
        "indie":     dict(danceability=(0.55, 0.12), energy=(0.60, 0.12), valence=(0.48, 0.20),
                          tempo=(118, 18), acousticness=(0.28, 0.16), instrumentalness=(0.10, 0.12),
                          speechiness=(0.04, 0.02), liveness=(0.14, 0.08), loudness=(-8.5, 3.0),
                          duration_ms=(240000, 45000), key_bias=range(12), mode_bias=0.55),
    }
    p = params[genre]
    def clip(val, lo=0.0, hi=1.0):
        return float(np.clip(val, lo, hi))

    return {
        "danceability":     clip(np.random.normal(*p["danceability"])),
        "energy":           clip(np.random.normal(*p["energy"])),
        "valence":          clip(np.random.normal(*p["valence"])),
        "tempo":            float(max(40, np.random.normal(*p["tempo"]))),
        "acousticness":     clip(np.random.normal(*p["acousticness"])),
        "instrumentalness": clip(np.random.normal(*p["instrumentalness"])),
        "speechiness":      clip(np.random.normal(*p["speechiness"])),
        "liveness":         clip(np.random.normal(*p["liveness"])),
        "loudness":         float(np.clip(np.random.normal(*p["loudness"]), -60, 0)),
        "duration_ms":      int(max(60000, np.random.normal(*p["duration_ms"]))),
        "key":              int(random.choice(list(p["key_bias"]))),
        "mode":             int(np.random.binomial(1, p["mode_bias"])),
    }

KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

rows = []
for i in range(N):
    genre = random.choice(GENRES)
    artist = random.choice(ARTISTS_BY_GENRE[genre])
    feats = audio_features_for_genre(genre)
    year = random.randint(1960, 2024)
    popularity = int(np.clip(
        np.random.normal(
            55 if year > 2010 else (45 if year > 1990 else 30),
            18
        ), 0, 100
    ))
    # add mild noise / missing values (5%)
    if random.random() < 0.03:
        feats["danceability"] = np.nan
    if random.random() < 0.02:
        feats["energy"] = np.nan
    if random.random() < 0.02:
        feats["tempo"] = np.nan
    if random.random() < 0.01:
        popularity = np.nan

    rows.append({
        "track_id":           f"T{i:05d}",
        "track_name":         random_track_name(),
        "artist_name":        artist,
        "genre":              genre,
        "year":               year,
        "popularity":         popularity,
        "duration_ms":        feats["duration_ms"],
        "explicit":           int(random.random() < (0.25 if genre in ["hip-hop", "metal", "r&b"] else 0.07)),
        "danceability":       feats["danceability"],
        "energy":             feats["energy"],
        "key":                feats["key"],
        "key_name":           KEY_NAMES[feats["key"]],
        "loudness":           feats["loudness"],
        "mode":               feats["mode"],
        "speechiness":        feats["speechiness"],
        "acousticness":       feats["acousticness"],
        "instrumentalness":   feats["instrumentalness"],
        "liveness":           feats["liveness"],
        "valence":            feats["valence"],
        "tempo":              feats["tempo"],
        "time_signature":     random.choice([3, 4, 4, 4, 4]),  # mostly 4/4
    })

df = pd.DataFrame(rows)
df["duration_min"] = (df["duration_ms"] / 60000).round(2)

# Introduce a few intentional outliers for extreme value treatment demo
idxs = np.random.choice(df.index, size=30, replace=False)
df.loc[idxs[:10], "tempo"] = np.random.uniform(250, 400, 10)
df.loc[idxs[10:20], "loudness"] = np.random.uniform(-70, -65, 10)
df.loc[idxs[20:], "popularity"] = np.random.uniform(102, 120, 10)

output_path = "spotify_tracks.csv"
df.to_csv(output_path, index=False)
print(f"✅ Dataset generat: {output_path}")
print(f"   Shape: {df.shape}")
print(f"   Coloane: {list(df.columns)}")
print(f"\nPrimele 3 rânduri:")
print(df.head(3).to_string())
