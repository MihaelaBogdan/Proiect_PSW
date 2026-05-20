/*===========================================================
  PROIECT: Analiza Platformei Spotify — Programare SAS
  Cerinte acoperite (minim 8):
    1. Creare set de date SAS din fisiere externe (PROC IMPORT)
    2. Formate definite de utilizator (PROC FORMAT)
    3. Procesare iterativa si conditionala (DATA step + IF/DO)
    4. Creare subseturi de date (WHERE / OUTPUT)
    5. Functii SAS (ROUND, MEAN, COMPRESS, UPCASE, etc.)
    6. Combinarea seturilor de date (MERGE / SET)
    7. SQL in SAS (PROC SQL)
    8. Proceduri statistice (PROC MEANS, PROC FREQ, PROC CORR,
                             PROC REG, PROC CLUSTER, PROC LOGISTIC)
    9. Generare grafice (PROC SGPLOT, PROC SGPANEL, ODS GRAPHICS)
   10. Macro-uri SAS (%MACRO / %MEND)
===========================================================*/

/* ─── 0. Optiuni globale ─────────────────────────────────── */
OPTIONS NODATE NONUMBER PAGESIZE=60 LINESIZE=120;
ODS GRAPHICS ON;
TITLE "Proiect Analiza Spotify — Pachete Software";

/* ─── 1. IMPORT date din CSV ──────────────────────────────
   Cerinta: crearea unui set de date SAS din fisiere externe  */
PROC IMPORT
    DATAFILE = "spotify_tracks.csv"
    OUT      = WORK.spotify_raw
    DBMS     = CSV
    REPLACE;
    GETNAMES = YES;
    GUESSINGROWS = 5000;
RUN;

/* Verificare structura */
PROC CONTENTS DATA=WORK.spotify_raw; RUN;
PROC PRINT DATA=WORK.spotify_raw (OBS=5); RUN;

/* ─── 2. FORMATE definite de utilizator ───────────────────
   Cerinta: crearea si folosirea de formate definite de utilizator */
PROC FORMAT;
    /* Format popularitate in categorii */
    VALUE pop_fmt
        LOW  -< 25 = "Necunoscut"
        25   -< 50 = "De nisa"
        50   -< 70 = "Popular"
        70   -< 85 = "Foarte popular"
        85  -  HIGH = "Viral";

    /* Format explicit */
    VALUE expl_fmt
        0 = "Non-explicit"
        1 = "Explicit";

    /* Format mod muzical */
    VALUE mode_fmt
        0 = "Minor"
        1 = "Major";

    /* Format deceniu */
    VALUE dec_fmt
        LOW  -< 1970 = "Pre-1970"
        1970 -< 1980 = "Anii 70"
        1980 -< 1990 = "Anii 80"
        1990 -< 2000 = "Anii 90"
        2000 -< 2010 = "Anii 2000"
        2010 -< 2020 = "Anii 2010"
        2020 -  HIGH = "Anii 2020";
RUN;

/* ─── 3. DATA STEP — Procesare iterativa si conditionala ──
   Cerinta: procesare iterativa si conditionala a datelor     */
DATA WORK.spotify_clean;
    SET WORK.spotify_raw;

    /* Tratare valori lipsa (imputare cu valori fixe) */
    IF MISSING(danceability)     THEN danceability     = 0.60;
    IF MISSING(energy)           THEN energy           = 0.65;
    IF MISSING(tempo)            THEN tempo            = 120;
    IF MISSING(popularity)       THEN popularity       = 50;

    /* Tratare valori extreme */
    IF tempo      > 200 THEN tempo      = 120;
    IF popularity > 100 THEN popularity = 100;
    IF loudness   < -60 THEN loudness   = -8;

    /* Variabile derivate */
    duration_min  = ROUND(duration_ms / 60000, 0.01);
    decade        = FLOOR(year / 10) * 10;
    valence_pct   = ROUND(valence  * 100, 0.1);
    dance_pct     = ROUND(danceability * 100, 0.1);
    energy_pct    = ROUND(energy   * 100, 0.1);
    genre_upper   = UPCASE(COMPRESS(genre));

    /* Categorie popularitate (procesare conditionala) */
    LENGTH pop_categ $20;
    IF      popularity <  25 THEN pop_categ = "Necunoscut";
    ELSE IF popularity <  50 THEN pop_categ = "De nisa";
    ELSE IF popularity <  70 THEN pop_categ = "Popular";
    ELSE IF popularity <  85 THEN pop_categ = "Foarte popular";
    ELSE                          pop_categ = "Viral";

    /* Scor energie-dans combinat */
    energy_dance_score = ROUND((energy + danceability) / 2, 0.001);

    /* Aplicare formate */
    FORMAT popularity pop_fmt.
           explicit   expl_fmt.
           mode       mode_fmt.
           decade     dec_fmt.;
