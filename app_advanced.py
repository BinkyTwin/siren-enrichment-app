import streamlit as st
import pandas as pd
from io import BytesIO
import time
from main import enrichir_sirens, valider_dataframe

# Configuration de la page
st.set_page_config(
    page_title="Enrichissement SIREN",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre et description
st.title("🏢 Enrichissement des SIREN")
st.markdown("""
Cette application permet d'enrichir automatiquement vos données d'entreprises avec leurs numéros SIREN 
en utilisant l'API gouvernementale française de recherche d'entreprises.

### Comment ça marche ?
1. **Importez** votre fichier CSV avec les colonnes : `Nom d'usage`, `Code Postal`, `Num Siren`
2. **Prévisualisez** vos données avant traitement
3. **Lancez** l'enrichissement automatique via l'API
4. **Téléchargez** le fichier Excel enrichi
""")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    st.subheader("Format d'entrée")
    separateur = st.selectbox(
        "Séparateur CSV",
        options=[";", ",", "\t"],
        index=0,
        help="Choisissez le séparateur utilisé dans votre fichier CSV"
    )
    
    encodage = st.selectbox(
        "Encodage",
        options=["utf-8-sig", "utf-8", "iso-8859-1", "cp1252"],
        index=0,
        help="Encodage du fichier CSV"
    )
    
    st.subheader("Traitement")
    mode_verbose = st.checkbox(
        "Mode détaillé",
        value=False,
        help="Afficher les détails du traitement (plus lent)"
    )
    
    delai_api = st.slider(
        "Délai entre requêtes (sec)",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.1,
        help="Temps d'attente entre chaque appel API"
    )

# Zone principale
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 Import du fichier")
    
    uploaded_file = st.file_uploader(
        "Choisissez votre fichier CSV",
        type=["csv"],
        help="Le fichier doit contenir les colonnes : 'Nom d'usage', 'Code Postal', 'Num Siren'"
    )

with col2:
    st.header("📊 Statistiques")
    if uploaded_file:
        # Conteneurs pour les métriques
        metric_container = st.container()

# Traitement du fichier uploadé
if uploaded_file:
    try:
        # Lecture du fichier
        df = pd.read_csv(
            uploaded_file, 
            sep=separateur, 
            encoding=encodage,
            dtype=str
        )
        
        # Validation basique
        df_validated = valider_dataframe(df)
        
        # Affichage des statistiques
        with metric_container:
            total_lignes = len(df_validated)
            sirens_existants = df_validated['Num Siren'].notna().sum()
            sirens_manquants = total_lignes - sirens_existants
            
            st.metric("Total lignes", total_lignes)
            st.metric("SIRENs existants", sirens_existants)
            st.metric("SIRENs manquants", sirens_manquants)
            
            if sirens_manquants > 0:
                st.success(f"✅ {sirens_manquants} SIREN(s) à enrichir")
            else:
                st.info("ℹ️ Tous les SIRENs sont déjà renseignés")
        
        # Prévisualisation des données
        st.header("👀 Prévisualisation des données")
        
        # Tabs pour différentes vues
        tab1, tab2, tab3 = st.tabs(["🔍 Aperçu", "❌ SIRENs manquants", "✅ SIRENs existants"])
        
        with tab1:
            st.dataframe(
                df_validated.head(10),
                use_container_width=True,
                hide_index=True
            )
            if len(df_validated) > 10:
                st.info(f"Affichage des 10 premières lignes sur {len(df_validated)} total")
        
        with tab2:
            sirens_manquants_df = df_validated[
                df_validated['Num Siren'].isna() | 
                (df_validated['Num Siren'] == '') |
                (df_validated['Num Siren'] == '0')
            ]
            if not sirens_manquants_df.empty:
                st.dataframe(sirens_manquants_df, use_container_width=True, hide_index=True)
                st.info(f"{len(sirens_manquants_df)} ligne(s) sans SIREN")
            else:
                st.success("Aucun SIREN manquant !")
        
        with tab3:
            sirens_existants_df = df_validated[
                df_validated['Num Siren'].notna() & 
                (df_validated['Num Siren'] != '') &
                (df_validated['Num Siren'] != '0')
            ]
            if not sirens_existants_df.empty:
                st.dataframe(sirens_existants_df, use_container_width=True, hide_index=True)
                st.info(f"{len(sirens_existants_df)} ligne(s) avec SIREN")
            else:
                st.warning("Aucun SIREN existant")
        
        # Section de traitement
        st.header("🚀 Enrichissement")
        
        if sirens_manquants > 0:
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🎯 Lancer l'enrichissement", type="primary", use_container_width=True):
                    # Progress bar et statistiques en temps réel
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    stats_container = st.container()
                    
                    start_time = time.time()
                    
                    try:
                        with st.spinner("Enrichissement en cours..."):
                            # Modification temporaire du délai dans main.py si nécessaire
                            import main
                            original_sleep = main.sleep
                            main.sleep = lambda x: time.sleep(delai_api)
                            
                            df_enrichi = enrichir_sirens(df_validated, verbose=mode_verbose)
                            
                            # Restaurer la fonction sleep originale
                            main.sleep = original_sleep
                        
                        # Calcul des résultats
                        end_time = time.time()
                        temps_traitement = end_time - start_time
                        
                        nouveaux_sirens = df_enrichi['Num Siren'].notna().sum() - sirens_existants
                        taux_succes = (nouveaux_sirens / sirens_manquants) * 100 if sirens_manquants > 0 else 0
                        
                        # Affichage des résultats
                        progress_bar.progress(1.0)
                        status_text.success("✅ Enrichissement terminé !")
                        
                        with stats_container:
                            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                            with col_stat1:
                                st.metric("Temps", f"{temps_traitement:.1f}s")
                            with col_stat2:
                                st.metric("Nouveaux SIRENs", nouveaux_sirens)
                            with col_stat3:
                                st.metric("Taux de succès", f"{taux_succes:.1f}%")
                            with col_stat4:
                                st.metric("Total SIRENs", df_enrichi['Num Siren'].notna().sum())
                        
                        # Stockage dans la session
                        st.session_state['df_enrichi'] = df_enrichi
                        st.session_state['enrichissement_effectue'] = True
                        
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'enrichissement : {str(e)}")
                        st.exception(e)
            
            with col_btn2:
                if st.button("📊 Test (5 lignes)", use_container_width=True):
                    st.info("Mode test - traitement des 5 premières lignes seulement")
                    df_test = df_validated.head(5)
                    
                    try:
                        with st.spinner("Test en cours..."):
                            df_test_enrichi = enrichir_sirens(df_test, verbose=True)
                        
                        st.success("✅ Test terminé !")
                        st.dataframe(df_test_enrichi, use_container_width=True, hide_index=True)
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors du test : {str(e)}")
            
            with col_btn3:
                st.download_button(
                    "💾 Télécharger original",
                    data=uploaded_file.getvalue(),
                    file_name=f"original_{uploaded_file.name}",
                    mime="text/csv",
                    use_container_width=True
                )
        
        else:
            st.info("ℹ️ Aucun enrichissement nécessaire - tous les SIRENs sont déjà renseignés")
            
            # Bouton pour télécharger quand même
            buffer = BytesIO()
            df_validated.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            
            st.download_button(
                "📥 Télécharger en Excel",
                data=buffer,
                file_name="donnees_completes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        # Section de téléchargement si enrichissement effectué
        if st.session_state.get('enrichissement_effectue', False) and 'df_enrichi' in st.session_state:
            st.header("📥 Téléchargement")
            
            df_enrichi = st.session_state['df_enrichi']
            
            col_dl1, col_dl2 = st.columns(2)
            
            with col_dl1:
                # Excel
                buffer_excel = BytesIO()
                df_enrichi.to_excel(buffer_excel, index=False, engine='openpyxl')
                buffer_excel.seek(0)
                
                st.download_button(
                    "📊 Télécharger Excel",
                    data=buffer_excel,
                    file_name="donnees_enrichies.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col_dl2:
                # CSV
                csv_enrichi = df_enrichi.to_csv(sep=separateur, index=False, encoding=encodage)
                
                st.download_button(
                    "📄 Télécharger CSV",
                    data=csv_enrichi,
                    file_name="donnees_enrichies.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Prévisualisation des données enrichies
            st.subheader("🔍 Aperçu des données enrichies")
            st.dataframe(df_enrichi.head(10), use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")
        st.info("Vérifiez que votre fichier contient bien les colonnes requises : 'Nom d'usage', 'Code Postal', 'Num Siren'")

else:
    # Interface d'accueil
    st.info("👆 Commencez par importer votre fichier CSV ci-dessus")
    
    # Exemple de format attendu
    st.subheader("📋 Format de fichier attendu")
    
    exemple_df = pd.DataFrame({
        "Nom d'usage": ["SOCIETE EXEMPLE 1", "ENTREPRISE TEST 2", "SARL DEMO 3"],
        "Code Postal": ["75001", "69000", "13000"],
        "Num Siren": ["", "123456789", ""]
    })
    
    st.dataframe(exemple_df, use_container_width=True, hide_index=True)
    st.caption("Exemple : Les lignes avec 'Num Siren' vide seront enrichies automatiquement")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    🔍 Données fournies par l'API gouvernementale française de recherche d'entreprises<br>
    🏢 Application d'enrichissement SIREN - Version avancée
</div>
""", unsafe_allow_html=True)
