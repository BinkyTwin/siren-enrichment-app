import streamlit as st
import pandas as pd
from io import BytesIO
from main import enrichir_sirens  # votre fonction refactorée

st.title("Enrichissement des SIREN")
st.markdown("Importez votre CSV et récupérez un fichier Excel enrichi.")

uploaded = st.file_uploader("Choisissez un CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, sep=';', dtype=str)
    if st.button("Lancer l'enrichissement"):
        with st.spinner("Traitement en cours…"):
            df_out = enrichir_sirens(df, verbose=False)  
            buffer = BytesIO()
            df_out.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
        st.success("Terminé ! Téléchargez votre fichier ci-dessous.")
        st.download_button("Télécharger le fichier enrichi", buffer, file_name="avec_sirens.xlsx")