RUN;

PROC PRINT DATA=WORK.spotify_clean (OBS=10)
    VAR track_name artist_name genre year popularity
        pop_categ danceability energy duration_min;
RUN;

/* ─── 4. CREARE SUBSETURI ─────────────────────────────────
   Cerinta: crearea de subseturi de date                     */

/* Subset: doar piese populare (>= 70) */
DATA WORK.spotify_popular;
    SET WORK.spotify_clean;
    WHERE popularity >= 70;
RUN;

/* Subset: piese din ultimul deceniu */
DATA WORK.spotify_modern;
    SET WORK.spotify_clean;
    WHERE year >= 2015;
RUN;

/* Subset per gen cu OUTPUT multiplu */
DATA WORK.sp_pop
     WORK.sp_rock
     WORK.sp_hiphop
     WORK.sp_electronic
     WORK.sp_other;
    SET WORK.spotify_clean;
    SELECT (genre);
        WHEN ("pop")        OUTPUT WORK.sp_pop;
        WHEN ("rock")       OUTPUT WORK.sp_rock;
        WHEN ("hip-hop")    OUTPUT WORK.sp_hiphop;
        WHEN ("electronic") OUTPUT WORK.sp_electronic;
        OTHERWISE           OUTPUT WORK.sp_other;
    END;
RUN;

/* ─── 5. FUNCTII SAS ─────────────────────────────────────
   Cerinta: utilizarea de functii SAS                        */
DATA WORK.spotify_features;
    SET WORK.spotify_clean;

    /* Functii matematice */
    log_popularity     = LOG(popularity + 1);
    sqrt_instrumentaln = SQRT(instrumentalness);
    abs_loudness       = ABS(loudness);

    /* Functii statistice inline */
    audio_mean   = MEAN(danceability, energy, valence, acousticness);
    audio_max    = MAX(danceability, energy, valence);
    audio_min    = MIN(danceability, energy, valence);
    audio_range  = audio_max - audio_min;

    /* Functii string */
    track_len    = LENGTH(STRIP(track_name));
    artist_upper = UPCASE(artist_name);
    genre_len    = LENGTH(genre);

    /* Functii data/an */
    decade_label = CATS("Deceniu_", PUT(decade, 4.));

    KEEP track_id track_name artist_name genre year popularity
         log_popularity sqrt_instrumentaln abs_loudness
         audio_mean audio_max audio_min audio_range
         track_len artist_upper decade_label
         danceability energy valence tempo loudness
         acousticness instrumentalness speechiness liveness
         explicit mode duration_min pop_categ energy_dance_score;
RUN;

/* ─── 6. COMBINARE SETURI DE DATE ────────────────────────
   Cerinta: combinarea seturilor de date prin MERGE si SET   */

/* Cream un tabel de referinta cu statistici per gen */
PROC SQL;
    CREATE TABLE WORK.genre_stats AS
    SELECT genre,
           COUNT(*)           AS nr_piese,
           MEAN(popularity)   AS pop_medie,
           MEAN(energy)       AS energy_medie,
           MEAN(danceability) AS dance_medie,
           MEAN(valence)      AS valence_medie,
           MEAN(tempo)        AS tempo_mediu
    FROM WORK.spotify_clean
    GROUP BY genre
    ORDER BY genre;
QUIT;

/* Sortare inainte de MERGE */
PROC SORT DATA=WORK.spotify_features; BY genre; RUN;
PROC SORT DATA=WORK.genre_stats;      BY genre; RUN;

