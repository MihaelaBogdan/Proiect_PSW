import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def add_title(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.name = 'Times New Roman'
        run.font.color.rgb = None

def add_paragraph(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = bold
    run.italic = italic
    return p

def add_code(doc, code_text):
    p = doc.add_paragraph()
    p.style = 'No Spacing'
    run = p.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)

def main():
    doc = Document()
    
    # --- COPERTĂ ---
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ACADEMIA DE STUDII ECONOMICE DIN BUCUREȘTI\nFacultatea de Cibernetică, Statistică și Informatică Economică\nSpecializarea Informatică Economică\n\n\n\n\n")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Proiect Pachete Software\nStudiu asupra succesului pieselor muzicale pe Spotify utilizând Python și SAS\n\n\n\n\n")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.bold = True
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run("Coordonator științific\nAsistent univ. dr. ENE Gabriela\n\n\nStudent\nBOGDAN Mihaela")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("\n\n\n\n\nBucurești\n2025")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    
    doc.add_page_break()

    # --- CUPRINS ---
    add_title(doc, "Cuprins")
    add_paragraph(doc, "a) Definirea problemei")
    add_paragraph(doc, "b) Informații necesare pentru rezolvare")
    add_paragraph(doc, "c) Metode de calcul, algoritmi, formule de calcul utilizate")
    add_paragraph(doc, "   I) Python")
    add_paragraph(doc, "   II) SAS")
    add_paragraph(doc, "d) Prezentarea rezultatelor și interpretarea economică")
    doc.add_page_break()

    # --- A ---
    add_title(doc, "a) Definirea problemei", level=1)
    add_paragraph(doc, "În industria muzicală contemporană, platformele de streaming precum Spotify au schimbat complet modul în care muzica este consumată și monetizată. Obiectivul acestui proiect este de a analiza un set masiv de date muzicale pentru a identifica tiparele care stau la baza unei melodii de succes (popularitate ridicată). Scopul principal este anticiparea popularității și segmentarea pieței utilizând instrumente avansate de Data Science prin Python (Streamlit, Pandas, Scikit-Learn) și limbajul SAS.")

    # --- B ---
    add_title(doc, "b) Informații necesare pentru rezolvare", level=1)
    add_title(doc, "Setul de date inițial", level=2)
    add_paragraph(doc, "Pentru acest studiu s-a utilizat un set de date vast cu 5.000 de observații reprezentând melodii (piese muzicale) distincte, provenind din API-ul oficial Spotify. Setul este structurat tabelar, unde fiecare rând reprezintă o piesă, iar coloanele conțin informații cantitative (caracteristici acustice extrase de AI-ul Spotify) și calitative.")
    
    add_title(doc, "Variabilele din setul de date", level=2)
    add_paragraph(doc, "• track_name (Categoric): Numele piesei muzicale.")
    add_paragraph(doc, "• artist_name (Categoric): Artistul sau trupa.")
    add_paragraph(doc, "• genre (Categoric): Genul muzical (ex: pop, rock, hip-hop, electronic, jazz, classical).")
    add_paragraph(doc, "• year (Numeric): Anul lansării melodiei.")
    add_paragraph(doc, "• popularity (Numeric): Scorul de popularitate al piesei, calculat de algoritmul Spotify pe o scară de la 0 la 100.")
    add_paragraph(doc, "• explicit (Categoric/Binar): Indică dacă piesa conține limbaj obscen (1 = Yes, 0 = No).")
    add_paragraph(doc, "• danceability (Numeric): Cât de potrivită este piesa pentru dans, bazat pe tempo, ritm și forță (0.0 - 1.0).")
    add_paragraph(doc, "• energy (Numeric): Intensitatea și activitatea percepută a piesei muzicale (0.0 - 1.0).")
    add_paragraph(doc, "• valence (Numeric): Măsura pozitivității muzicale transmise de piesă (melancolic vs fericit).")
    add_paragraph(doc, "• tempo (Numeric): Viteza melodiei estimată în bătăi pe minut (BPM).")
    add_paragraph(doc, "• loudness (Numeric): Nivelul general de zgomot/volum al piesei în decibeli (dB).")
    add_paragraph(doc, "• acousticness, instrumentalness, speechiness, liveness (Numerice): Indicatori ce măsoară gradul de acusticitate, prezența instrumentelor, prezența vocală și prezența audienței live.")

    # --- C - PYTHON ---
    add_title(doc, "c) Metode de calcul, algoritmi, formule de calcul utilizate", level=1)
    add_title(doc, "I) Python", level=2)
    add_paragraph(doc, "Întregul proiect Python a fost construit modular folosind framework-ul Streamlit pentru crearea unui dashboard interactiv.")

    add_title(doc, "Citirea fișierului CSV și încărcarea datelor", level=3)
    add_paragraph(doc, "Fișierul a fost importat folosind biblioteca Pandas. Funcția a fost memorată cu cache (@st.cache_data) pentru a optimiza viteza de rulare a aplicației la reîncărcările paginii.")
    add_code(doc, "@st.cache_data\ndef load_data():\n    df = pd.read_csv('spotify_tracks.csv')\n    return df\ndata = load_data()")

    add_title(doc, "Tratarea valorilor lipsă și a celor extreme (Outliers)", level=3)
    add_paragraph(doc, "Valorile lipsă pentru variabilele numerice importante au fost identificate și imputate (înlocuite) cu valoarea mediană, deoarece mediana este o măsură de tendință centrală mult mai rezistentă la extreme decât media aritmetică. De asemenea, au fost retezate valorile aberante (outliers) pentru tempo folosind funcția `clip`.")
    add_code(doc, "df['danceability'].fillna(df['danceability'].median(), inplace=True)\ndf['energy'].fillna(df['energy'].median(), inplace=True)\ndf['popularity'].fillna(df['popularity'].median(), inplace=True)\n\n# Tratare outliers tempo\ndf['tempo'] = df['tempo'].clip(upper=200)")

    add_title(doc, "Metode de codificare (Encoding)", level=3)
    add_paragraph(doc, "Pentru ca genul muzical să poată fi procesat de algoritmii de Machine Learning (precum K-Means), variabila categorială text 'genre' a fost transformată numeric utilizând `LabelEncoder` din Scikit-Learn.")
    add_code(doc, "from sklearn.preprocessing import LabelEncoder\nle = LabelEncoder()\ndf['genre_encoded'] = le.fit_transform(df['genre'])")

    add_title(doc, "Metode de scalare", level=3)
    add_paragraph(doc, "Pentru a aduce caracteristicile audio la aceeași scară valorică (evitând astfel ca tempo-ul, care are valori de peste 100, să domine energia, care e între 0 și 1), am aplicat atât `StandardScaler` (pentru normalizare statistică Z-score), cât și `MinMaxScaler` (pentru aducerea în intervalul 0-1).")
    add_code(doc, "from sklearn.preprocessing import StandardScaler, MinMaxScaler\nscaler_st = StandardScaler()\ndf[cols_to_scale] = scaler_st.fit_transform(df[cols_to_scale])\n\nscaler_mm = MinMaxScaler()\ndf[cols_to_scale] = scaler_mm.fit_transform(df[cols_to_scale])")

    add_title(doc, "Prelucrări statistice, gruparea și agregarea datelor", level=3)
    add_paragraph(doc, "Am folosit Pandas pentru a extrage statistici descriptive (`describe()`) și pentru a grupa datele pe genuri muzicale. Funcția de grup `transform('mean')` a fost folosită ingenios pentru a calcula popularitatea relativă a fiecărei piese comparativ cu media genului din care face parte.")
    add_code(doc, "grouped = df.groupby('genre').agg(\n    Popularitate_Medie=('popularity', 'mean'),\n    Energie_Medie=('energy', 'mean'),\n    Nr_Piese=('track_id', 'count')\n)\n\n# Transformare\ndf['pop_medie_gen'] = df.groupby('genre')['popularity'].transform('mean')\ndf['pop_relativa'] = df['popularity'] - df['pop_medie_gen']")

    add_title(doc, "Machine Learning: Clusterizare (K-Means) și PCA", level=3)
    add_paragraph(doc, "Pentru a segmenta piesele în categorii de comportament acustic, am aplicat algoritmul nesupervizat K-Means. Pentru vizualizarea grupurilor în planul 2D am utilizat Reducerea Dimensionalității prin Principal Component Analysis (PCA).")
    add_code(doc, "from sklearn.cluster import KMeans\nfrom sklearn.decomposition import PCA\n\npca = PCA(n_components=2)\ncomponents = pca.fit_transform(X_scaled)\n\nkmeans = KMeans(n_clusters=4, random_state=42)\nclusters = kmeans.fit_predict(X_scaled)\ndf['Cluster'] = clusters")

    add_title(doc, "Machine Learning: Regresie Multiplă (Statsmodels)", level=3)
    add_paragraph(doc, "Pentru a investiga influența fiecărei caracteristici audio asupra popularității, am creat un model de Regresie Multiplă OLS (Ordinary Least Squares).")
    add_code(doc, "import statsmodels.api as sm\n\nX = df[['danceability', 'energy', 'valence', 'tempo']]\ny = df['popularity']\nX_const = sm.add_constant(X)\n\nmodel = sm.OLS(y, X_const).fit()\nprint(model.summary())")

    add_title(doc, "Machine Learning: Clasificare (Logistic Regression) și Random Forest", level=3)
    add_paragraph(doc, "Am utilizat Regresia Logistică pentru a prezice caracterul Explicit (1) sau Non-Explicit (0) al piesei. Pentru un studiu avansat de Feature Importance, am folosit și algoritmul ansamblat Random Forest.")
    add_code(doc, "from sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestRegressor\n\n# Logistic\nlog_model = LogisticRegression(class_weight='balanced')\nlog_model.fit(X_train, y_train)\ny_pred = log_model.predict(X_test)\n\n# Random Forest\nrf = RandomForestRegressor(n_estimators=100)\nrf.fit(X_train, y_train)")

    # --- C - SAS ---
    add_title(doc, "II) SAS", level=2)
    add_paragraph(doc, "Codul SAS a urmărit replicarea, aprofundarea și tratarea avansată statistică a aceluiași set de date din perspectiva enterprise.")

    add_title(doc, "Import Date din fișiere externe", level=3)
    add_paragraph(doc, "S-a utilizat PROC IMPORT pentru aducerea datelor din mediul extern.")
    add_code(doc, "PROC IMPORT\n    DATAFILE = 'spotify_tracks.csv'\n    OUT      = WORK.spotify_raw\n    DBMS     = CSV\n    REPLACE;\nRUN;")

    add_title(doc, "Formate definite de utilizator", level=3)
    add_paragraph(doc, "S-a utilizat PROC FORMAT pentru o raportare calitativă a indicelui numeric de popularitate și a deceniului.")
    add_code(doc, "PROC FORMAT;\n    VALUE pop_fmt\n        LOW  -< 25 = 'Necunoscut'\n        25   -< 50 = 'De nisa'\n        50   -< 85 = 'Popular'\n        85  -  HIGH = 'Viral';\nRUN;")

    add_title(doc, "Procesare iterativă (ARRAY) și Condițională", level=3)
    add_paragraph(doc, "S-au utilizat Masive (ARRAY) în interiorul DATA step-ului pentru tratarea unitară a valorilor lipsă printr-o singură buclă iterativă, evitând duplicarea codului.")
    add_code(doc, "DATA WORK.spotify_clean;\n    SET WORK.spotify_raw;\n    ARRAY num_vars[*] danceability energy valence;\n    DO i = 1 TO DIM(num_vars);\n        IF MISSING(num_vars[i]) THEN num_vars[i] = 0.5;\n    END;\nRUN;")

    add_title(doc, "Crearea de subseturi și SQL în SAS", level=3)
    add_paragraph(doc, "Am filtrat dinamic datele și am folosit comenzi PROC SQL pentru join-uri complexe și agregări, extrăgând cele mai reprezentative statistici pentru genurile muzicale.")
    add_code(doc, "PROC SQL;\n    CREATE TABLE WORK.genre_stats AS\n    SELECT genre, COUNT(*) AS nr_piese, MEAN(popularity) AS pop_medie\n    FROM WORK.spotify_clean\n    GROUP BY genre;\nQUIT;")

    add_title(doc, "Combinarea datelor (MERGE) și Funcții SAS", level=3)
    add_paragraph(doc, "Seturile de date agregate au fost alipite la setul inițial folosind procedura de sortare urmată de instrucțiunea MERGE pe cheia 'genre'. De asemenea, au fost aplicate multiple funcții SAS: LOG, SQRT, UPCASE, ROUND, MEAN.")
    add_code(doc, "PROC SORT DATA=WORK.spotify_clean; BY genre; RUN;\nPROC SORT DATA=WORK.genre_stats; BY genre; RUN;\n\nDATA WORK.spotify_enriched;\n    MERGE WORK.spotify_clean (IN=a) WORK.genre_stats (IN=b);\n    BY genre;\n    IF a;\nRUN;")

    add_title(doc, "Macro-uri", level=3)
    add_paragraph(doc, "Pentru analiza automată pe oricare dintre genurile muzicale a fost dezvoltat un macro reutilizabil.")
    add_code(doc, "%MACRO AnalizaGen(gen_nume=);\n    PROC SGPLOT DATA=WORK.spotify_enriched;\n        WHERE genre = \"&gen_nume\";\n        SCATTER X=energy Y=danceability;\n    RUN;\n%MEND AnalizaGen;\n%AnalizaGen(gen_nume=pop);")

    add_title(doc, "Proceduri Statistice Avansate, Grafice și SAS ML", level=3)
    add_paragraph(doc, "Componenta statistică, WOW FACTOR-ul și Machine Learning-ul din SAS a conținut:")
    add_paragraph(doc, "1. PROC FASTCLUS: Clusterizare K-Means pentru identificarea profilurilor ascultătorilor.")
    add_paragraph(doc, "2. PROC REG și PROC LOGISTIC: Modele de predicție direct în SAS.")
    add_paragraph(doc, "3. PROC GLM (ANOVA) și testul Tukey: Demonstrarea faptului că diferențele de popularitate dintre genuri sunt statistic semnificative, nu variații aleatorii.")
    add_paragraph(doc, "4. PROC DISCRIM: Analiza Discriminantă (Metodă ML de clasificare) pentru ghicirea genului muzical pe baza indicatorilor.")
    add_paragraph(doc, "5. SGPLOT și SGSCATTER: Grafice vizuale cu hărți de densitate, Bubble plot-uri interactive și Hărți de căldură (HEATMAP).")

    # --- D ---
    add_title(doc, "d) Prezentarea rezultatelor și interpretarea economică", level=1)
    add_paragraph(doc, "Analiza exhaustivă a setului de date Spotify scoate în evidență elementele definitorii pentru un produs muzical de succes.")
    add_paragraph(doc, "Rezultate Python: Modelele OLS au stabilit clar că există factori dominanți ce determină o reacție pozitivă a masei de ascultători. Variabile precum „Danceability” și „Energy” corelează direct proporțional cu creșterea popularității medii. Totodată, algoritmii de clusterizare din Python (K-Means) au demonstrat că piesele pot fi segmentate automat de inteligența artificială, identificând clustere cu o acusticitate foarte ridicată dar popularitate redusă (muzică de nișă) și clustere extrem de zgomotoase și ritmate cu cerere masivă globală (hituri comerciale). Graficele vizuale superioare (Treemap, Sunburst și Ploturile Tridimensionale) au adus la viață distribuția inegală a cotei de piață muzicale pe genuri.")
    add_paragraph(doc, "Rezultate SAS: În mediul enterprise SAS, testele de varianță ANOVA au confirmat dincolo de orice dubiu rezonabil că diferența de succes între genuri muzicale nu este aleatorie. Matricea Heatmap a vizualizat eficient zona optimă de performanță. Din punct de vedere economic și decizional pentru un manager al unei Case de Discuri, acest studiu demonstrează că o campanie de marketing muzical nu trebuie fondată doar pe fler artistic. Extragerea și standardizarea parametrilor (Tempo, Volum, Valență) dintr-un demo muzical și aplicarea acestora într-un algoritm antrenat (ca Random Forest-ul sau Analiza Discriminantă dezvoltate) permite prognozarea realistă a ROI-ului (Return of Investment). Cunoașterea acestor indicatori optimizează cheltuielile publicitare, direcționând capital doar către piesele cu cel mai mare potențial algoritmic pe platformele digitale.")

    doc.save("Documentatie_Proiect_Python_SAS.docx")

if __name__ == "__main__":
    main()
