#!/usr/bin/env python3
"""
Enrichissement automatique de données d'entreprises avec les numéros SIREN.

Ce module utilise l'API gouvernementale française de recherche d'entreprises
pour enrichir automatiquement des fichiers CSV avec les numéros SIREN manquants.

Auteur: DJEDDOU Abdelatif
Licence: MIT
Version: 2.0.0
"""

import requests
import urllib.parse
import pandas as pd
import os
from time import sleep
import warnings
from typing import Tuple, Union

# Supprimer les avertissements pandas
warnings.filterwarnings('ignore', category=FutureWarning)

BASE_URL = "https://recherche-entreprises.api.gouv.fr"

def recherche_entreprise(api_base: str, terme: str, code_postal: str, per_page: int = 5) -> str:
    """
    Recherche une entreprise via l'API gouvernementale et retourne le SIREN du premier résultat.
    
    Args:
        api_base (str): URL de base de l'API
        terme (str): Nom de l'entreprise à rechercher
        code_postal (str): Code postal de l'entreprise
        per_page (int): Nombre de résultats par page (défaut: 5)
    
    Returns:
        str: Numéro SIREN trouvé ou None si aucun résultat
    
    Raises:
        requests.exceptions.RequestException: En cas d'erreur de requête HTTP
    """
    if not terme or not terme.strip():
        print(f"  > Terme de recherche vide, passage...")
        return None
        
    q = urllib.parse.quote(terme.strip(), safe="")
    url = (
        f"{api_base}/search"
        f"?q={q}"
        f"&code_postal={code_postal}"
        f"&per_page={per_page}"
    )
    
    try:
        r = requests.get(url)
        print(f"  > URL appelée : {r.request.url}")
        print(f"  > Status : {r.status_code}")
        r.raise_for_status()

        results = r.json().get("results", [])
        if not results:
            print(f"  > Aucun résultat pour « {terme} » dans le {code_postal}")
            return None

        premier = results[0]
        siren = premier.get("siren", "")
        nom = (
            premier.get("denomination")
            or premier.get("denominationUniteLegale")
            or premier.get("nom_raison_sociale")
            or premier.get("nom_complet")
            or "<nom inconnu>"
        )
        siege_cp = premier.get("siege", {}).get("code_postal", "<CP inconnu>")
        print(f"  > Match trouvé → SIREN: {siren} | Nom : {nom} | CP du siège : {siege_cp}")
        return siren
        
    except requests.exceptions.RequestException as e:
        print(f"  > Erreur lors de la requête : {e}")
        return None
    except Exception as e:
        print(f"  > Erreur inattendue : {e}")
        return None