/* MERGE: adaugam statisticile genului la fiecare piesa */
DATA WORK.spotify_enriched;
    MERGE WORK.spotify_features (IN=a)
          WORK.genre_stats      (IN=b);
    BY genre;
    IF a;  /* pastram doar inregistrarile din setul principal */

    /* Popularitate relativa fata de media genului */
    pop_vs_gen = ROUND(popularity - pop_medie, 0.01);

    /* Etichetam piesa */
    LENGTH performanta $20;
    IF      pop_vs_gen >  15 THEN performanta = "Peste medie";
    ELSE IF pop_vs_gen < -15 THEN performanta = "Sub medie";
    ELSE                          performanta = "In medie";
RUN;

/* ─── 7. PROC SQL ────────────────────────────────────────
   Cerinta: utilizarea SQL in SAS                           */
TITLE2 "Analiza SQL: Top 10 genuri dupa popularitate medie";
PROC SQL OUTOBS=10;
    SELECT
        genre                        AS Gen,
        COUNT(*)                     AS Nr_Piese,
        ROUND(MEAN(popularity), 0.1) AS Pop_Medie,
        ROUND(MEAN(energy), 3)       AS Energy_Medie,
        ROUND(MEAN(danceability),3)  AS Dansabilitate_Medie,
        ROUND(MEAN(valence), 3)      AS Valenta_Medie,
        SUM(explicit)                AS Nr_Explicite,
        ROUND(MEAN(duration_min),2)  AS Durata_Medie_Min
    FROM WORK.spotify_enriched
    GROUP BY genre
    ORDER BY Pop_Medie DESC;
QUIT;

TITLE2 "SQL: Top 15 artisti dupa popularitate (min 3 piese)";
PROC SQL OUTOBS=15;
    SELECT
        artist_name                  AS Artist,
        genre                        AS Gen,
        COUNT(*)                     AS Nr_Piese,
        ROUND(MEAN(popularity), 0.1) AS Pop_Medie,
        ROUND(MAX(popularity), 0)    AS Pop_Max
    FROM WORK.spotify_enriched
    GROUP BY artist_name, genre
    HAVING COUNT(*) >= 3
    ORDER BY Pop_Medie DESC;
QUIT;

TITLE2 "SQL: Piese explicite vs non-explicite per gen";
PROC SQL;
    SELECT
        genre,
        SUM(explicit = 1)                                  AS Nr_Explicite,
        SUM(explicit = 0)                                  AS Nr_NonExplicite,
        ROUND(MEAN(explicit) * 100, 0.1)                   AS Procent_Explicite
    FROM WORK.spotify_enriched
    GROUP BY genre
    ORDER BY Procent_Explicite DESC;
QUIT;

TITLE2 "SQL JOIN: Piese populare cu statistici gen";
PROC SQL OUTOBS=20;
    SELECT  p.track_name, p.artist_name, p.genre,
            p.popularity, p.energy, p.danceability,
            g.pop_medie AS pop_medie_gen,
            ROUND(p.popularity - g.pop_medie, 0.1) AS diferenta_fata_de_gen
    FROM WORK.spotify_clean AS p
    INNER JOIN WORK.genre_stats AS g
        ON p.genre = g.genre
    WHERE p.popularity >= 80
    ORDER BY diferenta_fata_de_gen DESC;
QUIT;

/* ─── 8. MACRO-URI SAS ───────────────────────────────────
   Cerinta: utilizarea de macro-uri (proceduri reutilizabile) */

/* Macro 1: Raport statistic pentru un gen dat */
%MACRO raport_gen(gen=pop, var=popularity);
    TITLE2 "Macro raport_gen: Gen=&gen, Variabila=&var";
    PROC MEANS DATA=WORK.spotify_enriched N MEAN STD MIN MAX MEDIAN Q1 Q3;
        WHERE genre = "&gen";
        VAR &var;
        LABEL &var = "&var pentru genul &gen";
    RUN;
    PROC SGPLOT DATA=WORK.spotify_enriched (WHERE=(genre="&gen"));
        HISTOGRAM &var / FILLATTRS=(COLOR="#1db954") TRANSPARENCY=0.3;
        DENSITY &var / LINEATTRS=(COLOR="red" THICKNESS=2);
        TITLE "Distributia &var pentru genul &gen";
    RUN;
    TITLE2;
