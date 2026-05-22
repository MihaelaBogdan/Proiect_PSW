"""
tab_ml_extra.py - Random Forest, Feature Importance, Time Series
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def render():
    st.markdown("# Machine Learning Avansat & Time Series")

    if "processed_data" not in st.session_state:
        st.warning("Te rog sa rulezi mai intai Preprocesarea Datelor (tab-ul Preprocesare)!")
        return

    df = st.session_state.processed_data.copy()

    # --- 1. Random Forest Feature Importance ---
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

    # --- 2. Comparatie Modele: Random Forest vs Decision Tree ---
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

    # --- 3. Analiza Time Series: Evolutia Atributelor ---
    st.subheader("3. Analiza de tip Time Series (Medii Mobile per An)")
    st.write("Analizam evolutia medie a caracteristicilor acustice de-a lungul anilor de lansare.")

    time_df = df.groupby('year')[audio_feats + ['popularity']].mean().reset_index()
    time_df = time_df.sort_values('year')
    
    sel_ts = st.multiselect("Selecteaza variabilele pentru evolutia in timp:", 
                            audio_feats + ['popularity'], default=['energy', 'acousticness', 'danceability'])
    
    if sel_ts:
        fig_ts = go.Figure()
        for col in sel_ts:
            # Medie mobila pe 3 ani pentru a netezi seria
            smoothed = time_df[col].rolling(window=3, min_periods=1).mean()
            fig_ts.add_trace(go.Scatter(x=time_df['year'], y=smoothed, mode='lines', name=col))
            
        fig_ts.update_layout(title="Evolutia temporala (Medie mobila 3 ani)", 
                             xaxis_title="Anul Lansării", yaxis_title="Valoarea Medie a Atributului", template="plotly_dark")
        st.plotly_chart(fig_ts, use_container_width=True)

    # --- 4. Cross-tabulation si Heatmap Avansat ---
    st.subheader("4. Cross-Tabulation: Gen muzical si Mod (Major/Minor)")
    st.write("Analizam distributia genurilor muzicale pe tonalitati (Major = 1, Minor = 0).")
    
    cross_tab = pd.crosstab(df['genre'], df['mode'], normalize='index') * 100
    cross_tab = cross_tab.round(1)
    cross_tab.columns = ["Minor (%)", "Major (%)"]
    st.dataframe(cross_tab.style.background_gradient(cmap="Blues"), use_container_width=True)

