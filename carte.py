from globalvar import *  # Importer toutes les variables globales définies dans le fichier globalvar.py

# URL du fichier GeoJSON pour les contours des départements français
url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
# Lire le fichier GeoJSON avec geopandas pour obtenir un GeoDataFrame des départements
departements = gpd.read_file(url)

# Boucler sur les années de 2008 à 2021 inclus
for year in range(2008, 2022):
    df_carte = dfs[year]  # Sélectionner le DataFrame pour l'année courante

    # Obtenir la ligne correspondant au service de la Brigade des sapeurs-pompiers de Paris (BSPP)
    bspp_row = df_carte[df_carte['Numéro'] == 'BSPP'].copy().iloc[0]

    new_rows = []
    # Créer de nouvelles lignes pour chaque département que BSPP couvre
    for dep in ['75', '92', '93', '94']:
        new_row = bspp_row.copy()  # Copier la ligne BSPP
        new_row['Numéro'] = dep  # Affecter le numéro du département
        new_rows.append(new_row)  # Ajouter la nouvelle ligne à la liste

    # Supprimer l'ancienne ligne BSPP du DataFrame
    df_carte = df_carte[df_carte['Numéro'] != 'BSPP']
    # Ajouter les nouvelles lignes avec les bons numéros de département
    df_carte = pd.concat([df_carte, pd.DataFrame(new_rows)], ignore_index=True)

    # Formater les numéros de département pour avoir deux chiffres avec des zéros non significatifs
    df_carte['Numéro'] = df_carte['Numéro'].apply(lambda x: str(x).zfill(2))

    # Joindre le GeoDataFrame des départements avec les données d'interventions par numéro de département
    merged = departements.set_index('code').join(df_carte.set_index('Numéro'))
    # Exclure certains départements de la région Île-de-France
    merged = merged.drop(['77', '78', '91', '95'], errors='ignore')

    # Réinitialiser l'index pour avoir 'code' en tant que colonne
    merged = merged.reset_index()

    # Calculer les quantiles des interventions totales pour déterminer l'échelle de couleur de la carte
    quantiles = list(merged['Total interventions'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))

    # Initialiser une carte Folium centrée sur la France
    m = folium.Map(location=[46.896242, 3.078600], zoom_start=5)
    # Ajouter la couche choroplèthe au mapp avec les données fusionnées
    folium.Choropleth(
        geo_data=departements,
        data=merged,
        columns=['code', 'Total interventions'],
        key_on='feature.properties.code',
        fill_color='GnBu',  # Couleur de remplissage
        fill_opacity=0.7,  # Opacité du remplissage
        line_opacity=0.2,  # Opacité des lignes
        legend_name=f'Interventions par département {year}',  # Légende
        threshold_scale=quantiles  # Échelle de couleur basée sur les quantiles calculés
    ).add_to(m)

    # Sauvegarder la carte dans un fichier HTML nommé d'après l'année
    filename = f"map_{year}.html"
    m.save(filename)
    # Afficher un message de confirmation que la carte a été sauvegardée
    print(f"Carte sauvegardée pour l'année {year} dans le fichier {filename}")