%MEND raport_gen;

/* Macro 2: Comparatie intre doua genuri */
%MACRO compara_genuri(gen1=pop, gen2=rock, var=popularity);
    TITLE2 "Comparatie &gen1 vs &gen2 — &var";
    DATA WORK._temp_comp;
        SET WORK.spotify_enriched;
        WHERE genre IN ("&gen1", "&gen2");
    RUN;
    PROC SGPLOT DATA=WORK._temp_comp;
        VBOX &var / CATEGORY=genre FILLATTRS=(COLOR="#1db954");
        TITLE "Boxplot &var: &gen1 vs &gen2";
    RUN;
    TITLE2;
%MEND compara_genuri;

/* Macro 3: Loop prin mai multe variabile */
%MACRO analiza_variabile(vars=danceability energy valence tempo);
    %LET n = %SYSFUNC(COUNTW(&vars));
    %DO i = 1 %TO &n;
        %LET var = %SCAN(&vars, &i);
        TITLE2 "Analiza variabilei: &var";
        PROC MEANS DATA=WORK.spotify_enriched N MEAN STD MIN MAX;
            CLASS genre;
            VAR &var;
        RUN;
    %END;
%MEND analiza_variabile;

/* Executare macro-uri */
%raport_gen(gen=pop,  var=popularity);
%raport_gen(gen=rock, var=energy);
%compara_genuri(gen1=pop, gen2=hip-hop, var=danceability);
%analiza_variabile(vars=danceability energy valence);

/* ─── 9. PROCEDURI STATISTICE ────────────────────────────
   Cerinta: proceduri statistice SAS                         */

TITLE2 "PROC MEANS — Statistici descriptive complete";
PROC MEANS DATA=WORK.spotify_enriched
    N NMISS MEAN STD MIN Q1 MEDIAN Q3 MAX SKEWNESS KURTOSIS;
    CLASS genre;
    VAR popularity danceability energy valence tempo loudness;
    OUTPUT OUT=WORK.means_out MEAN= STD= / AUTONAME;
RUN;

TITLE2 "PROC FREQ — Frecvente si tabele de contingenta";
PROC FREQ DATA=WORK.spotify_enriched;
    TABLES genre / PLOTS=FREQPLOT(ORIENT=HORIZONTAL SCALE=PERCENT);
    TABLES pop_categ / PLOTS=FREQPLOT;
    TABLES genre * pop_categ / CHISQ EXPECTED;
    TABLES explicit * genre  / CHISQ;
RUN;

TITLE2 "PROC CORR — Matrice de corelatie Pearson";
PROC CORR DATA=WORK.spotify_enriched
    PLOTS=MATRIX(HISTOGRAM NVAR=8);
    VAR popularity danceability energy valence
        tempo acousticness instrumentalness loudness;
RUN;

TITLE2 "PROC UNIVARIATE — Analiza distributiei popularitatii";
PROC UNIVARIATE DATA=WORK.spotify_enriched NORMAL PLOT;
    VAR popularity energy danceability;
    HISTOGRAM popularity / NORMAL(COLOR=red) CFILL=lightblue;
    PROBPLOT popularity / NORMAL(MU=EST SIGMA=EST);
    INSET N MEAN STD SKEWNESS KURTOSIS / FORMAT=6.3;
RUN;

/* ─── 9b. REGRESIE MULTIPLA (PROC REG) ───────────────────*/
TITLE2 "PROC REG — Regresia popularitatii dupa caracteristici audio";
PROC REG DATA=WORK.spotify_enriched PLOTS=DIAGNOSTICS;
    MODEL popularity = danceability energy valence tempo
                       acousticness loudness speechiness liveness
                       / SELECTION=STEPWISE SLENTRY=0.05 SLSTAY=0.05
                         R VIF;
    OUTPUT OUT=WORK.reg_out PREDICTED=pop_pred RESIDUAL=pop_resid;
