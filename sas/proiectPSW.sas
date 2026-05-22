/*1*/
PROC IMPORT
    DATAFILE = "/home/u64486141/ProiectSpotify/spotify_tracks.csv"
    OUT      = WORK.spotify
    DBMS     = CSV
    REPLACE;
    GETNAMES = YES;
    GUESSINGROWS = 5000;
RUN;

PROC PRINT DATA=WORK.spotify (OBS=5);
RUN;

/*2*/
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

PROC PRINT DATA=WORK.spotify (OBS=10);
    VAR track_name artist_name popularity explicit mode;
    FORMAT popularity pop_fmt.
           explicit expl_fmt.
           mode mode_fmt.;
    TITLE "Primele 10 piese cu formate aplicate";
RUN;

/*3*/
DATA WORK.spotify_clean;
    SET WORK.spotify;

    /* Procesare conditionala: clasificare pe categorii de popularitate */
    LENGTH pop_categ $20;
    IF popularity < 25 THEN pop_categ = "Necunoscut";
    ELSE IF popularity < 50 THEN pop_categ = "De nisa";
    ELSE IF popularity < 70 THEN pop_categ = "Popular";
    ELSE IF popularity < 85 THEN pop_categ = "Foarte popular";
    ELSE pop_categ = "Viral";

    /* Procesare conditionala: clasificare durata piesa */
    LENGTH durata_categ $10;
    IF duration_min < 2 THEN durata_categ = "Scurta";
    ELSE IF duration_min < 4 THEN durata_categ = "Medie";
    ELSE IF duration_min < 6 THEN durata_categ = "Lunga";
    ELSE durata_categ = "Foarte lunga";

    /* Procesare iterativa: numar caracteristici audio ridicate (>0.5) */
    audio_score = 0;
    DO WHILE (audio_score = 0);
        IF danceability > 0.5 THEN audio_score = audio_score + 1;
        IF energy > 0.5 THEN audio_score = audio_score + 1;
        IF valence > 0.5 THEN audio_score = audio_score + 1;
        IF acousticness > 0.5 THEN audio_score = audio_score + 1;
        LEAVE;
    END;
RUN;

PROC PRINT DATA=WORK.spotify_clean (OBS=10);
    VAR track_name popularity pop_categ duration_min durata_categ audio_score;
    TITLE "Primele 10 piese dupa procesare conditionala si iterativa";
RUN;

/*4*/
/* Subset 1: piese populare (popularity >= 70) */
DATA WORK.subset_populare;
    SET WORK.spotify_clean;
    WHERE popularity >= 70;
RUN;

/* Subset 2: piese explicit */
DATA WORK.subset_explicit;
    SET WORK.spotify_clean;
    WHERE explicit = 1;
RUN;

/* Subset 3: piese pop si hip-hop */
DATA WORK.subset_pop_hiphop;
    SET WORK.spotify_clean;
    WHERE genre IN ("pop", "hip-hop");
RUN;

/* Verificare dimensiuni subseturi */
PROC SQL;
    SELECT "Piese populare" AS subset, COUNT(*) AS nr_piese
    FROM WORK.subset_populare
    UNION ALL
    SELECT "Piese explicit" AS subset, COUNT(*) AS nr_piese
    FROM WORK.subset_explicit
    UNION ALL
    SELECT "Pop si Hip-Hop" AS subset, COUNT(*) AS nr_piese
    FROM WORK.subset_pop_hiphop;
QUIT;

/*5*/
DATA WORK.spotify_functii;
    SET WORK.spotify_clean;

    /* Functii numerice */
    popularitate_log = ROUND(LOG(popularity + 1), 0.01);
    durata_sec = INT(duration_min * 60);
    tempo_rotunjit = ROUND(tempo, 1);

    /* Functii statistice pe caracteristici audio */
    audio_medie = MEAN(danceability, energy, valence);
    audio_maxim = MAX(danceability, energy, valence);
    audio_minim = MIN(danceability, energy, valence);

    /* Functii de tip string */
    artist_upper = UPCASE(artist_name);
    genre_len = LENGTH(STRIP(genre));
    track_scurt = SUBSTR(track_name, 1, 20);

RUN;

PROC PRINT DATA=WORK.spotify_functii (OBS=10);
    VAR track_name artist_upper track_scurt tempo_rotunjit 
        audio_medie audio_maxim audio_minim durata_sec;
    TITLE "Primele 10 piese cu functii SAS aplicate";
RUN;

/*6*/
/* Pasul 1: cream un tabel cu statistici agregate pe gen */
PROC SQL;
    CREATE TABLE WORK.stats_gen AS
    SELECT genre,
           COUNT(*) AS nr_piese,
           ROUND(MEAN(popularity), 0.1) AS pop_medie,
           ROUND(MEAN(energy), 0.01) AS energy_medie
    FROM WORK.spotify_clean
    GROUP BY genre;
QUIT;

