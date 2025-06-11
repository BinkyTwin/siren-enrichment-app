# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## 🚀 Comment contribuer

### 1. Fork et Clone
```bash
git fork https://github.com/BinkyTwin/siren-enrichment-app
git clone https://github.com/votre-fork/siren-enrichment-app.git
cd siren-enrichment-app
```

### 2. Configuration de l'environnement
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Création d'une branche
```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

## 📋 Types de contributions

### 🐛 Signaler un bug
- Utilisez les [GitHub Issues](https://github.com/BinkyTwin/siren-enrichment-app/issues)
- Décrivez le problème en détail
- Incluez les étapes de reproduction
- Mentionnez votre environnement (OS, Python version)

### ✨ Proposer une fonctionnalité
- Ouvrez d'abord une issue pour discuter
- Décrivez le cas d'usage
- Proposez une implémentation

### 🔧 Améliorer le code
- Corrigez des bugs
- Améliorez les performances
- Ajoutez des tests
- Améliorez la documentation

## 🧪 Tests

Avant de soumettre votre PR :

```bash
# Tests unitaires
python test_unit.py

# Tests manuels
python demo.py
streamlit run app.py
```

## 📝 Standards de code

### Style Python
- Suivez [PEP 8](https://pep8.org/)
- Utilisez des noms de variables descriptifs
- Commentez le code complexe
- Documentez les fonctions

### Structure des commits
```
type(scope): description courte

Description détaillée si nécessaire

Fixes #123
```

Types : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Exemple
```
feat(api): ajouter support pour nouveaux formats CSV

- Support des fichiers avec séparateur tabulation
- Détection automatique de l'encodage
- Validation améliorée des colonnes

Fixes #45
```

## 🔍 Process de review

1. **Tests** : Tous les tests doivent passer
2. **Documentation** : Mise à jour si nécessaire
3. **Code review** : Au moins une approbation
4. **Pas de conflits** : Branche à jour avec main

## 📚 Ressources

- [Documentation Python](https://docs.python.org/)
- [Guide Streamlit](https://docs.streamlit.io/)
- [API Entreprises](https://recherche-entreprises.api.gouv.fr/docs)
- [PEP 8 Style Guide](https://pep8.org/)

## 🆘 Besoin d'aide ?

- 💬 Ouvrez une [Discussion](https://github.com/BinkyTwin/siren-enrichment-app/discussions)
- 📧 Contactez le mainteneur : abdelatifdjeddou@gmail.com
- 📖 Consultez la documentation

## 📄 Licence

En contribuant, vous acceptez que vos contributions soient sous licence MIT.

---

Merci pour votre contribution ! 🙏
