from globalvar import *  # Importe toutes les variables globales du fichier globalvar.py

# Initialisation de l'application Dash avec le thème Bootstrap pour le CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Lecture du contenu de la carte sauvegardée en HTML
with open('map_2021.html', 'r', encoding='utf-8') as f:
    map_content = f.read()

# Définition de la mise en page du tableau de bord avec des conteneurs, des rangées et des colonnes Bootstrap
app.layout = dbc.Container([
    # Première rangée pour les filtres et le titre
    dbc.Row([
        dbc.Col([
            # Widget de sélection d'année
            html.Label("Filtre Année"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(i), 'value': i} for i in range(2008, 2022)],
                value=2021
            ),
        ], width=3, lg=1.5),
        dbc.Col([
            # Titre du tableau de bord
            html.H1("Insights sur les Interventions d'Urgence", style={'font-weight': 'bold'}),    
        ], width=3, lg=9)    
    ], className='mb-1'),  # Ajout d'une marge en bas de la rangée

    dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-chart', style={'height': '50vh'}),  # Ajustement de la hauteur
            ], width=12, lg=6),
            dbc.Col([
                dcc.Graph(id='pie-chart', style={'height': '50vh'}),  # Ajustement de la hauteur
            ], width=12, lg=6),
    ], className='mb-1'),  # Ajout d'une marge en bas de la rangée

    dbc.Row([
        dbc.Col([
            html.Iframe(id='map-iframe', srcDoc=map_content, width='100%', height='370px'),  # Hauteur ajustée en pixels
        ], width=12, lg=6),
        dbc.Col([
            dcc.Graph(id='top5-bar-chart', style={'height': '50vh'}),  # Ajustement de la hauteur
        ], width=12, lg=6),
    ], className='mb-1'),

    dbc.Row([
            dbc.Col([
                dcc.Graph(id='hist-chart', style={'height': '50vh'}),  # Ajustement de la hauteur
            ], width=12, lg=6),
            dbc.Col([
                dcc.Graph(id='corre-chart', style={'height': '50vh'}),  # Ajustement de la hauteur
            ], width=12, lg=6),
    ], ),  # Ajout d'une marge en bas de la rangée
], fluid=True, style={'backgroundColor': '#E9ECEF'})  # Couleur de fond douce pour l'ensemble du container
# Graphique à barres pour l'évolution des interventions par année
@app.callback(
    Output('bar-chart', 'figure'),  # Le composant 'bar-chart' sera mis à jour avec une nouvelle 'figure'
    [Input('year-dropdown', 'value')]  # La mise à jour dépend de la valeur sélectionnée dans 'year-dropdown'
)
def update_bar_chart(selected_year):
    # Crée un graphique en barres avec les totaux annuels
    bar_fig = px.bar(
        x=years,  # L'axe des abscisses représente les années
        y=totals,  # L'axe des ordonnées représente le total des interventions pour chaque année
        labels={'x': 'Année', 'y': 'Nombre d\'interventions'},  # Étiquettes pour les axes
        title='Évolution des interventions par année'  # Titre du graphique
    )

    # Met à jour la couleur des barres du graphique
    bar_fig.update_traces(marker_color='#83A1A4')

    # Boucle sur chaque type d'intervention pour ajouter une ligne au graphique
    for idx, intervention in enumerate(interventions):
        # Calcule le total annuel de chaque type d'intervention
        yearly_totals = [df[intervention].sum() for _, df in dfs.items()]
        # Ajoute une ligne au graphique pour représenter le total annuel de chaque type d'intervention
        bar_fig.add_scatter(
            x=years, y=yearly_totals, 
            mode='lines', name=intervention, 
            line=dict(color=colors[idx])  # Utilise la couleur spécifique de l'intervention
        )

    # Met à jour la mise en page du graphique pour améliorer la lisibilité et l'apparence
    bar_fig.update_layout(
        title={
            'text': 'Évolution des interventions par année',
            'y': 0.95,  # Position verticale du titre
            'x': 0.5,   # Position horizontale du titre
            'xanchor': 'center',  # Ancrage horizontal du titre
            'yanchor': 'top'  # Ancrage vertical du titre
        },
        title_font=dict(size=15),  # Définit la taille de la police du titre
        margin=dict(l=20, r=20, t=40, b=20)  # Marges autour du graphique
    )

    # Retourne la figure mise à jour pour être affichée dans le composant 'bar-chart'
    return bar_fig

