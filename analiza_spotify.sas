/*===========================================================
  PROIECT: Analiza Platformei Spotify — Programare SAS
  Cerinte acoperite (minim 8):
    1. Creare set de date SAS din fisiere externe (PROC IMPORT)
    2. Formate definite de utilizator (PROC FORMAT)
    3. Procesare iterativa si conditionala (DATA step + IF/DO)
    4. Creare subseturi de date (WHERE / OUTPUT)
    5. Functii SAS (ROUND, MEAN, COMPRESS, UPCASE, etc.)
    6. Combinarea seturilor de date (MERGE / SET)
    7. Utilizarea de masive (ARRAY)
    8. SQL in SAS (PROC SQL)
    9. Proceduri statistice si Machine Learning (SAS ML)
       (PROC MEANS, PROC FREQ, PROC CORR, PROC REG,
        PROC LOGISTIC, PROC FASTCLUS)
   10. Generare grafice (PROC SGPLOT, PROC SGPANEL, ODS)
   11. Macro-uri SAS (%MACRO / %MEND)
===========================================================*/

/* ─── 0. Optiuni globale ─────────────────────────────────── */
OPTIONS NODATE NONUMBER PAGESIZE=60 LINESIZE=120;
ODS GRAPHICS ON;
TITLE "Proiect Analiza Spotify — Pachete Software";

/* ─── 1. IMPORT date din CSV ────────────────────────────── */
PROC IMPORT
    DATAFILE = "spotify_tracks.csv"
    OUT      = WORK.spotify_raw
    DBMS     = CSV
    REPLACE;
    GETNAMES = YES;
    GUESSINGROWS = 5000;
RUN;

/* ─── 2. FORMATE definite de utilizator ─────────────────── */
PROC FORMAT;
    VALUE pop_fmt
        LOW  -< 25 = "Necunoscut"
        25   -< 50 = "De nisa"
        50   -< 70 = "Popular"
        70   -< 85 = "Foarte popular"
        85  -  HIGH = "Viral";

    VALUE expl_fmt
        0 = "Non-explicit"
        1 = "Explicit";

    VALUE mode_fmt
        0 = "Minor"
        1 = "Major";
RUN;

/* ─── 3, 5, 7. DATA STEP: Masive (ARRAY), Functii, Iteratii ── */
DATA WORK.spotify_clean;
    SET WORK.spotify_raw;

    /* Utilizarea de masive (ARRAY) pentru inlocuirea valorilor lipsa */
    ARRAY num_vars[*] danceability energy valence acousticness speechiness liveness instrumentalness;
    DO i = 1 TO DIM(num_vars);
        IF MISSING(num_vars[i]) THEN num_vars[i] = 0.5; /* Valoare default */
    END;
    DROP i;

    /* ARRAY pentru scalare la 0-100 a caracteristicilor (care sunt 0-1) */
    ARRAY vars_01[*] danceability energy valence acousticness;
    ARRAY vars_pct[*] dance_pct energy_pct valence_pct acoustic_pct;
    
    DO j = 1 TO DIM(vars_01);
        vars_pct[j] = ROUND(vars_01[j] * 100, 0.1);
    END;
    DROP j;

    /* Procesare conditionala IF/ELSE IF */
    LENGTH pop_categ $20;
    IF popularity < 25 THEN pop_categ = "Necunoscut";
    ELSE IF popularity < 50 THEN pop_categ = "De nisa";
    ELSE IF popularity < 70 THEN pop_categ = "Popular";
    ELSE IF popularity < 85 THEN pop_categ = "Foarte popular";
    ELSE pop_categ = "Viral";

    /* Functii SAS (string, numerice, etc.) */
    track_len = LENGTH(STRIP(track_name));
    artist_upper = UPCASE(COMPRESS(artist_name));
    log_pop = LOG(popularity + 1);
    audio_mean = MEAN(OF danceability energy valence);
    audio_max = MAX(OF danceability energy valence);
    
    /* Format aplicat */
    FORMAT popularity pop_fmt. explicit expl_fmt. mode mode_fmt.;
RUN;

/* ─── 4. Creare Subseturi (OUTPUT multiplu) ─────────────── */
DATA WORK.subset_pop WORK.subset_rock WORK.subset_other;
    SET WORK.spotify_clean;
    IF genre = "pop" THEN OUTPUT WORK.subset_pop;
    ELSE IF genre = "rock" THEN OUTPUT WORK.subset_rock;
    ELSE OUTPUT WORK.subset_other;
RUN;

