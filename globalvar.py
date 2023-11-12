import pandas as pd  # Bibliothèque pour la manipulation de données
import numpy as np  # Bibliothèque pour les opérations numériques
import matplotlib.pyplot as plt  # Bibliothèque pour la création de visualisations statiques
import folium  # Bibliothèque pour la création de cartes interactives
import geopandas as gpd  # Bibliothèque pour la manipulation de données géospatiales
import seaborn as sns  # Bibliothèque pour la création de visualisations statistiques

# Importations nécessaires pour créer un tableau de bord interactif
import dash  # Framework pour la création d'applications web avec Python
from dash import dcc, html, Input, Output  # Composants Dash pour l'interactivité
import plotly.express as px  # Bibliothèque pour la création de visualisations interactives
import dash_bootstrap_components as dbc  # Composants bootstrap pour Dash

# Chemin de base vers le répertoire contenant les données
base_path = 'cheminversvotrerepertoire/Données/'

# Initialiser un dictionnaire vide pour stocker les DataFrames par année
dfs = {}

# Boucler sur les années de 2008 à 2021 inclus
for year in range(2008, 2022):
    file_name = f"interventions{year}V3.xlsx"  # Nom de fichier pour l'année donnée
    full_path = base_path + file_name  # Chemin complet du fichier
    dfs[year] = pd.read_excel(full_path)  # Lire le fichier Excel et stocker le DataFrame dans le dictionnaire

# Les DataFrames sont maintenant accessibles par année dans le dictionnaire `dfs`
# Exemple d'accès au DataFrame pour l'année 2008 : dfs[2008]

# Liste des années pour référence ultérieure
years = list(dfs.keys())

# Calculer les totaux d'interventions pour chaque année et les stocker dans une liste
totals = [df['Total interventions'].sum() for _, df in dfs.items()]

# Définir une palette de couleurs pour la visualisation
colors = ['#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3', '#2b8cbe']

# Liste des types d'interventions à analyser
interventions = ['Incendies', 'Secours à personne', 'Accidents de circulation', 'Risques technologiques', 'Opérations diverses']