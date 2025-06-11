#!/usr/bin/env python3
"""
Tests unitaires pour les fonctions refactorisées
"""

import unittest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from main import (
    lire_csv, 
    valider_dataframe, 
    nettoyer_donnees_ligne, 
    enrichir_sirens,
    sauvegarder_excel,
    recherche_entreprise
)

class TestMainFunctions(unittest.TestCase):
    
    def setUp(self):
        """Configuration des tests"""
        self.sample_data = {
            'Nom d\'usage': ['Entreprise A', 'Société B', 'SARL C'],
            'Code Postal': ['75001', '69000', '13000'],
            'Num Siren': ['', '123456789', '']
        }
        self.df_sample = pd.DataFrame(self.sample_data)
    
    def test_valider_dataframe_valid(self):
        """Test de validation d'un DataFrame valide"""
        df_validated = valider_dataframe(self.df_sample)
        self.assertIsInstance(df_validated, pd.DataFrame)
        self.assertEqual(len(df_validated), 3)
        self.assertIn('Nom d\'usage', df_validated.columns)
    
    def test_valider_dataframe_empty(self):
        """Test de validation d'un DataFrame vide"""
        df_empty = pd.DataFrame()
        with self.assertRaises(ValueError):
            valider_dataframe(df_empty)
    
    def test_valider_dataframe_missing_column(self):
        """Test de validation d'un DataFrame avec colonne manquante"""
        df_invalid = pd.DataFrame({
            'Nom d\'usage': ['Test'],
            'Code Postal': ['75001']
            # Manque 'Num Siren'
        })
        with self.assertRaises(ValueError):
            valider_dataframe(df_invalid)
    
    def test_nettoyer_donnees_ligne(self):
        """Test de nettoyage des données d'une ligne"""
        row = pd.Series({
            'Nom d\'usage': ' Entreprise Test ',
            'Code Postal': '75001.0',
            'Num Siren': ''
        })
        
        nom, cp, siren = nettoyer_donnees_ligne(row)
        
        self.assertEqual(nom, 'Entreprise Test')
        self.assertEqual(cp, '75001')
        self.assertEqual(siren, '')
    
    def test_nettoyer_donnees_ligne_nan_values(self):
        """Test de nettoyage avec valeurs NaN"""
        row = pd.Series({
            'Nom d\'usage': pd.NA,
            'Code Postal': pd.NA,
            'Num Siren': pd.NA
        })
        
        nom, cp, siren = nettoyer_donnees_ligne(row)
        
        self.assertEqual(nom, '')
        self.assertEqual(cp, '')
        self.assertEqual(siren, '')
    
    def test_lire_csv_file_not_found(self):
        """Test de lecture d'un fichier inexistant"""
        with self.assertRaises(FileNotFoundError):
            lire_csv('fichier_inexistant.csv')
    
    def test_lire_csv_valid_file(self):
        """Test de lecture d'un fichier CSV valide"""
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write('Nom d\'usage;Code Postal;Num Siren\n')
            f.write('Test Entreprise;75001;\n')
            f.write('Autre Société;69000;123456789\n')
            temp_file = f.name
        
        try:
            df = lire_csv(temp_file)
            self.assertEqual(len(df), 2)
            self.assertIn('Nom d\'usage', df.columns)
            self.assertEqual(df.iloc[0]['Nom d\'usage'], 'Test Entreprise')
        finally:
            os.unlink(temp_file)
    
    @patch('main.recherche_entreprise')
    def test_enrichir_sirens_with_dataframe(self, mock_recherche):
        """Test d'enrichissement avec un DataFrame"""
        # Mock de la fonction recherche_entreprise
        mock_recherche.return_value = '987654321'
        
        # DataFrame de test
        df_test = self.df_sample.copy()
        
        # Enrichissement
        df_enrichi = enrichir_sirens(df_test, verbose=False)
        
        # Vérifications
        self.assertIsInstance(df_enrichi, pd.DataFrame)
        self.assertEqual(len(df_enrichi), 3)
        
        # Vérifier que les SIRENs vides ont été enrichis
        sirens_non_vides = df_enrichi['Num Siren'][df_enrichi['Num Siren'] != ''].count()
        self.assertGreaterEqual(sirens_non_vides, 1)  # Au moins un SIREN a été ajouté
    
    @patch('main.lire_csv')
    @patch('main.recherche_entreprise')
    def test_enrichir_sirens_with_file_path(self, mock_recherche, mock_lire_csv):
        """Test d'enrichissement avec un chemin de fichier"""
        # Mock des fonctions
        mock_lire_csv.return_value = self.df_sample.copy()
        mock_recherche.return_value = '987654321'
        
        # Enrichissement
        df_enrichi = enrichir_sirens('test.csv', verbose=False)
        
        # Vérifications
        mock_lire_csv.assert_called_once_with('test.csv')
        self.assertIsInstance(df_enrichi, pd.DataFrame)
    
    def test_enrichir_sirens_invalid_input(self):
        """Test d'enrichissement avec entrée invalide"""
        with self.assertRaises(TypeError):
            enrichir_sirens(123)  # Type invalide
    
    def test_sauvegarder_excel(self):
        """Test de sauvegarde Excel"""
        df = self.df_sample.copy()
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_file = f.name
        
        try:
            chemin_sauvegarde = sauvegarder_excel(df, temp_file)
            self.assertTrue(os.path.exists(chemin_sauvegarde))
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @patch('main.requests.get')
    def test_recherche_entreprise_success(self, mock_get):
        """Test de recherche d'entreprise avec succès"""
        # Mock de la réponse API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [{
                'siren': '123456789',
                'denomination': 'Test Entreprise',
                'siege': {'code_postal': '75001'}
            }]
        }
        mock_response.status_code = 200
        mock_response.request.url = 'http://test.url'
        mock_get.return_value = mock_response
        
        # Test avec mock print pour éviter les sorties
        with patch('builtins.print'):
            siren = recherche_entreprise('http://api.test', 'Test Entreprise', '75001')
        
        self.assertEqual(siren, '123456789')
    
    @patch('main.requests.get')
    def test_recherche_entreprise_no_results(self, mock_get):
        """Test de recherche d'entreprise sans résultats"""
        # Mock de la réponse API vide
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_response.status_code = 200
        mock_response.request.url = 'http://test.url'
        mock_get.return_value = mock_response
        
        with patch('builtins.print'):
            siren = recherche_entreprise('http://api.test', 'Entreprise Inexistante', '00000')
        
        self.assertIsNone(siren)
    
    @patch('main.requests.get')
    def test_recherche_entreprise_api_error(self, mock_get):
        """Test de recherche d'entreprise avec erreur API"""
        # Mock d'une erreur de requête
        mock_get.side_effect = Exception('Erreur API')
        
        with patch('builtins.print'):
            siren = recherche_entreprise('http://api.test', 'Test', '75001')
        
        self.assertIsNone(siren)

class TestIntegration(unittest.TestCase):
    """Tests d'intégration"""
    
    def test_workflow_complet(self):
        """Test du workflow complet avec données de test"""
        # Données de test
        data = {
            'Nom d\'usage': ['Entreprise Existante', 'Entreprise à Enrichir'],
            'Code Postal': ['75001', '69000'],
            'Num Siren': ['123456789', '']  # Une avec SIREN, une sans
        }
        df_test = pd.DataFrame(data)
        
        # Mock de l'API pour éviter les appels réels
        with patch('main.recherche_entreprise') as mock_recherche:
            mock_recherche.return_value = '987654321'
            
            # Test du workflow
            df_enrichi = enrichir_sirens(df_test, verbose=False)
            
            # Vérifications
            self.assertEqual(len(df_enrichi), 2)
            self.assertEqual(df_enrichi.iloc[0]['Num Siren'], '123456789')  # Inchangé
            self.assertEqual(df_enrichi.iloc[1]['Num Siren'], '987654321')  # Enrichi

if __name__ == '__main__':
    # Configuration pour éviter les sorties lors des tests
    import sys
    from io import StringIO
    
    # Rediriger stdout pour les tests
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        unittest.main(verbosity=2)
    finally:
        sys.stdout = old_stdout
