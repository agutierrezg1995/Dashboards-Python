
import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Datos ficticios de población proyectada por departamento en Colombia para 2025
departamentos = [
    'Amazonas', 'Antioquia', 'Arauca', 'Atlántico', 'Bolívar', 'Boyacá', 'Caldas',
    'Caquetá', 'Casanare', 'Cauca', 'Cesar', 'Chocó', 'Córdoba', 'Cundinamarca',
    'Guainía', 'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 'Meta', 'Nariño',
    'Norte de Santander', 'Putumayo', 'Quindío', 'Risaralda', 'San Andrés y Providencia',
    'Santander', 'Sucre', 'Tolima', 'Valle del Cauca', 'Vaupés'
]
poblacion = [
    76000, 6500000, 270000, 2500000, 2200000, 1300000, 1000000, 400000, 350000,
    1100000, 500000, 1800000, 2900000, 50000, 100000, 1200000, 900000,
    1300000, 1100000, 1800000, 1500000, 80000, 550000, 1000000, 80000, 2200000,
    900000, 1400000, 4500000, 2500000, 60000
]

# Crear DataFrame
data = pd.DataFrame({
    'Departamento': departamentos,
    'Poblacion': poblacion
})

# Datos ficticios para pirámide poblacional
np.random.seed(42)
edades = np.random.randint(0, 100, size=1000)
generos = np.random.choice(['Masculino', 'Femenino'], size=1000)
piramide_data = pd.DataFrame({
    'Edad': edades,
    'Genero': generos
})

# Datos ficticios para evolución de población
years = np.arange(2020, 2026)
evolucion_data = pd.DataFrame({
    'Year': np.tile(years, len(departamentos)),
    'Departamento': np.repeat(departamentos, len(years)),
    'Poblacion': np.random.randint(50000, 7000000, size=len(departamentos) * len(years))
})

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Población de Colombia'),
    html.Div(children='Visualización de la población proyectada por departamento en 2025.'),
    dcc.Dropdown(
        id='departamentos-dropdown',
        options=[{'label': depto, 'value': depto} for depto in departamentos],
        value=departamentos,
        multi=True
    ),
    html.Div([
        dcc.Graph(id='poblacion-piramide'),
        dcc.Graph(id='poblacion-radar'),
        dcc.Graph(id='poblacion-violin'),
        dcc.Graph(id='poblacion-densidad'),
        dcc.Graph(id='poblacion-barras-horizontal'),
        dcc.Graph(id='poblacion-pastel'),
        dcc.Graph(id='poblacion-box'),
        dcc.Graph(id='poblacion-dispersion'),
        dcc.Graph(id='poblacion-lineas'),
        dcc.Graph(id='poblacion-histograma'),
        dcc.Graph(id='poblacion-burbujas'),
        dcc.Graph(id='poblacion-barras-genero'),
        dcc.Graph(id='poblacion-area'),
        dcc.Graph(id='poblacion-dispersion-3d')
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(2, 1fr)',
        'gap': '20px',
        'marginTop': '20px'
    })
])

@app.callback(
    [Output('poblacion-piramide', 'figure'),
     Output('poblacion-radar', 'figure'),
     Output('poblacion-violin', 'figure'),
     Output('poblacion-densidad', 'figure'),
     Output('poblacion-barras-horizontal', 'figure'),
     Output('poblacion-pastel', 'figure'),
     Output('poblacion-box', 'figure'),
     Output('poblacion-dispersion', 'figure'),
     Output('poblacion-lineas', 'figure'),
     Output('poblacion-histograma', 'figure'),
     Output('poblacion-burbujas', 'figure'),
     Output('poblacion-barras-genero', 'figure'),
     Output('poblacion-area', 'figure'),
     Output('poblacion-dispersion-3d', 'figure')],
    [Input('departamentos-dropdown', 'value')]
)
def update_graphs(selected_departments):
    filtered_data = data[data['Departamento'].isin(selected_departments)]
    evolucion_filtered_data = evolucion_data[evolucion_data['Departamento'].isin(selected_departments)]

    # Pirámide poblacional simulada
    piramide_fig = px.histogram(
        piramide_data, x='Edad', color='Genero', barmode='overlay',
        title='Pirámide Poblacional Simulada'
    )

    # Gráfico de radar
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=filtered_data['Poblacion'],
        theta=filtered_data['Departamento'],
        fill='toself'
    ))
    radar_fig.update_layout(title='Población por Departamento (Radar)')

    # Gráfico de violín
    violin_fig = px.violin(
        filtered_data, y='Poblacion', box=True, points="all",
        title='Distribución de Población por Departamento (Violín)'
    )

    # Gráfico de densidad
    densidad_fig = px.density_heatmap(
        filtered_data, x='Departamento', y='Poblacion',
        title='Densidad de Población por Departamento'
    )

    # Gráfico de barras horizontal
    barras_horizontal_fig = px.bar(
        filtered_data, x='Poblacion', y='Departamento', orientation='h',
        title='Población por Departamento (Barras Horizontal)'
    )

    # Gráfico de pastel
    pastel_fig = px.pie(
        filtered_data, values='Poblacion', names='Departamento',
        title='Proporción de Población por Departamento (Pastel)'
    )

    # Gráfico de caja (box plot)
    box_fig = px.box(
        filtered_data, y='Poblacion',
        title='Distribución de Población por Departamento (Box Plot)'
    )

    # Gráfico de dispersión (scatter plot)
    dispersion_fig = px.scatter(
        filtered_data, x='Departamento', y='Poblacion',
        title='Dispersión de Población por Departamento (Scatter Plot)'
    )

    # Gráfico de líneas (evolución simulada)
    lineas_fig = px.line(
        evolucion_filtered_data, x='Year', y='Poblacion', color='Departamento',
        title='Evolución de Población por Departamento (Líneas)'
    )

    # Gráfico de histograma
    histograma_fig = px.histogram(
        filtered_data, x='Poblacion',
        title='Histograma de Población por Departamento'
    )

    # Gráfico de burbujas
    burbujas_fig = px.scatter(
        filtered_data, x='Departamento', y='Poblacion', size='Poblacion',
        title='Población por Departamento (Burbujas)'
    )

    # Gráfico de barras agrupadas por género (simulado)
    barras_genero_fig = px.bar(
        piramide_data, x='Genero', y='Edad', color='Genero', barmode='group',
        title='Distribución de Edad por Género (Barras Agrupadas)'
    )

    # Gráfico de área acumulada (simulado)
    area_fig = px.area(
        evolucion_filtered_data, x='Year', y='Poblacion', color='Departamento',
        title='Evolución Acumulada de Población por Departamento (Área)'
    )

    # Gráfico de dispersión 3D (simulado)
    dispersion_3d_fig = px.scatter_3d(
        evolucion_filtered_data, x='Year', y='Departamento', z='Poblacion',
        title='Dispersión 3D de Población por Departamento'
    )

    return (piramide_fig, radar_fig, violin_fig, densidad_fig, barras_horizontal_fig, pastel_fig,
            box_fig, dispersion_fig, lineas_fig, histograma_fig, burbujas_fig, barras_genero_fig,
            area_fig, dispersion_3d_fig)

if __name__ == '__main__':
    app.run(debug=True)