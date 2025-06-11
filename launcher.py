#!/usr/bin/env python3
"""
Script de lancement rapide pour l'application Enrichissement SIREN
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Vérifie que les dépendances sont installées"""
    try:
        import streamlit
        import pandas
        import requests
        import openpyxl
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False

def launch_simple_app():
    """Lance l'application Streamlit simple"""
    print("🚀 Lancement de l'application simple...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

def launch_advanced_app():
    """Lance l'application Streamlit avancée"""
    print("🚀 Lancement de l'application avancée...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app_advanced.py"])

def run_demo():
    """Exécute la démonstration"""
    print("🎯 Exécution de la démonstration...")
    subprocess.run([sys.executable, "demo.py"])

def run_tests():
    """Exécute les tests unitaires"""
    print("🧪 Exécution des tests...")
    subprocess.run([sys.executable, "test_unit.py"])

def main():
    """Menu principal"""
    print("🏢 Enrichissement SIREN - Launcher")
    print("=" * 40)
    
    if not check_requirements():
        return
    
    print("\nQue voulez-vous faire ?")
    print("1. 📱 Lancer l'application simple")
    print("2. 🚀 Lancer l'application avancée") 
    print("3. 🎯 Exécuter la démonstration")
    print("4. 🧪 Lancer les tests")
    print("5. ❌ Quitter")
    
    while True:
        try:
            choice = input("\nVotre choix (1-5): ").strip()
            
            if choice == "1":
                launch_simple_app()
                break
            elif choice == "2":
                launch_advanced_app()
                break
            elif choice == "3":
                run_demo()
                break
            elif choice == "4":
                run_tests()
                break
            elif choice == "5":
                print("👋 Au revoir !")
                break
            else:
                print("❌ Choix invalide. Utilisez 1, 2, 3, 4 ou 5.")
        
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
