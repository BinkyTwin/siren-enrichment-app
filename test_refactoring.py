#!/usr/bin/env python3
"""
Script de test pour démontrer l'utilisation de la fonction enrichir_sirens refactorisée
"""

from main import enrichir_sirens, sauvegarder_excel
import pandas as pd
import os

def test_enrichissement_simple():
    """
    Test simple de la fonction enrichir_sirens
    """
    fichier_csv = "data/TEST LOTFI .csv"
    
    if not os.path.exists(fichier_csv):
        print(f"Erreur : Le fichier {fichier_csv} n'existe pas")
        return
    
    print("=== TEST DE LA FONCTION ENRICHIR_SIRENS ===\n")
    
    try:
        # Utilisation de la nouvelle fonction
        df_enrichi = enrichir_sirens(fichier_csv, verbose=True)
        
        print(f"\n=== DATAFRAME ENRICHI ===")
        print(f"Nombre de lignes : {len(df_enrichi)}")
        print(f"Colonnes : {list(df_enrichi.columns)}")
        
        # Compter les SIRENs renseignés
        sirens_renseignes = df_enrichi['Num Siren'].notna().sum()
        print(f"SIRENs renseignés : {sirens_renseignes}/{len(df_enrichi)}")
        
        # Sauvegarder le résultat
        fichier_sortie = "data/TEST_LOTFI_enrichi_refactored.xlsx"
        chemin_sauvegarde = sauvegarder_excel(df_enrichi, fichier_sortie)
        print(f"\nFichier sauvegardé : {chemin_sauvegarde}")
        
    except Exception as e:
        print(f"Erreur lors du test : {e}")

def test_enrichissement_silencieux():
    """
    Test de la fonction enrichir_sirens en mode silencieux
    """
    fichier_csv = "data/TEST LOTFI .csv"
    
    if not os.path.exists(fichier_csv):
        print(f"Erreur : Le fichier {fichier_csv} n'existe pas")
        return
    
    print("\n=== TEST EN MODE SILENCIEUX ===\n")
    
    try:
        # Mode silencieux (verbose=False)
        df_enrichi = enrichir_sirens(fichier_csv, verbose=False)
        
        print(f"Enrichissement terminé silencieusement")
        print(f"Lignes traitées : {len(df_enrichi)}")
        
        # Retourner le DataFrame pour utilisation ultérieure
        return df_enrichi
        
    except Exception as e:
        print(f"Erreur lors du test silencieux : {e}")
        return None

def demo_utilisation_programmmatique():
    """
    Démontre comment utiliser la fonction dans un contexte programmatique
    """
    print("\n=== DÉMONSTRATION UTILISATION PROGRAMMATIQUE ===\n")
    
    fichier_csv = "data/TEST LOTFI .csv"
    
    # Enrichissement
    df = enrichir_sirens(fichier_csv, verbose=False)
    
    if df is not None:
        # Analyse des résultats
        total_lignes = len(df)
        sirens_avant = df['Num Siren'].notna().sum()
        
        print(f"Analyse du DataFrame enrichi :")
        print(f"- Total lignes : {total_lignes}")
        print(f"- SIRENs renseignés : {sirens_avant}")
        print(f"- Taux de complétude : {(sirens_avant/total_lignes)*100:.1f}%")
        
        # Exemple d'opérations sur le DataFrame
        lignes_avec_siren = df[df['Num Siren'].notna() & (df['Num Siren'] != '')]
        print(f"- Lignes avec SIREN valide : {len(lignes_avec_siren)}")
        
        # Sauvegarde multiple formats
        sauvegarder_excel(df, "data/resultat_programmmatique.xlsx")

if __name__ == "__main__":
    # Test complet
    test_enrichissement_simple()
    
    # Test silencieux
    df_silent = test_enrichissement_silencieux()
    
    # Démo programmatique
    demo_utilisation_programmmatique()
    
    print("\n=== TOUS LES TESTS TERMINÉS ===")
