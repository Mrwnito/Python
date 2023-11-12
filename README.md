### Tableau de Bord des Interventions

Ce projet fournit un tableau de bord interactif construit avec Dash pour visualiser les données d'intervention des services d'urgence en France.  Il est structuré en trois fichiers principaux de script Python (globalvar.py, carte.py, dashboard.py) et utilise un dossier de données (les interventions des sapeurs pompiers en france de 2008 a 2021) ayant été traité via python pour harmoniser les colonnes, enlever les valeurs manquantes, etc.

### Structure du Projet

- `globalvar.py`: Contient les importations des bibliothèques nécessaires et la définition des variables globales.
- `carte.py`: Script pour générer des cartes géographiques interactives utilisées dans le tableau de bord.
- `dashboard.py`: Construit le tableau de bord Dash et définit les callbacks pour l'interactivité.

### Prérequis

Pour exécuter ce projet, assurez-vous d'avoir Python installé avec les bibliothèques suivantes :


pip install dash pandas numpy matplotlib.pyplot folium geopandas dash_bootstrap_components


### Installation

1. Clonez le dépôt du projet :

git clone https://github.com/Mrwnito/Python.git


### Exécution du Tableau de Bord

## Tout d'abord allez dans global.py et changer "cheminvervotrerepertoire" dans 'base_path' par le chemin vers votre repertoire de travail actuel.

Pour lancer le tableau de bord, suivez ces étapes :

1. Exécutez le fichier `globalvar.py` pour initialiser les configurations globales :

python globalvar.py


2. Générez les cartes en exécutant `carte.py` :

python carte.py


3. Lancez le tableau de bord avec `dashboard.py` :

python dashboard.py


Le tableau de bord devrait maintenant être accessible via un navigateur web à l'adresse `http://127.0.0.1:8050/` 