RUN;
QUIT;

/* ─── 9c. REGRESIE LOGISTICA (PROC LOGISTIC) ─────────────*/
TITLE2 "PROC LOGISTIC — Prezicerea caracterului explicit";
/* Cream variabila binara clara */
DATA WORK.sp_logistic;
    SET WORK.spotify_enriched;
    explicit_bin = (explicit = 1);
RUN;

PROC LOGISTIC DATA=WORK.sp_logistic DESCENDING PLOTS(ONLY)=ROC;
    MODEL explicit_bin = danceability energy valence speechiness
                         acousticness tempo loudness
                         / SELECTION=BACKWARD SLSTAY=0.05 RSQUARE;
    OUTPUT OUT=WORK.logistic_out PREDICTED=prob_explicit;
RUN;

/* ─── 9d. ANALIZA CLUSTER (PROC CLUSTER + PROC FASTCLUS) ─*/
TITLE2 "PROC FASTCLUS — Clusterizare K-Means pe caracteristici audio";
/* Cream date normalizate pentru clustering */
PROC STANDARD DATA=WORK.spotify_enriched OUT=WORK.sp_standard MEAN=0 STD=1;
    VAR danceability energy valence tempo acousticness loudness
        instrumentalness speechiness;
RUN;

PROC FASTCLUS DATA=WORK.sp_standard MAXCLUSTERS=5 MAXITER=100
              OUT=WORK.sp_clustered OUTSTAT=WORK.cluster_stats;
    VAR danceability energy valence tempo acousticness loudness
        instrumentalness speechiness;
RUN;

/* Profil clustere */
TITLE2 "Profile clustere muzicale";
PROC MEANS DATA=WORK.sp_clustered MEAN;
    CLASS CLUSTER;
    VAR popularity danceability energy valence tempo acousticness;
RUN;

PROC FREQ DATA=WORK.sp_clustered;
    TABLES CLUSTER * genre / NOROW NOCOL NOPERCENT;
RUN;

/* ─── 10. GRAFICE (PROC SGPLOT, PROC SGPANEL) ───────────
   Cerinta: generare grafice SAS                            */

ODS GRAPHICS ON / WIDTH=900px HEIGHT=600px;

/* Grafic 1: Distributia popularitatii */
TITLE2 "Distributia popularitatii — Histograma cu curba normala";
PROC SGPLOT DATA=WORK.spotify_enriched;
    HISTOGRAM popularity / BINWIDTH=5 FILLATTRS=(COLOR="#1db954") TRANSPARENCY=0.2;
    DENSITY popularity / LINEATTRS=(COLOR="red" THICKNESS=2 PATTERN=1);
    DENSITY popularity / TYPE=KERNEL LINEATTRS=(COLOR="blue" THICKNESS=2);
    XAXIS LABEL="Popularitate";
    YAXIS LABEL="Frecventa";
    KEYLEGEND / LOCATION=INSIDE POSITION=TOPRIGHT;
RUN;

/* Grafic 2: Boxplot popularitate per gen */
TITLE2 "Boxplot: Popularitate per gen muzical";
PROC SGPLOT DATA=WORK.spotify_enriched;
    VBOX popularity / CATEGORY=genre FILLATTRS=(COLOR="#1db954")
                      WHISKERATTRS=(COLOR=gray);
    XAXIS LABEL="Gen muzical" FITPOLICY=ROTATETHIN;
    YAXIS LABEL="Popularitate (0-100)";
RUN;

/* Grafic 3: Scatter energie vs dansabilitate colorat per gen */
TITLE2 "Scatter: Energie vs Dansabilitate (colorat per gen)";
PROC SGPLOT DATA=WORK.spotify_enriched (WHERE=(genre IN ("pop","rock","hip-hop","electronic","jazz")));
    SCATTER X=energy Y=danceability / GROUP=genre
            MARKERATTRS=(SYMBOL=circlefilled SIZE=6)
            TRANSPARENCY=0.5;
    LINEPARM X=0 Y=0 SLOPE=1 / LINEATTRS=(COLOR=gray PATTERN=shortdash);
    XAXIS LABEL="Energie";
    YAXIS LABEL="Dansabilitate";
    KEYLEGEND / TITLE="Gen";
