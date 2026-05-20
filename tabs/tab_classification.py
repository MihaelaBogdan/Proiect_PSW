"""
tab_classification.py — Regresie Logistică cu Scikit-Learn
"""
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import plotly.express as px

def render():
    st.markdown("# 🤖 Clasificare (Regresie Logistică)")
    
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
            
            # Split
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
