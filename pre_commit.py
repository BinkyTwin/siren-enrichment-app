#!/usr/bin/env python3
"""
Script de validation pre-commit pour vérifier la qualité du code
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Exécute une commande et retourne True si succès"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - ÉCHEC")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - ERREUR: {e}")
        return False

def main():
    """Validation pre-commit principale"""
    print("🚀 Validation Pre-commit - Enrichissement SIREN")
    print("=" * 50)
    
    checks = [
        ("python -m py_compile main.py", "Syntaxe main.py"),
        ("python -m py_compile app.py", "Syntaxe app.py"), 
        ("python -m py_compile app_advanced.py", "Syntaxe app_advanced.py"),
        ("python test_unit.py", "Tests unitaires"),
        ("python -c 'from main import enrichir_sirens; print(\"Import OK\")'", "Import des modules"),
    ]
    
    success_count = 0
    total_checks = len(checks)
    
    for command, description in checks:
        if run_command(command, description):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Résultat: {success_count}/{total_checks} vérifications réussies")
    
    if success_count == total_checks:
        print("🎉 Toutes les vérifications sont passées avec succès !")
        print("✅ Votre code est prêt pour le commit")
        return 0
    else:
        print("⚠️ Certaines vérifications ont échoué")
        print("🔧 Corrigez les erreurs avant de committer")
        return 1

if __name__ == "__main__":
    sys.exit(main())
