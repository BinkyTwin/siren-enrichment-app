import requests
import urllib.parse
import pandas as pd
import os
from time import sleep
import warnings

# Supprimer les avertissements pandas
warnings.filterwarnings('ignore', category=FutureWarning)

BASE_URL = "https://recherche-entreprises.api.gouv.fr"

def recherche_entreprise(api_base, terme, code_postal, per_page=5):
    """
    Recherche une entreprise via l'API et retourne le SIREN du premier résultat
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

def traiter_fichier_csv(fichier_csv):
    """
    Traite le fichier CSV en recherchant les SIREN manquants et exporte en Excel
    """
    if not os.path.exists(fichier_csv):
        print(f"Erreur : Le fichier {fichier_csv} n'existe pas")
        return
      # Lire le fichier CSV avec pandas en forçant les codes postaux comme string
    try:
        df = pd.read_csv(fichier_csv, sep=';', encoding='utf-8-sig', dtype={'Code Postal': str})
        # Nettoyer les noms de colonnes (supprimer espaces en trop)
        df.columns = df.columns.str.strip()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return
    
    if df.empty:
        print("Erreur : Le fichier CSV est vide")
        return
    
    print(f"Fichier CSV chargé : {len(df)} lignes")
    print(f"Colonnes disponibles : {list(df.columns)}")
    print(f"Premières lignes du DataFrame :")
    print(df.head(3))
    
    # Vérifier que les colonnes nécessaires existent
    colonnes_requises = ['Nom d\'usage', 'Code Postal', 'Num Siren']
    for col in colonnes_requises:
        if col not in df.columns:
            print(f"Erreur : Colonne '{col}' manquante dans le fichier")
            return
      # Traiter chaque ligne
    lignes_traitées = 0
    sirens_trouvés = 0
    
    for index, row in df.iterrows():
        # Traiter toutes les lignes du fichier
        
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
        
        print(f"\n--- Ligne {index + 2} ---")
        print(f"Nom d'usage : '{nom_usage}'")
        print(f"Code postal : '{code_postal}'")
        print(f"SIREN actuel : '{siren_actuel}'")
        
        # Si le SIREN est déjà renseigné et non vide, on passe
        if siren_actuel and siren_actuel != 'nan' and siren_actuel != '0':
            print("  > SIREN déjà renseigné, passage...")
            lignes_traitées += 1
            continue
        
        # Si nom d'usage ou code postal manquants, on passe
        if not nom_usage or nom_usage == 'nan' or not code_postal or code_postal == 'nan':
            print("  > Nom d'usage ou code postal manquant, passage...")
            lignes_traitées += 1
            continue
          # Recherche du SIREN
        print(f"  > Recherche de '{nom_usage}' dans '{code_postal}'...")
        siren_trouvé = recherche_entreprise(BASE_URL, nom_usage, code_postal)
        
        if siren_trouvé:
            df.at[index, 'Num Siren'] = str(siren_trouvé)  # Conversion en string pour éviter l'avertissement
            sirens_trouvés += 1
            print(f"  > SIREN mis à jour : {siren_trouvé}")
        else:
            print("  > Aucun SIREN trouvé")
        
        lignes_traitées += 1
        
        # Pause pour éviter de surcharger l'API
        sleep(1)
    
    # Sauvegarder le fichier Excel mis à jour
    fichier_sortie = fichier_csv.replace('.csv', '_avec_sirens.xlsx')
    try:
        df.to_excel(fichier_sortie, index=False, engine='openpyxl')
        print(f"\n=== RÉSUMÉ ===")
        print(f"Lignes traitées : {lignes_traitées}")
        print(f"SIRENs trouvés : {sirens_trouvés}")
        print(f"Fichier Excel sauvegardé : {fichier_sortie}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde Excel : {e}")
        # Fallback en CSV si Excel échoue
        fichier_csv_sortie = fichier_csv.replace('.csv', '_avec_sirens.csv')
        df.to_csv(fichier_csv_sortie, sep=';', index=False, encoding='utf-8')
        print(f"Fichier CSV de secours sauvegardé : {fichier_csv_sortie}")

if __name__ == "__main__":
    fichier_csv = "data/TEST LOTFI .csv"
    traiter_fichier_csv(fichier_csv)