/* Pasul 2: sortam ambele seturi dupa cheia comuna */
PROC SORT DATA=WORK.spotify_clean; BY genre; RUN;
PROC SORT DATA=WORK.stats_gen; BY genre; RUN;

/* Pasul 3: combinam cu MERGE */
DATA WORK.spotify_enriched;
    MERGE WORK.spotify_clean (IN=a)
          WORK.stats_gen (IN=b);
    BY genre;
    IF a;
    diferenta_pop = ROUND(popularity - pop_medie, 0.1);
RUN;

/* Verificare rezultat */
PROC PRINT DATA=WORK.spotify_enriched (OBS=10);
    VAR track_name genre popularity pop_medie diferenta_pop energy_medie;
    TITLE "Primele 10 piese dupa combinarea seturilor de date";
RUN;

/*7*/
DATA WORK.spotify_array;
    SET WORK.spotify_enriched;

    /* ARRAY 1: verificare valori lipsa si inlocuire cu 0.5 */
    ARRAY audio_vars[5] danceability energy valence 
                        acousticness speechiness;
    DO i = 1 TO DIM(audio_vars);
        IF MISSING(audio_vars[i]) THEN audio_vars[i] = 0.5;
    END;
    DROP i;

    /* ARRAY 2: scalare la procente (0-1 devine 0-100) */
    ARRAY vars_orig[3] danceability energy valence;
    ARRAY vars_pct[3]  dance_pct energy_pct valence_pct;
    DO j = 1 TO DIM(vars_orig);
        vars_pct[j] = ROUND(vars_orig[j] * 100, 0.1);
    END;
    DROP j;

RUN;

PROC PRINT DATA=WORK.spotify_array (OBS=10);
    VAR track_name danceability dance_pct 
                   energy energy_pct 
                   valence valence_pct;
    TITLE "Primele 10 piese - valori originale vs procente (ARRAY)";
RUN;

/*8*/
/* PROC MEANS: statistici descriptive pe gen */
PROC MEANS DATA=WORK.spotify_array 
           N MEAN STD MIN MAX MEDIAN;
    CLASS genre;
    VAR popularity energy danceability;
    TITLE "Statistici descriptive pe gen muzical";
RUN;

/* PROC FREQ: distributia categoriilor de popularitate */
PROC FREQ DATA=WORK.spotify_array;
    TABLES pop_categ / NOCUM;
    TITLE "Distributia pieselor pe categorii de popularitate";
RUN;

/* PROC CORR: corelatii intre caracteristici audio si popularitate */
PROC CORR DATA=WORK.spotify_array NOSIMPLE;
    VAR popularity danceability energy valence tempo;
    TITLE "Corelatii intre popularitate si caracteristici audio";
RUN;

/*9*/
/* Pasul 1: standardizare date inainte de clusterizare */
PROC STANDARD DATA=WORK.spotify_array 
              OUT=WORK.spotify_scaled 
              MEAN=0 STD=1;
    VAR danceability energy valence tempo;
RUN;

/* Pasul 2: clusterizare K-Means cu 3 clustere */
PROC FASTCLUS DATA=WORK.spotify_scaled 
              OUT=WORK.spotify_clustere
              MAXCLUSTERS=3;
    VAR danceability energy valence tempo;
    TITLE "Clusterizare K-Means - 3 grupuri de piese";
RUN;

/* Pasul 3: verificare profil clustere */
PROC MEANS DATA=WORK.spotify_clustere 
           MEAN MAXDEC=2;
    CLASS CLUSTER;
    VAR danceability energy valence tempo popularity;
    TITLE "Profilul celor 3 clustere";
RUN;

/*10*/
/* Grafic 1: Histograma distributiei popularitatii */
PROC SGPLOT DATA=WORK.spotify_clustere;
    HISTOGRAM popularity / FILLATTRS=(COLOR="#1db954") 
                           BINWIDTH=5;
    DENSITY popularity / LINEATTRS=(COLOR="red" THICKNESS=2);
    XAXIS LABEL="Popularitate";
    YAXIS LABEL="Procent piese (%)";
    TITLE "Distributia popularitatii pieselor Spotify";
RUN;

/* Grafic 2: Bara orizontala - energia medie pe gen */
PROC SGPLOT DATA=WORK.spotify_clustere;
    HBAR genre / RESPONSE=energy 
                 STAT=MEAN
                 FILLATTRS=(COLOR="steelblue")
                 DATALABEL;
    XAXIS LABEL="Energie medie";
    TITLE "Energia medie pe gen muzical";
RUN;

/* Grafic 3: Scatter - dansabilitate vs popularitate colorat pe cluster */
PROC SGPLOT DATA=WORK.spotify_clustere;
    SCATTER X=danceability Y=popularity / 
            GROUP=CLUSTER
            MARKERATTRS=(SYMBOL=circlefilled SIZE=5)
            TRANSPARENCY=0.5;
    XAXIS LABEL="Dansabilitate";
    YAXIS LABEL="Popularitate";
    TITLE "Dansabilitate vs Popularitate pe clustere";
RUN;