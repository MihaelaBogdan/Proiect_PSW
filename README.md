#  Proiect PSW - Analiza Platformei Spotify utilizand Python si SAS

## Descriere
Acest proiect este un **dashboard Streamlit complet** pentru analiza unui dataset Spotify (5.000 de piese).  Include:
- Generare dataset sintetic (script `generate_dataset.py`).
- Încărcare & cache (`data_loader.py`).
- Pagini multi‑tab (`tabs/`):
  - Overview – KPI, distribuție genuri, radar audio etc.
  - (alte tab‑uri pot fi adăugate: preprocessing, statistici, clustering, regresie, clasificare, analize avansate).
- Design premium: dark‑mode, gradient, micro‑animări, font **Inter**.

##  Instalare și configurare
1. **Deschide terminalul în directorul proiectului**
   ```bash
   cd /Users/mihaela/Desktop/Proiect_pachete
   ```
2. **Creează un mediu virtual și instalează dependențele** (comanda a fost deja pornită în fundal, așteaptă finalizarea). Dacă vrei să rulezi manual:
   ```bash
   python3 -m venv venv               # creează mediul virtual
   ./venv/bin/pip install --upgrade pip
   ./venv/bin/pip install streamlit pandas plotly scikit-learn statsmodels seaborn
   ```
3. **Activează mediul** (macOS, zsh):
   ```bash
   source ./venv/bin/activate
   ```
4. **Generează dataset‑ul** (sau descarcă unul real – vezi secțiunea "Dataset real"): 
   ```bash
   python generate_dataset.py
   ```
   Acest script creează `spotify_tracks.csv` în directorul proiectului.

##  Obținerea unui dataset real (opțional)
- **Kaggle** – există *Spotify Songs Dataset* pe Kaggle. Pentru a-l descărca:
  1. Instalează `kaggle` în mediul virtual:
     ```bash
     ./venv/bin/pip install kaggle
     ```
  2. Creează un fișier `~/.kaggle/kaggle.json` cu tokenul tău API (obținut de pe kaggle.com → My Account → API → "Create New Token").
  3. Rulează:
     ```bash
     kaggle datasets download -d msd/spotify_dataset -p . --unzip
     ```
  4. Redenumește fișierul descărcat în `spotify_tracks.csv` sau modifică `load_data()` să citească numele corect.

##  Rulare aplicație
După ce mediul este activat și `spotify_tracks.csv` există, pornește dashboard‑ul:
```bash
streamlit run app.py
```
**Important:** comanda trebuie executată din directorul `Proiect_pachete`, nu din `Embeddings`. Dacă rulezi din altă locație, Python nu găsește pachetul `streamlit` (module‑not‑found).

## 📂 Structura directorului
```
Proiect_pachete/
├─ app.py               # intrare Streamlit
├─ generate_dataset.py  # script generare date sintetice
├─ data_loader.py       # încărcare și cache
├─ spotify_tracks.csv   # dataset – generat sau descărcat
├─ tabs/                # pachet cu pagini
│   ├─ __init__.py
│   ├─ tab_overview.py
│   └─ … (alte tab‑uri)
└─ README.md            # acest fișier
```

##  Depanare `ModuleNotFoundError: No module 'streamlit'`
1. **Asigură-te că mediul virtual este activ** (`source venv/bin/activate`).
2. **Verifică instalarea**:
   ```bash
   which streamlit   # ar trebui să indice ./venv/bin/streamlit
   streamlit --version
   ```
3. **Rulează din directorul corect** (`Proiect_pachete`).
4. Dacă tot apar erori, reinstalează:
   ```bash
   ./venv/bin/pip uninstall streamlit -y && ./venv/bin/pip install streaml i t
   ```

##  Design & UX
- Font: *Inter* (Google Fonts) – se încarcă în CSS.
- Paletă: tonuri închise, verde Spotify (`#1db954`).
- Carduri KPI, grafice Plotly în stil *dark*.
- Sidebar cu navigare intuitivă și informații de contact.

##  Ce poți adăuga în continuare
- **Pre‑processing** – curățare valori lipsă, scaling.
- **Statistici descriptive** – corelații, heatmap.
- **Clustering** – K‑Means pe caracteristici audio, vizualizare PCA.
- **Regresie** – prezicerea popularității din audio‑features.
- **Clasificare** – logistic regression pentru genuri.
- **Analiză avansată** – modelare mixtă, SHAP explicabilitate.



