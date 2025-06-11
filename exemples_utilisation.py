#!/usr/bin/env python3
"""
Exemple d'utilisation de l'API refactorisée
"""

from main import enrichir_sirens, sauvegarder_excel, lire_csv
import pandas as pd

def exemple_utilisation_basique():
    """
    Exemple d'utilisation basique de la fonction enrichir_sirens
    """
    fichier_input = "data/TEST LOTFI .csv"
    
    # Enrichissement simple
    df_enrichi = enrichir_sirens(fichier_input)
    
    # Sauvegarde
    fichier_output = "data/resultat_enrichi.xlsx"
    sauvegarder_excel(df_enrichi, fichier_output)
    
    return df_enrichi

def exemple_utilisation_avancee():
    """
    Exemple d'utilisation avancée avec manipulation du DataFrame
    """
    fichier_input = "data/TEST LOTFI .csv"
    
    # 1. Lecture seule (sans enrichissement)
    df_original = lire_csv(fichier_input)
    print(f"DataFrame original : {len(df_original)} lignes")
    
    # 2. Enrichissement en mode silencieux
    df_enrichi = enrichir_sirens(fichier_input, verbose=False)
    print(f"DataFrame enrichi : {len(df_enrichi)} lignes")
    
    # 3. Analyse des changements
    sirens_avant = df_original['Num Siren'].notna().sum()
    sirens_après = df_enrichi['Num Siren'].notna().sum()
    nouveaux_sirens = sirens_après - sirens_avant
    
    print(f"SIRENs ajoutés : {nouveaux_sirens}")
    
    # 4. Filtrage des résultats
    lignes_enrichies = df_enrichi[
        df_enrichi['Num Siren'].notna() & 
        (df_enrichi['Num Siren'] != '') &
        (df_enrichi['Num Siren'] != '0')
    ]
    
    print(f"Lignes avec SIREN valide : {len(lignes_enrichies)}")
    
    # 5. Sauvegarde conditionnelle
    if nouveaux_sirens > 0:
        sauvegarder_excel(df_enrichi, "data/enrichissement_reussi.xlsx")
    else:
        print("Aucun nouveau SIREN trouvé, pas de sauvegarde")
    
    return df_enrichi, nouveaux_sirens

def exemple_integration_dans_pipeline():
    """
    Exemple d'intégration dans un pipeline de traitement de données
    """
    print("=== Pipeline de traitement ===")
    
    # Étape 1: Lecture et validation
    try:
        df = lire_csv("data/TEST LOTFI .csv")
        print(f"✓ Fichier lu : {len(df)} lignes")
    except Exception as e:
        print(f"✗ Erreur de lecture : {e}")
        return None
    
    # Étape 2: Enrichissement
    try:
        df_enrichi = enrichir_sirens("data/TEST LOTFI .csv", verbose=False)
        print(f"✓ Enrichissement terminé")
    except Exception as e:
        print(f"✗ Erreur d'enrichissement : {e}")
        return None
    
    # Étape 3: Validation des résultats
    sirens_valides = df_enrichi['Num Siren'].notna().sum()
    taux_completion = (sirens_valides / len(df_enrichi)) * 100
    
    print(f"✓ Taux de completion SIREN : {taux_completion:.1f}%")
    
    # Étape 4: Sauvegarde avec nom basé sur la qualité
    if taux_completion >= 80:
        nom_fichier = "data/dataset_haute_qualite.xlsx"
    elif taux_completion >= 50:
        nom_fichier = "data/dataset_qualite_moyenne.xlsx"
    else:
        nom_fichier = "data/dataset_a_verifier.xlsx"
    
    sauvegarder_excel(df_enrichi, nom_fichier)
    print(f"✓ Sauvegardé : {nom_fichier}")
    
    return df_enrichi

if __name__ == "__main__":
    print("=== EXEMPLES D'UTILISATION DE L'API REFACTORISÉE ===\n")
    
    # Exemple 1: Utilisation basique
    print("1. Utilisation basique :")
    df1 = exemple_utilisation_basique()
    
    print("\n" + "="*50 + "\n")
    
    # Exemple 2: Utilisation avancée
    print("2. Utilisation avancée :")
    df2, nouveaux = exemple_utilisation_avancee()
    
    print("\n" + "="*50 + "\n")
    
    # Exemple 3: Pipeline
    print("3. Intégration dans un pipeline :")
    df3 = exemple_integration_dans_pipeline()
    
    print("\n=== FIN DES EXEMPLES ===")