/* ─── 6, 8. SQL si MERGE (Combinarea datelor) ───────────── */
/* Pasul 1: PROC SQL pentru statistici agregate */
PROC SQL;
    CREATE TABLE WORK.genre_stats AS
    SELECT genre,
           COUNT(*) AS nr_piese,
           MEAN(popularity) AS pop_medie_gen
    FROM WORK.spotify_clean
    GROUP BY genre;
QUIT;

/* Pasul 2: Sortare necesara pentru MERGE */
PROC SORT DATA=WORK.spotify_clean; BY genre; RUN;
PROC SORT DATA=WORK.genre_stats; BY genre; RUN;

/* Pasul 3: Combinare cu MERGE */
DATA WORK.spotify_enriched;
    MERGE WORK.spotify_clean (IN=a) WORK.genre_stats (IN=b);
    BY genre;
    IF a; /* Pastram doar observatiile din tabelul principal */
    
    diferenta_pop = ROUND(popularity - pop_medie_gen, 0.1);
RUN;

/* ─── 9. Proceduri Statistice si Machine Learning ───────── */

TITLE2 "PROC MEANS: Statistici Deschise";
PROC MEANS DATA=WORK.spotify_enriched N MEAN STD MIN MAX MEDIAN;
    CLASS genre;
    VAR popularity energy danceability;
RUN;

TITLE2 "PROC FREQ: Frecvente";
PROC FREQ DATA=WORK.spotify_enriched;
    TABLES genre * pop_categ / CHISQ;
RUN;

TITLE2 "PROC CORR: Corelatii";
PROC CORR DATA=WORK.spotify_enriched;
    VAR popularity danceability energy valence tempo loudness;
RUN;

/* ML: Regresie Liniara Multipla */
TITLE2 "PROC REG: Predicția Popularității";
PROC REG DATA=WORK.spotify_enriched;
    MODEL popularity = danceability energy valence tempo loudness / SELECTION=STEPWISE;
RUN;
QUIT;

/* ML: Regresie Logistica (Clasificare) */
TITLE2 "PROC LOGISTIC: Prezicere Explicit/Non-Explicit";
PROC LOGISTIC DATA=WORK.spotify_enriched DESCENDING;
    MODEL explicit = danceability energy speechiness acousticness loudness;
RUN;

/* ML: Clusterizare K-Means */
TITLE2 "PROC FASTCLUS: Clusterizare (K-Means)";
PROC STANDARD DATA=WORK.spotify_enriched OUT=WORK.std_data MEAN=0 STD=1;
    VAR danceability energy valence tempo;
RUN;

PROC FASTCLUS DATA=WORK.std_data MAXCLUSTERS=4 OUT=WORK.clusters;
    VAR danceability energy valence tempo;
RUN;

/* ─── 10. Generare Grafice ──────────────────────────────── */

TITLE2 "Grafice: Distribuția Popularității (PROC SGPLOT)";
PROC SGPLOT DATA=WORK.spotify_enriched;
    HISTOGRAM popularity / FILLATTRS=(COLOR="#1db954");
    DENSITY popularity / LINEATTRS=(COLOR="red" THICKNESS=2);
RUN;

TITLE2 "Grafice: Boxplot Energie pe Gen (PROC SGPLOT)";
PROC SGPLOT DATA=WORK.spotify_enriched;
    VBOX energy / CATEGORY=genre FILLATTRS=(COLOR="lightblue");
RUN;

TITLE2 "Grafice: Panou Evolutie in Timp (PROC SGPANEL)";
PROC SGPANEL DATA=WORK.spotify_enriched (WHERE=(year >= 2000 AND genre IN ('pop', 'rock', 'hip-hop')));
    PANELBY genre;
    SCATTER X=year Y=popularity / MARKERATTRS=(SYMBOL=circlefilled COLOR="#1db954");
    REG X=year Y=popularity / LINEATTRS=(COLOR="red");
RUN;

/* ─── 11. Macro-uri SAS ─────────────────────────────────── */
%MACRO AnalizaGen(gen_nume=);
    TITLE2 "Analiza automata macro pentru genul: &gen_nume";
    PROC SGPLOT DATA=WORK.spotify_enriched;
        WHERE genre = "&gen_nume";
        SCATTER X=energy Y=danceability / GROUP=pop_categ;
    RUN;
%MEND AnalizaGen;

/* Rulam macro-ul pentru 2 genuri */
%AnalizaGen(gen_nume=pop);
%AnalizaGen(gen_nume=hip-hop);

/* ─── EXPORT rezultate finale ───────────────────────────── */
PROC EXPORT DATA=WORK.spotify_enriched
    OUTFILE = "spotify_final_sas.csv"
    DBMS    = CSV
    REPLACE;
RUN;

TITLE; TITLE2;
