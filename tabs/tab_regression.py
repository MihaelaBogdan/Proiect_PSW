"""
tab_regression.py — Regresie Multiplă cu Statsmodels
"""
import streamlit as st
import pandas as pd
import statsmodels.api as sm

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
      
      # Adăugăm constanta
      X = sm.add_constant(X)
      
      # Fit model
      model = sm.OLS(y, X).fit()
      
      st.success("Modelul a fost antrenat!")
      
      st.markdown("### Rezultatele Regresiei")
      # Afișăm summary într-un format text frumos
      st.text(model.summary().as_text())
      
      st.markdown("### Interpretare")
      st.write(f"R-squared: **{model.rsquared:.4f}**")
      st.write("Acest coeficient indică proporția varianței din 'popularitate' care poate fi explicată de variabilele selectate.")
