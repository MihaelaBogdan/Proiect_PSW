import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
from data_loader import load_data, GENRE_COLORS
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

class tab_overview:
    @staticmethod
    def render():
        df = load_data()

        st.markdown("# Spotify Tracks — Prezentare Generală")
        st.markdown(
            "Analiză completă a unui dataset cu **5.000 de piese Spotify** cuprinzând "
            "15 genuri muzicale, caracteristici audio și metadate de popularitate."
        )

        c1, c2, c3, c4, c5 = st.columns(5)
        kpis = [
            (c1, len(df), "Piese totale"),
            (c2, df["genre"].nunique(), "Genuri"),
            (c3, df["artist_name"].nunique(), "Artiști"),
            (c4, f"{df['year'].min()}–{df['year'].max()}", "Interval ani"),
            (c5, f"{df['popularity'].mean():.1f}", "Popularitate medie"),
        ]
        for col, val, label in kpis:
            col.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='section-header'>Distribuție pe genuri</div>", unsafe_allow_html=True)
            genre_counts = df["genre"].value_counts().reset_index()
            genre_counts.columns = ["genre", "count"]
            fig_genre = px.bar(
                genre_counts,
                x="count", y="genre",
                orientation="h",
                color="genre",
                color_discrete_map=GENRE_COLORS,
                text="count",
                template="plotly_dark",
            )
            fig_genre.update_traces(textposition="outside")
            fig_genre.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                yaxis=dict(categoryorder="total ascending"),
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig_genre, use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>Piese lansate per deceniu</div>", unsafe_allow_html=True)
            df["decade"] = (df["year"] // 10) * 10
            decade_genre = df.groupby(["decade", "genre"]).size().reset_index(name="count")
            fig_time = px.area(
                decade_genre,
                x="decade", y="count", color="genre",
                color_discrete_map=GENRE_COLORS,
                template="plotly_dark",
            )
            fig_time.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                legend=dict(orientation="h", y=-0.25, x=0),
                margin=dict(l=20, r=20, t=20, b=60),
            )
            st.plotly_chart(fig_time, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<div class='section-header'>Popularitate medie per gen</div>", unsafe_allow_html=True)
            pop_genre = df.groupby("genre")["popularity"].mean().reset_index().sort_values("popularity", ascending=False)
            fig_pop = px.funnel(
                pop_genre,
                x="popularity", labels={"popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale", "genre": "Gen Muzical"}, y="genre",
                color="genre",
                color_discrete_map=GENRE_COLORS,
                template="plotly_dark",
            )
            fig_pop.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig_pop, use_container_width=True)

        with col4:
            st.markdown("<div class='section-header'>Profil audio mediu per gen</div>", unsafe_allow_html=True)
            radar_feats = ["danceability", "energy", "valence", "acousticness", "liveness", "speechiness"]
            genre_sel = st.multiselect(
                "Selectați genuri pentru radar:",
                options=sorted(df["genre"].unique()),
                default=["pop", "rock", "jazz", "electronic"],
                key="radar_genres",
            )
            if genre_sel:
                fig_radar = go.Figure()
                for g in genre_sel:
                    vals = df[df["genre"] == g][radar_feats].mean().tolist()
                    vals += [vals[0]]
                    fig_radar.add_trace(go.Scatterpolar(
                        r=vals,
                        theta=radar_feats + [radar_feats[0]],
                        fill="toself",
                        name=g,
                        line_color=GENRE_COLORS.get(g, "#ffffff"),
                        opacity=0.7,
                    ))
                fig_radar.update_layout(
                    polar=dict(bgcolor="rgba(0,0,0,0)",
                              radialaxis=dict(visible=True, range=[0, 1], color="#666")),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=True,
                    height=420,
                    template="plotly_dark",
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig_radar, use_container_width=True)

        st.markdown("<div class='section-header'>Preview Dataset</div>", unsafe_allow_html=True)
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search = st.text_input(" Caută artist sau piesă:", placeholder="Ex: Taylor Swift")
        with col_filter:
            genre_filter = st.selectbox("Filtrează gen:", ["Toate"] + sorted(df["genre"].unique()))

        df_view = df.copy()
        if search:
            mask = (df_view["artist_name"].str.contains(search, case=False, na=False) |
                    df_view["track_name"].str.contains(search, case=False, na=False))
            df_view = df_view[mask]
        if genre_filter != "Toate":
            df_view = df_view[df_view["genre"] == genre_filter]

        display_cols = ["track_name", "artist_name", "genre", "year", "popularity",
                        "danceability", "energy", "valence", "tempo", "duration_min"]
        st.dataframe(
            df_view[display_cols].rename(columns={
                "track_name": "Piesă", "artist_name": "Artist", "genre": "Gen",
                "year": "An", "popularity": "Popularitate", "danceability": "Dansabilitate",
                "energy": "Energie", "valence": "Valență", "tempo": "Tempo (BPM)",
                "duration_min": "Durată (min)"
            }).style.format({
                "Popularitate": "{:.0f}",
                "Dansabilitate": "{:.3f}", "Energie": "{:.3f}",
                "Valență": "{:.3f}", "Tempo (BPM)": "{:.1f}",
                "Durată (min)": "{:.2f}",
            }).background_gradient(subset=["Popularitate"], cmap="Greens"),
            use_container_width=True,
            height=350,
        )
        st.caption(f" {len(df_view):,} piese afișate din {len(df):,} total")

        with st.expander(" Structura completă a dataset-ului"):
            col_info = pd.DataFrame({
                "Coloană": df.columns,
                "Tip date": df.dtypes.astype(str).values,
                "Valori lipsă": df.isnull().sum().values,
                "Valori unice": [df[c].nunique() for c in df.columns],
                "Exemplu": [str(df[c].iloc[0]) for c in df.columns],
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)


class tab_preprocessing:
    @staticmethod
    def render():
        st.markdown("#  Preprocesare Date")
        st.markdown("În această secțiune tratăm valorile lipsă, codificăm datele categorice și scalăm variabilele numerice.")
        
        if "raw_data" not in st.session_state:
            st.session_state.raw_data = load_data()
        
        df = st.session_state.raw_data.copy()
        
        st.subheader("1. Tratarea valorilor lipsă și extreme")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Valori lipsă inițiale:")
            st.dataframe(df.isna().sum()[df.isna().sum() > 0])
            
        df['danceability'] = df['danceability'].fillna(df['danceability'].median())
        df['energy'] = df['energy'].fillna(df['energy'].median())
        df['tempo'] = df['tempo'].fillna(df['tempo'].median())
        df['popularity'] = df['popularity'].fillna(df['popularity'].median())
        
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


class tab_statistics:
    @staticmethod
    def render():
        st.markdown("# Statistici Descriptive & Grupări")

        if "processed_data" not in st.session_state:
            st.warning(" Te rog să rulezi mai întâi **Preprocesarea Datelor** (tab-ul Preprocesare Date)!")
            return

        df = st.session_state.processed_data.copy()

        st.subheader("1. Statistici descriptive generale (pandas describe)")
        numeric_cols = ["popularity", "danceability", "energy", "valence",
                        "tempo", "acousticness", "instrumentalness",
                        "speechiness", "liveness", "loudness", "duration_min"]
        desc = df[numeric_cols].describe().round(4)
        st.dataframe(desc.style.background_gradient(cmap="Greens"), use_container_width=True)
        st.caption("Rândurile arată: count, mean, std, min, 25%, 50%, 75%, max pentru fiecare coloană numerică.")

        st.subheader("2. Agregări cu pandas groupby")
        st.write("Calculăm mai multe statistici agregate pentru fiecare gen muzical, "
                 "utilizând funcțiile de grup: `mean`, `median`, `std`, `count`, `min`, `max`.")

        grouped = df.groupby("genre").agg(
            Popularitate_Medie = ("popularity",    "mean"),
            Popularitate_Mediana= ("popularity",    "median"),
            Energie_Medie    = ("energy",      "mean"),
            Dansabilitate_Medie = ("danceability",   "mean"),
            Valenta_Medie    = ("valence",      "mean"),
            Tempo_Mediu     = ("tempo",       "mean"),
            Durata_Medie_min  = ("duration_min",   "mean"),
            Nr_Piese      = ("track_id",     "count"),
            Nr_Artisti_Unici  = ("artist_name",    "nunique"),
            Explicit_Procent  = ("explicit",     "mean"),
        ).reset_index().sort_values("Popularitate_Medie", ascending=False).round(3)

        st.dataframe(grouped, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(grouped, x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}, y="Popularitate_Medie",
                         color="genre", text_auto=".1f",
                         title="Popularitate Medie per Gen",
                         template="plotly_dark")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.scatter(grouped, x="Energie_Medie", y="Popularitate_Medie",
                              size="Nr_Piese", color="genre",
                              text="genre", title="Energie vs. Popularitate (per Gen)",
                              template="plotly_dark")
            fig2.update_traces(textposition="top center")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("3. Funcția transform — Popularitate relativă față de media genului")
        st.write("Folosim `groupby().transform('mean')` pentru a calcula cât de populară "
                 "este fiecare piesă față de media genului ei.")
        df["pop_medie_gen"] = df.groupby("genre")["popularity"].transform("mean")
        df["pop_relativa"] = (df["popularity"] - df["pop_medie_gen"]).round(2)

        top_relative = df[["track_name", "artist_name", "genre",
                          "popularity", "pop_medie_gen", "pop_relativa"]]\
            .sort_values("pop_relativa", ascending=False).head(10)
        st.dataframe(top_relative, use_container_width=True)
        st.caption("pop_relativa > 0 = piesa e mai populară decât media genului ei.")

        st.subheader("4. Distribuții ale variabilelor audio")
        feat_sel = st.selectbox("Alege caracteristica:", 
                                ["popularity", "danceability", "energy", "valence",
                                 "tempo", "acousticness", "speechiness", "liveness"])
        col3, col4 = st.columns(2)
        with col3:
            fig_hist = px.histogram(df, x=feat_sel, nbins=50, color_discrete_sequence=["#1db954"],
                                    title=f"Histogramă: {feat_sel}", template="plotly_dark")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col4:
            fig_box = px.box(df, x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}, y=feat_sel, color="genre",
                             title=f"Boxplot: {feat_sel} per gen",
                             template="plotly_dark")
            fig_box.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_box, use_container_width=True)

        st.subheader("5. Matrice de corelație (Pearson)")
        st.write("Corelațiile dintre caracteristicile audio — `df.corr()` cu pandas.")
        corr_cols = ["popularity", "danceability", "energy", "valence",
                     "tempo", "acousticness", "instrumentalness",
                     "speechiness", "liveness", "loudness"]
        corr_matrix = df[corr_cols].corr().round(3)

        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            title="Heatmap Corelație Pearson",
            template="plotly_dark",
            aspect="auto"
        )
        fig_heat.update_layout(height=500)
        st.plotly_chart(fig_heat, use_container_width=True)

        st.subheader("6. Top 15 artiști după popularitate medie")
        top_artists = (
            df.groupby("artist_name")
              .agg(Pop_Medie=("popularity", "mean"),
                   Nr_Piese=("track_id", "count"))
              .query("Nr_Piese >= 3")
              .sort_values("Pop_Medie", ascending=False)
              .head(15)
              .reset_index()
              .round(1)
        )
        fig_art = px.bar(top_artists, x="Pop_Medie", y="artist_name",
                         orientation="h", color="Pop_Medie",
                         color_continuous_scale="Greens",
                         text="Pop_Medie",
                         title="Top 15 Artiști (min. 3 piese)",
                         template="plotly_dark")
        fig_art.update_layout(yaxis=dict(categoryorder="total ascending"), showlegend=False)
        st.plotly_chart(fig_art, use_container_width=True)

        st.subheader("7. Evoluție popularitate în timp (deceniu)")
        df["decade"] = (df["year"] // 10) * 10
        trend = df.groupby(["decade", "genre"])["popularity"].mean().reset_index()
        genres_sel = st.multiselect("Filtrează genuri:", sorted(df["genre"].unique()),
                                    default=["pop", "rock", "hip-hop", "electronic"])
        trend_filtered = trend[trend["genre"].isin(genres_sel)]
        fig_trend = px.line(trend_filtered, x="decade", y="popularity", color="genre",
                            markers=True, title="Popularitate Medie per Deceniu",
                            template="plotly_dark")
        st.plotly_chart(fig_trend, use_container_width=True)


class tab_clustering:
    @staticmethod
    def render():
        st.markdown("# Clusterizare (K-Means)")
        
        if "processed_data" not in st.session_state:
            st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
            return
            
        df = st.session_state.processed_data
        
        st.write("Vom grupa piesele în clustere folosind caracteristici audio.")
        
        features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'loudness']
        X = df[features]
        
        n_clusters = st.slider("Număr de clustere (K)", min_value=2, max_value=10, value=4)
        
        if st.button("Rulează K-Means"):
            with st.spinner("Antrenare model K-Means..."):
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                df['Cluster'] = kmeans.fit_predict(X)
                
                pca = PCA(n_components=2)
                pca_components = pca.fit_transform(X)
                
                df['PCA1'] = pca_components[:, 0]
                df['PCA2'] = pca_components[:, 1]
                
                st.success("Clusterizare completă!")
                
                fig = px.scatter(df, x='PCA1', y='PCA2', color=df['Cluster'].astype(str),
                                 hover_data=['track_name', 'artist_name', 'genre'],
                                 template="plotly_dark", title="Vizualizare Clustere (PCA)")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Caracteristicile mediilor pe fiecare cluster")
                cluster_means = df.groupby('Cluster')[features].mean()
                st.dataframe(cluster_means)