RUN;

/* Grafic 4: Bar chart popularitate medie per gen */
TITLE2 "Popularitate medie per gen — Bar Chart";
PROC SGPLOT DATA=WORK.genre_stats;
    HBAR genre / RESPONSE=pop_medie
                 FILLATTRS=(COLOR="#1db954")
                 DATALABEL;
    XAXIS LABEL="Popularitate medie" GRID;
    YAXIS LABEL="Gen muzical";
RUN;

/* Grafic 5: Trend popularitate in timp (per deceniu) */
TITLE2 "Evolutia popularitatii in timp (deceniu)";
PROC SQL;
    CREATE TABLE WORK.decade_trend AS
    SELECT decade, genre,
           MEAN(popularity) AS pop_medie
    FROM WORK.spotify_clean
    WHERE genre IN ("pop","rock","hip-hop","electronic","jazz")
    GROUP BY decade, genre
    ORDER BY decade, genre;
QUIT;

PROC SGPANEL DATA=WORK.decade_trend;
    PANELBY genre / COLUMNS=5;
    SERIES X=decade Y=pop_medie / MARKERS LINEATTRS=(COLOR="#1db954");
    COLAXIS LABEL="Deceniu" VALUES=(1960 TO 2020 BY 10);
    ROWAXIS LABEL="Popularitate medie";
RUN;

/* Grafic 6: Heatmap gen vs categorie popularitate */
TITLE2 "Heatmap: Gen vs Categorie Popularitate";
PROC FREQ DATA=WORK.spotify_enriched;
    TABLES genre * pop_categ / PLOTS=FREQPLOT(TWOWAY=STACKED SCALE=PERCENT);
RUN;

/* Grafic 7: Scatter matrix audio features */
TITLE2 "Scatter Matrix: Caracteristici audio principale";
PROC SGSCATTER DATA=WORK.spotify_enriched
               (WHERE=(genre IN ("pop","rock","hip-hop") AND _N_ <= 500));
    MATRIX danceability energy valence popularity /
           GROUP=genre DIAGONAL=(HISTOGRAM KERNEL);
RUN;

/* ─── EXPORT rezultate ────────────────────────────────── */
TITLE2 "Export: Seturi de date finale";
PROC EXPORT DATA=WORK.spotify_enriched
    OUTFILE = "spotify_enriched.csv"
    DBMS    = CSV
    REPLACE;
RUN;

PROC EXPORT DATA=WORK.genre_stats
    OUTFILE = "genre_statistics.csv"
    DBMS    = CSV
    REPLACE;
RUN;

PROC EXPORT DATA=WORK.sp_clustered
    OUTFILE = "spotify_clustered.csv"
    DBMS    = CSV
    REPLACE;
RUN;

ODS GRAPHICS OFF;
TITLE; TITLE2;

/*
  REZUMAT CERINTE ACOPERITE:
  ✅ 1.  PROC IMPORT — creare set date din fisier extern CSV
  ✅ 2.  PROC FORMAT — formate definite de utilizator (pop_fmt, expl_fmt, mode_fmt, dec_fmt)
  ✅ 3.  DATA step cu IF/ELSE/SELECT — procesare iterativa si conditionala
  ✅ 4.  WHERE / OUTPUT multiplu — creare subseturi de date
  ✅ 5.  Functii SAS: LOG, SQRT, ABS, MEAN, MAX, MIN, LENGTH, UPCASE, COMPRESS, ROUND, CATS, PUT
  ✅ 6.  MERGE si SET — combinare seturi de date
  ✅ 7.  PROC SQL — interogari, GROUP BY, JOIN, HAVING, subinterogari
  ✅ 8.  %MACRO / %MEND / %DO — macro-uri reutilizabile
  ✅ 9.  PROC MEANS, PROC FREQ, PROC CORR, PROC UNIVARIATE, PROC REG, PROC LOGISTIC, PROC FASTCLUS
  ✅ 10. PROC SGPLOT, PROC SGPANEL, PROC SGSCATTER — grafice diverse
*/
