# 🏢 Enrichissement SIREN

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red.svg)](https://streamlit.io)

Une application Python avec interface Streamlit pour enrichir automatiquement vos données d'entreprises avec leurs numéros SIREN via l'API gouvernementale française.

## ✨ Fonctionnalités

- 🔍 **Recherche automatique** de SIREN via l'API officielle
- 📊 **Interface web** moderne avec Streamlit
- 📁 **Import CSV** avec validation automatique
- 💾 **Export Excel/CSV** des données enrichies
- ⚙️ **Configuration flexible** (séparateurs, encodage, délais)
- 🧪 **Mode test** pour valider sur un échantillon
- 📈 **Métriques temps réel** du processus d'enrichissement

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances

```bash
git clone https://github.com/BinkyTwin/siren-enrichment-app.git
cd siren-enrichment-app
pip install -r requirements.txt
```

## 📖 Utilisation

### Interface web (recommandé)

#### Application simple
```bash
streamlit run app.py
```
Accès : http://localhost:8501

#### Application avancée
```bash
streamlit run app_advanced.py
```
Accès : http://localhost:8501

### Utilisation programmatique

```python
from main import enrichir_sirens
import pandas as pd

# Avec un fichier CSV
df_enrichi = enrichir_sirens("mon_fichier.csv")

# Avec un DataFrame pandas
df = pd.read_csv("mon_fichier.csv", sep=";")
df_enrichi = enrichir_sirens(df, verbose=False)

# Sauvegarde
df_enrichi.to_excel("resultat_enrichi.xlsx", index=False)
```

### Ligne de commande

```python
python main.py  # Traite le fichier par défaut
```

## 📋 Format des données

Votre fichier CSV doit contenir les colonnes suivantes :

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `Nom d'usage` | Nom de l'entreprise | "SOCIETE EXEMPLE SAS" |
| `Code Postal` | Code postal du siège | "75001" |
| `Num Siren` | Numéro SIREN (vide = à enrichir) | "" ou "123456789" |

### Exemple de fichier CSV

```csv
Nom d'usage;Code Postal;Num Siren
SOCIETE EXEMPLE SAS;75001;
ENTREPRISE TEST SARL;69000;123456789
DEMO COMPANY SA;13000;
```

## 🏗️ Architecture

```
📁 siren-enrichment-app/
├── 📄 main.py              # Logique métier principale
├── 📱 app.py               # Interface Streamlit simple
├── 🚀 app_advanced.py      # Interface Streamlit avancée
├── 🧪 test_unit.py         # Tests unitaires
├── 📝 exemples_utilisation.py # Exemples d'usage
├── 📋 requirements.txt     # Dépendances
├── 📂 data/               # Données d'exemple
│   └── exemple.csv
└── 📚 README.md
```

## 🔧 API

### `enrichir_sirens(input_data, verbose=True)`

**Paramètres :**
- `input_data` : `str` (chemin fichier) ou `pd.DataFrame`
- `verbose` : `bool` - Affichage des logs détaillés

**Retour :** `pd.DataFrame` enrichi

### Autres fonctions utiles

```python
from main import lire_csv, sauvegarder_excel, valider_dataframe

# Lecture et validation
df = lire_csv("fichier.csv")
df_valide = valider_dataframe(df)

# Sauvegarde
chemin = sauvegarder_excel(df, "sortie.xlsx")
```

## 🧪 Tests

```bash
python test_unit.py
```

Ou avec pytest :
```bash
pip install pytest
pytest test_unit.py -v
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` :
```env
API_BASE_URL=https://recherche-entreprises.api.gouv.fr
API_DELAY=1.0
API_PER_PAGE=5
```

### Paramètres Streamlit

L'application avancée permet de configurer :
- Séparateur CSV (`;`, `,`, `\t`)
- Encodage (`utf-8-sig`, `utf-8`, `iso-8859-1`)
- Délai entre requêtes API (0.5s à 3s)

## 📊 Sources de données

Cette application utilise l'**API officielle du gouvernement français** :
- 🔗 [API Recherche d'entreprises](https://recherche-entreprises.api.gouv.fr)
- 📖 [Documentation officielle](https://recherche-entreprises.api.gouv.fr/docs)

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Changelog

### Version 2.0.0
- ✨ Interface Streamlit avec deux niveaux (simple/avancée)
- 🔧 API refactorisée pour supporter DataFrame et fichiers
- 📊 Métriques temps réel et prévisualisation
- 🧪 Mode test et validation renforcée

### Version 1.0.0
- 🎯 Enrichissement SIREN via API gouvernementale
- 📁 Support CSV/Excel
- 🐍 Interface ligne de commande

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## ⚠️ Avertissements

- **Respect de l'API** : Respectez les limites de taux de l'API gouvernementale
- **Données personnelles** : Veillez à respecter le RGPD lors du traitement de données d'entreprises
- **Usage** : Cette application est destinée à un usage professionnel légal

## 🆘 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/BinkyTwin/siren-enrichment-app/issues)
- 📧 **Contact** : abdelatifdjeddou@gmail.com

---

<div align="center">
  <strong>Fait avec ❤️ par DJEDDOU Abdelatif</strong><br>
  Utilise l'API officielle gouvernementale française
</div>