class tab_regression:
    @staticmethod
    def render():
        st.markdown("# Regresie Multiplă (Statsmodels)")
        
        if "processed_data" not in st.session_state:
            st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
            return
            
        df = st.session_state.processed_data
        
        st.write("Vom prezice **popularitatea** unei piese folosind caracteristicile sale audio.")
        
        independent_vars = st.multiselect(
            "Alege variabilele independente (X):",
            ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness', 'liveness'],
            default=['danceability', 'energy', 'loudness']
        )
        
        if st.button("Construiește Modelul"):
            if len(independent_vars) == 0:
                st.error("Selectează cel puțin o variabilă!")
                return
                
            with st.spinner("Se calculează regresia..."):
                X = df[independent_vars]
                y = df['popularity']
                
                X = sm.add_constant(X)
                
                model = sm.OLS(y, X).fit()
                
                st.success("Modelul a fost antrenat!")
                
                st.markdown("### Rezultatele Regresiei")
                st.text(model.summary().as_text())
                
                st.markdown("### Interpretare")
                st.write(f"R-squared: **{model.rsquared:.4f}**")
                st.write("Acest coeficient indică proporția varianței din 'popularitate' care poate fi explicată de variabilele selectate.")


class tab_classification:
    @staticmethod
    def render():
        st.markdown("#  Clasificare (Regresie Logistică)")
        
        if "processed_data" not in st.session_state:
            st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
            return
            
        df = st.session_state.processed_data.copy()
        
        st.write("Scop: Prezicerea dacă o piesă este explicită (`explicit` = 1 sau 0) pe baza caracteristicilor sale audio.")
        
        features = ['danceability', 'energy', 'valence', 'speechiness', 'acousticness']
        
        st.write("Variabile folosite pentru predicție:")
        st.write(", ".join(features))
        
        if st.button("Antrenează Regresia Logistică"):
            with st.spinner("Se antrenează modelul..."):
                X = df[features]
                y = df['explicit']
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                
                st.success("Model antrenat cu succes!")
                
                st.metric("Acuratețea modelului pe datele de test", f"{acc*100:.2f}%")
                
                st.markdown("### Raport de clasificare")
                report = classification_report(y_test, y_pred, output_dict=True)
                st.dataframe(pd.DataFrame(report).transpose())
                
                st.markdown("### Matricea de confuzie")
                cm = confusion_matrix(y_test, y_pred)
                fig = px.imshow(cm, text_auto=True, color_continuous_scale='Blues',
                                labels=dict(x="Predicție", y="Adevărat"),
                                x=['Non-Explicit', 'Explicit'], y=['Non-Explicit', 'Explicit'],
                                title="Confusion Matrix")
                st.plotly_chart(fig)