def lire_csv(fichier_csv: str) -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame pandas nettoyé
    """
    if not os.path.exists(fichier_csv):
        raise FileNotFoundError(f"Le fichier {fichier_csv} n'existe pas")
    
    try:
        df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8-sig', dtype={'Code Postal': str})
        # Nettoyer les noms de colonnes (supprimer espaces en trop)
        df.columns = df.columns.str.strip()
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du fichier : {e}")
    
    if df.empty:
        raise ValueError("Le fichier CSV est vide")
    
    # Vérifier que les colonnes nécessaires existent
    colonnes_requises = ['Nom d\'usage', 'Code Postal', 'Num Siren']
    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' manquante dans le fichier")
    
    return df

def nettoyer_donnees_ligne(row: pd.Series) -> Tuple[str, str, str]:
    """
    Nettoie les données d'une ligne (nom, code postal, siren)
    """
    nom_usage = str(row['Nom d\'usage']).strip() if pd.notna(row['Nom d\'usage']) else ""
    code_postal_raw = row['Code Postal'] if pd.notna(row['Code Postal']) else ""
    
    # Nettoyer le code postal
    if pd.notna(code_postal_raw) and str(code_postal_raw) != 'nan':
        code_postal = str(code_postal_raw).strip()
        # Si c'est un nombre avec .0 à la fin, on supprime la partie décimale
        if code_postal.endswith('.0'):
            code_postal = code_postal[:-2]
    else:
        code_postal = ""
        
    siren_actuel = str(row['Num Siren']).strip() if pd.notna(row['Num Siren']) else ""
    
    return nom_usage, code_postal, siren_actuel

def valider_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valide et nettoie un DataFrame pour l'enrichissement SIREN
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide")
    
    # Nettoyer les noms de colonnes (supprimer espaces en trou)
    df.columns = df.columns.str.strip()
    
    # Vérifier que les colonnes nécessaires existent
    colonnes_requises = ['Nom d\'usage', 'Code Postal', 'Num Siren']
    for col in colonnes_requises:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' manquante dans le DataFrame")
    
    return df

def enrichir_sirens(input_data: Union[str, pd.DataFrame], verbose: bool = True) -> pd.DataFrame:
    """
    Enrichit un DataFrame avec les SIRENs manquants via l'API gouvernementale
    
    Args:
        input_data: Chemin vers le fichier CSV d'entrée OU DataFrame pandas
        verbose: Afficher les logs détaillés
    
    Returns:
        DataFrame pandas enrichi avec les SIRENs
    """
    # Étape 1: Obtenir le DataFrame
    if isinstance(input_data, str):
        # C'est un chemin de fichier
        if verbose:
            print(f"Lecture du fichier CSV : {input_data}")
        df = lire_csv(input_data)
    elif isinstance(input_data, pd.DataFrame):
        # C'est déjà un DataFrame
        if verbose:
            print("Traitement du DataFrame fourni")
        df = valider_dataframe(input_data.copy())
    else:
        raise TypeError("input_data doit être un chemin de fichier (str) ou un DataFrame pandas")
    
    if verbose:
        print(f"DataFrame chargé : {len(df)} lignes")
        print(f"Colonnes disponibles : {list(df.columns)}")
        print(f"Premières lignes du DataFrame :")
        print(df.head(3))
    
    # Étape 2: Enrichissement via API
    lignes_traitées = 0
    sirens_trouvés = 0
    
    for index, row in df.iterrows():
        nom_usage, code_postal, siren_actuel = nettoyer_donnees_ligne(row)
        
        if verbose:
            print(f"\n--- Ligne {index + 2} ---")
            print(f"Nom d'usage : '{nom_usage}'")
            print(f"Code postal : '{code_postal}'")
            print(f"SIREN actuel : '{siren_actuel}'")
        
        # Si le SIREN est déjà renseigné et non vide, on passe
        if siren_actuel and siren_actuel != 'nan' and siren_actuel != '0':
            if verbose:
                print("  > SIREN déjà renseigné, passage...")
            lignes_traitées += 1
            continue
        
        # Si nom d'usage ou code postal manquants, on passe
        if not nom_usage or nom_usage == 'nan' or not code_postal or code_postal == 'nan':
            if verbose:
                print("  > Nom d'usage ou code postal manquant, passage...")
            lignes_traitées += 1
            continue
        
        # Recherche du SIREN
        if verbose:
            print(f"  > Recherche de '{nom_usage}' dans '{code_postal}'...")
        
        siren_trouvé = recherche_entreprise(BASE_URL, nom_usage, code_postal)
        
        if siren_trouvé:
            df.at[index, 'Num Siren'] = str(siren_trouvé)
            sirens_trouvés += 1
            if verbose:
                print(f"  > SIREN mis à jour : {siren_trouvé}")
        else:
            if verbose:
                print("  > Aucun SIREN trouvé")
        
        lignes_traitées += 1
        
        # Pause pour éviter de surcharger l'API
        sleep(1)
    
    if verbose:
        print(f"\n=== RÉSUMÉ ENRICHISSEMENT ===")
        print(f"Lignes traitées : {lignes_traitées}")
        print(f"SIRENs trouvés : {sirens_trouvés}")
    
    return df

def sauvegarder_excel(df: pd.DataFrame, fichier_sortie: str) -> str:
    """
    Sauvegarde un DataFrame en Excel avec fallback CSV
    
    Returns:
        Chemin du fichier sauvegardé
    """
    try:
        df.to_excel(fichier_sortie, index=False, engine='openpyxl')
        print(f"Fichier Excel sauvegardé : {fichier_sortie}")
        return fichier_sortie
    except Exception as e:
        print(f"Erreur lors de la sauvegarde Excel : {e}")
        # Fallback en CSV si Excel échoue
        fichier_csv_sortie = fichier_sortie.replace('.xlsx', '.csv')
        df.to_csv(fichier_csv_sortie, sep=';', index=False, encoding='utf-8')
        print(f"Fichier CSV de secours sauvegardé : {fichier_csv_sortie}")
        return fichier_csv_sortie

def traiter_fichier_csv(fichier_csv: str):
    """
    Fonction legacy pour compatibilité - utilise maintenant enrichir_sirens
    """
    try:
        # Utilisation de la nouvelle fonction d'enrichissement
        df_enrichi = enrichir_sirens(fichier_csv)
        
        # Sauvegarde
        fichier_sortie = fichier_csv.replace('.csv', '_avec_sirens.xlsx')
        sauvegarder_excel(df_enrichi, fichier_sortie)
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    # Exemple d'utilisation avec le fichier d'exemple
    fichier_csv = "data/exemple.csv"
    if os.path.exists(fichier_csv):
        traiter_fichier_csv(fichier_csv)
    else:
        print(f"❌ Fichier d'exemple non trouvé : {fichier_csv}")
        print("💡 Créez un fichier CSV avec les colonnes : 'Nom d'usage', 'Code Postal', 'Num Siren'")
        print("📖 Consultez data/exemple.csv pour voir le format attendu")