# Met à jour le graphique en secteurs pour la répartition des interventions par type pour l'année sélectionnée
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_pie_chart(selected_year):
    # Calcul de la somme des interventions par type pour l'année sélectionnée
    répartition_interventions = dfs[selected_year][[
        'Incendies',
        'Secours à personne',
        'Accidents de circulation',
        'Risques technologiques',
        'Opérations diverses'
    ]].sum()

    # Création du graphique en secteurs avec les données calculées
    pie_fig = px.pie(
        values=répartition_interventions.values, 
        names=répartition_interventions.index,
        title=f"Répartition des interventions par type pour l'année {selected_year}",
        color_discrete_sequence=colors
    )

    # Mise à jour de la mise en page du graphique
    pie_fig.update_layout(
        title_font=dict(size=15),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return pie_fig

# Met à jour le contenu de la carte intégrée en fonction de l'année sélectionnée
@app.callback(
    Output(component_id='map-iframe', component_property='srcDoc'),
    Input(component_id='year-dropdown', component_property='value')
)
def update_map(selected_year):
    # Ouverture et lecture du fichier HTML correspondant à la carte de l'année sélectionnée
    with open(f'map_{selected_year}.html', 'r', encoding='utf-8') as f:
        map_content = f.read()
    return map_content

# Met à jour le graphique en barres pour le top 5 des départements en fonction de l'année sélectionnée
@app.callback(
    Output('top5-bar-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_top5_bar_chart(selected_year):
    # Sélection des cinq départements avec le plus grand nombre d'interventions
    df = dfs[selected_year]
    top5 = df.sort_values(by='Total interventions', ascending=False).head(5)

    # Création du graphique en barres avec les données filtrées
    bar_fig = px.bar(
        top5,
        x='Département',
        y='Total interventions',
        color='Département',
        title=f"Top 5 des départements avec le plus grand nombre d'interventions pour {selected_year}",
        color_discrete_sequence=colors
    )

    # Mise à jour de la mise en page du graphique
    bar_fig.update_layout(
        title_font=dict(size=15),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return bar_fig


# Met à jour l'histogramme des interventions pour l'année sélectionnée
@app.callback(
    Output('hist-chart', 'figure'), 
    [Input('year-dropdown', 'value')]
)
def update_histogram(selected_year):
    # Extraction des données pour l'année sélectionnée
    data_for_year = dfs[selected_year]
    
    # Création de l'histogramme avec Plotly Express
    fig = px.histogram(
        data_for_year, 
        x='Total interventions',  # Axe X représentant le total des interventions
        nbins=30,  # Nombre de bins dans l'histogramme
        title=f"Histogramme des interventions pour l'année {selected_year}",
        color_discrete_sequence=['#4eb3d3']  # Séquence de couleurs pour les barres
    )
    
    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        xaxis_title="Nombre d'interventions",  # Titre de l'axe X
        yaxis_title="Fréquence",  # Titre de l'axe Y
        margin=dict(l=20, r=20, t=40, b=20)  # Réglage des marges autour du graphique
    )
    
    return fig

# Met à jour la matrice de corrélation pour l'année sélectionnée
@app.callback(
    Output('corre-chart', 'figure'),  
    [Input('year-dropdown', 'value')]
)
def update_correlation_matrix(selected_year):
    # Extraction des données pour l'année sélectionnée
    data_for_year = dfs[selected_year]
    # Sélection des données relatives aux interventions
    interventions_data = data_for_year[interventions]
    
    # Calcul de la matrice de corrélation
    correlation_matrix = interventions_data.corr(method='pearson')
    # Transformation des valeurs pour l'affichage
    transformed_correlation_matrix = np.arctan(correlation_matrix * (np.pi/2 - 0.1))
    
    # Création de la matrice de corrélation avec Plotly Express
    fig = px.imshow(
        transformed_correlation_matrix, 
        text_auto=True,  # Affichage automatique des valeurs dans les cellules
        title=f"Matrice de Corrélation pour l'année {selected_year}",
        color_continuous_scale=colors  # Échelle de couleurs pour la matrice
    )
    
    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        xaxis_title="Types d'interventions",  # Titre de l'axe X
        yaxis_title="Types d'interventions",  # Titre de l'axe Y
        margin=dict(l=20, r=20, t=40, b=20)  # Réglage des marges autour du graphique
    )
    
    return fig

# Lancer l'application en mode débogage
if __name__ == '__main__':
    app.run_server(debug=True)