class tab_advanced:
    @staticmethod
    def render():
        st.markdown("# Analiză Avansată")

        if "processed_data" not in st.session_state:
            st.warning(" Te rog să rulezi mai întâi **Preprocesarea Datelor** (tab-ul Preprocesare Date)!")
            return

        df = st.session_state.processed_data.copy()
        audio_feats = ["danceability", "energy", "valence", "tempo",
                       "acousticness", "instrumentalness", "speechiness", "liveness"]

        st.subheader("1. Reducerea dimensionalității — PCA 2D")
        st.write("Reducem cele 8 caracteristici audio la **2 componente principale** cu `sklearn.decomposition.PCA` "
                 "pentru a vizualiza spațiul muzical.")

        X = df[audio_feats].dropna()
        sc = StandardScaler()
        X_scaled = sc.fit_transform(X)

        pca = PCA(n_components=2)
        components = pca.fit_transform(X_scaled)
        var_exp = pca.explained_variance_ratio_

        df_pca = df.loc[X.index].copy()
        df_pca["PC1"] = components[:, 0]
        df_pca["PC2"] = components[:, 1]

        fig_pca = px.scatter(
            df_pca, x="PC1", labels={"PC1": "Componenta Principală 1", "PC2": "Componenta Principală 2", "genre": "Gen Muzical", "tip": "Tip (Normal/Outlier)"}, y="PC2", color="genre",
            hover_data=["track_name", "artist_name", "popularity"],
            title=f"PCA 2D — Varianta explicată: PC1={var_exp[0]:.1%}, PC2={var_exp[1]:.1%}",
            template="plotly_dark", opacity=0.7,
        )
        st.plotly_chart(fig_pca, use_container_width=True)

        st.info(f" PCA explică **{sum(var_exp):.1%}** din varianța totală cu doar 2 componente.")

        st.subheader("2. Contribuția variabilelor la componentele principale (Loadings)")
        loadings = pd.DataFrame(
            pca.components_.T,
            index=audio_feats,
            columns=["PC1", "PC2"]
        ).round(3)
        fig_load = px.bar(loadings, barmode="group",
                          title="PCA Loadings — Contribuția fiecărei caracteristici",
                          template="plotly_dark", color_discrete_sequence=["#1db954", "#e91e63"])
        st.plotly_chart(fig_load, use_container_width=True)
        st.dataframe(loadings, use_container_width=True)

        st.subheader("3. Detecție automată a Outlierilor — Isolation Forest")
        st.write("Folosim `IsolationForest` din scikit-learn pentru a identifica piesele "
                 "cu caracteristici audio atipice (anomalii).")

        contamination = st.slider("Proporție estimată de outlieri:", 0.01, 0.15, 0.05, 0.01)
        iso = IsolationForest(contamination=contamination, random_state=42)
        df_pca["outlier"] = iso.fit_predict(X_scaled)
        df_pca["tip"] = df_pca["outlier"].map({1: "Normal", -1: "Outlier"})

        n_out = (df_pca["outlier"] == -1).sum()
        st.metric("Outlieri detectați", n_out, f"{n_out/len(df_pca):.1%} din date")

        fig_out = px.scatter(
            df_pca, x="PC1", labels={"PC1": "Componenta Principală 1", "PC2": "Componenta Principală 2", "genre": "Gen Muzical", "tip": "Tip (Normal/Outlier)"}, y="PC2", color="tip",
            color_discrete_map={"Normal": "#1db954", "Outlier": "#e91e63"},
            hover_data=["track_name", "artist_name", "genre"],
            title="Outlieri detectați cu Isolation Forest (spațiu PCA)",
            template="plotly_dark", opacity=0.7,
        )
        st.plotly_chart(fig_out, use_container_width=True)

        st.subheader("Piesele outlier identificate")
        outliers_df = df_pca[df_pca["outlier"] == -1][
            ["track_name", "artist_name", "genre", "popularity",
             "tempo", "loudness", "instrumentalness"]
        ].head(20)
        st.dataframe(outliers_df, use_container_width=True)

        st.subheader("4. Distribuție popularitate per gen — Violin Plot")
        fig_vio = px.violin(
            df, x="genre", labels={"genre": "Gen Muzical", "count": "Număr Piese", "popularity": "Popularitate", "energy": "Energie", "danceability": "Dansabilitate", "valence": "Valență", "tempo": "Tempo", "acousticness": "Acusticitate", "speechiness": "Vocale"}, y="popularity", color="genre",
            box=True, points="outliers",
            title="Violin Plot: Distribuția popularității per gen muzical",
            template="plotly_dark",
        )
        fig_vio.update_layout(showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig_vio, use_container_width=True)

        st.subheader("5. Scatter Matrix (Pair Plot) — relații între variabile")
        cols_sel = st.multiselect(
            "Selectează variabilele pentru scatter matrix:",
            audio_feats + ["popularity"],
            default=["danceability", "energy", "valence", "popularity"],
        )
        if len(cols_sel) >= 2:
            fig_scat = px.scatter_matrix(
                df.sample(min(500, len(df)), random_state=42),
                dimensions=cols_sel, color="genre",
                title="Scatter Matrix — caracteristici audio",
                template="plotly_dark",
                opacity=0.5,
            )
            fig_scat.update_layout(height=600)
            st.plotly_chart(fig_scat, use_container_width=True)


