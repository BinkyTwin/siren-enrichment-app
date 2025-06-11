# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet respecte [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-11

### ✨ Ajouté
- **Interface Streamlit** avec deux niveaux (simple et avancée)
- **API flexible** : support DataFrame et chemins de fichiers
- **Prévisualisation** des données avant traitement
- **Mode test** pour validation sur échantillon
- **Métriques temps réel** pendant l'enrichissement
- **Export multi-format** (Excel/CSV)
- **Configuration avancée** (séparateurs, encodage, délai API)
- **Tests unitaires** complets
- **Documentation** professionnelle
- **Launcher** pour démarrage rapide

### 🔧 Modifié
- **Architecture refactorisée** avec séparation des responsabilités
- **Fonction enrichir_sirens()** accepte maintenant DataFrame ou chemin
- **Gestion d'erreurs** améliorée et plus robuste
- **Interface utilisateur** modernisée avec Streamlit

### 🐛 Corrigé
- Gestion des codes postaux avec décimales (.0)
- Validation des colonnes CSV manquantes
- Encodage des caractères spéciaux
- Timeout et retry sur erreurs API

### 📚 Documentation
- README complet avec exemples
- Guide de contribution
- Tests unitaires documentés
- Licence MIT ajoutée

## [1.0.0] - 2025-06-10

### ✨ Ajouté
- **Enrichissement SIREN** via API gouvernementale française
- **Support CSV** avec validation automatique
- **Export Excel** des résultats
- **Interface ligne de commande**
- **Gestion des erreurs** API
- **Logs détaillés** du processus

### 🔧 Fonctionnalités
- Recherche automatique par nom d'entreprise et code postal
- Respect des limites de taux API (délai configurable)
- Support des fichiers CSV avec séparateur `;`
- Nettoyage automatique des données d'entrée
- Sauvegarde avec fallback CSV si Excel échoue

---

## Légende des types de changements

- ✨ **Ajouté** : nouvelles fonctionnalités
- 🔧 **Modifié** : changements dans les fonctionnalités existantes
- 🐛 **Corrigé** : corrections de bugs
- 🗑️ **Supprimé** : fonctionnalités supprimées
- 🚨 **Sécurité** : correctifs de sécurité
- 📚 **Documentation** : améliorations de la documentation