class tab_ml_extra:
    @staticmethod
    def render():
        st.markdown("# Machine Learning Avansat & Time Series")

        if "processed_data" not in st.session_state:
            st.warning("Te rog sa rulezi mai intai Preprocesarea Datelor (tab-ul Preprocesare Date)!")
            return

        df = st.session_state.processed_data.copy()

        st.subheader("1. Random Forest - Importanta Variabilelor (Feature Importance)")
        st.write("Antrenam un model Random Forest Regressor pentru a vedea care caracteristici audio "
                 "sunt cele mai importante in determinarea popularitatii.")

        audio_feats = ["danceability", "energy", "valence", "tempo", 
                       "acousticness", "instrumentalness", "speechiness", "liveness", "loudness"]
        
        X = df[audio_feats]
        y = df["popularity"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        
        r2_rf = r2_score(y_test, y_pred_rf)
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        
        col1, col2 = st.columns(2)
        col1.metric("R-squared (Random Forest)", f"{r2_rf:.3f}")
        col2.metric("Mean Squared Error", f"{mse_rf:.2f}")

        importance = pd.DataFrame({
            'Feature': audio_feats,
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=True)

        fig_imp = px.bar(importance, x='Importance', y='Feature', orientation='h',
                         title="Importanta Caracteristicilor Audio (Random Forest)",
                         template="plotly_dark", color='Importance', color_continuous_scale="Viridis")
        st.plotly_chart(fig_imp, use_container_width=True)

        st.subheader("2. Comparatie Modele Predicție (Random Forest vs Decision Tree)")
        st.write("Comparam performanta unui arbore de decizie simplu cu algoritmul de tip ensemble (Random Forest).")

        dt = DecisionTreeRegressor(max_depth=10, random_state=42)
        dt.fit(X_train, y_train)
        y_pred_dt = dt.predict(X_test)
        r2_dt = r2_score(y_test, y_pred_dt)

        comp_df = pd.DataFrame({
            "Model": ["Decision Tree", "Random Forest"],
            "R-squared": [r2_dt, r2_rf]
        })
        
        fig_comp = px.bar(comp_df, x="Model", labels={"Model": "Model de Predicție", "R-squared": "Scor R-Pătrat"}, y="R-squared", color="Model",
                          title="Comparatie R-squared: Arbori vs Pădure", template="plotly_dark")
        st.plotly_chart(fig_comp, use_container_width=True)

        st.subheader("3. Analiza de tip Time Series (Medii Mobile per An)")
        st.write("Analizam evolutia medie a caracteristicilor acustice de-a lungul anilor de lansare.")

        time_df = df.groupby('year')[audio_feats + ['popularity']].mean().reset_index()
        time_df = time_df.sort_values('year')
        
        sel_ts = st.multiselect("Selecteaza variabilele pentru evolutia in timp:", 
                                audio_feats + ['popularity'], default=['energy', 'acousticness', 'danceability'])
        
        if sel_ts:
            fig_ts = go.Figure()
            for col in sel_ts:
                smoothed = time_df[col].rolling(window=3, min_periods=1).mean()
                fig_ts.add_trace(go.Scatter(x=time_df['year'], y=smoothed, mode='lines', name=col))
                
            fig_ts.update_layout(title="Evolutia temporala (Medie mobila 3 ani)", 
                                 xaxis_title="Anul Lansării", yaxis_title="Valoarea Medie a Atributului", template="plotly_dark")
            st.plotly_chart(fig_ts, use_container_width=True)

        st.subheader("4. Cross-Tabulation: Gen muzical si Mod (Major/Minor)")
        st.write("Analizam distributia genurilor muzicale pe tonalitati (Major = 1, Minor = 0).")
        
        cross_tab = pd.crosstab(df['genre'], df['mode'], normalize='index') * 100
        cross_tab = cross_tab.round(1)
        cross_tab.columns = ["Minor (%)", "Major (%)"]
        st.dataframe(cross_tab.style.background_gradient(cmap="Blues"), use_container_width=True)


class tab_viz_extra:
    @staticmethod
    def render():
        st.markdown("# Vizualizări Avansate și Interactive")

        if "processed_data" not in st.session_state:
            st.warning("Te rog să rulezi mai întâi Preprocesarea Datelor!")
            return

        df = st.session_state.processed_data.copy()

        if 'decade' not in df.columns:
            df['decade'] = (df['year'] // 10) * 10

        st.subheader("1. Treemap: Structura Genurilor și Popularitatea")
        st.write("Mărimea dreptunghiului reprezintă numărul de piese, iar culoarea indică popularitatea medie.")
        
        treemap_data = df.groupby('genre').agg(
            Număr_Piese=('track_id', 'count'),
            Popularitate_Medie=('popularity', 'mean')
        ).reset_index()

        fig_tree = px.treemap(treemap_data, 
                              path=['genre'], 
                              values='Număr_Piese',
                              color='Popularitate_Medie', 
                              color_continuous_scale='Viridis',
                              title="Treemap Genuri Muzicale",
                              labels={"genre": "Gen Muzical", "Număr_Piese": "Număr Piese", "Popularitate_Medie": "Popularitate Medie"})
        st.plotly_chart(fig_tree, use_container_width=True)

        st.subheader("2. Sunburst Chart: Evoluția Ierarhică (Deceniu  Gen  Explicit)")
        st.write("Navighează ierarhic dând click pe componentele cercului pentru a explora structura datelor.")
        
        sunburst_df = df[df['genre'].isin(df['genre'].value_counts().head(8).index)]
        sunburst_df['Explicit_Label'] = sunburst_df['explicit'].map({1: 'Explicit', 0: 'Curat'})
        
        fig_sunburst = px.sunburst(sunburst_df, 
                                   path=['decade', 'genre', 'Explicit_Label'], 
                                   values='popularity',
                                   color='energy', 
                                   color_continuous_scale='RdBu_r',
                                   title="Sunburst: Distribuția Popularității și Energiei",
                                   labels={"decade": "Deceniu", "genre": "Gen Muzical", "energy": "Energie"})
        st.plotly_chart(fig_sunburst, use_container_width=True)

        st.subheader("3. Scatter Plot 3D: Exploram spațiul 3D al muzicii")
        st.write("Analizăm modul în care 3 variabile principale interacționează în spațiu tridimensional.")
        
        sample_df = df.sample(n=min(1000, len(df)), random_state=42)
        
        fig_3d = px.scatter_3d(sample_df, 
                               x='danceability', 
                               y='energy', 
                               z='popularity',
                               color='genre',
                               hover_name='track_name',
                               title="3D Scatter: Dansabilitate vs Energie vs Popularitate",
                               labels={"danceability": "Dansabilitate", "energy": "Energie", "popularity": "Popularitate", "genre": "Gen Muzical"},
                               opacity=0.7)
        fig_3d.update_layout(scene=dict(bgcolor='#0a0a0f'), template="plotly_dark")
        st.plotly_chart(fig_3d, use_container_width=True)

        st.subheader("4. Density Contour: Harta de Densitate 2D (Tempo vs Energie)")
        st.write("Arată zonele de concentrare maximă a pieselor, similar cu o hartă topografică.")
        
        fig_contour = px.density_contour(df, 
                                         x="tempo", 
                                         y="energy", 
                                         color="genre",
                                         title="Densitate 2D: Unde se concentrează genurile?",
                                         labels={"tempo": "Tempo (BPM)", "energy": "Energie", "genre": "Gen Muzical"})
        fig_contour.update_traces(contours_coloring="fill", contours_showlabels=True)
        st.plotly_chart(fig_contour, use_container_width=True)

        st.subheader("5. Polar/Radar Chart (Top Artiști)")
        st.write("Comparăm semnătura acustică (amprenta muzicală) a celor mai populari artiști.")
        
        top_artists = df.groupby('artist_name')['popularity'].mean().nlargest(3).index
        artist_df = df[df['artist_name'].isin(top_artists)]
        
        metrics = ['danceability', 'energy', 'valence', 'acousticness', 'liveness', 'speechiness']
        artist_means = artist_df.groupby('artist_name')[metrics].mean().reset_index()

        fig_radar = go.Figure()
        for i, row in artist_means.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=row[metrics].values.tolist() + [row[metrics].values.tolist()[0]], 
                theta=[m.capitalize() for m in metrics] + [metrics[0].capitalize()],
                fill='toself',
                name=row['artist_name']
            ))
            
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Amprenta Acustică (Radar Chart)",
            template="plotly_dark"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
