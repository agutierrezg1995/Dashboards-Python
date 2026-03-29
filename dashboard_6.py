# Layout del dashboard
import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output

# Datos ficticios
np.random.seed(42)
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
         'Diciembre']
ventas = np.random.randint(1000, 5000, size=12)
gastos = np.random.randint(500, 3000, size=12)
beneficios = ventas - gastos

# Crear DataFrame
data = pd.DataFrame({
    'Mes': meses,
    'Ventas': ventas,
    'Gastos': gastos,
    'Beneficios': beneficios
})

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard Interactivo'),

    html.Div(children='Visualización de datos mensuales.'),

    # Dropdown para seleccionar meses
    dcc.Dropdown(
        id='meses-dropdown',
        options=[{'label': mes, 'value': mes} for mes in meses],
        value=meses,
        multi=True
    ),

    dcc.Graph(id='ventas-mensuales'),
    dcc.Graph(id='gastos-mensuales'),
    dcc.Graph(id='beneficios-distribucion'),
    dcc.Graph(id='ventas-gastos-scatter')  # Nuevo gráfico de dispersión
])


# Callback para actualizar gráficos según los meses seleccionados
@app.callback(
    [Output('ventas-mensuales', 'figure'),
     Output('gastos-mensuales', 'figure'),
     Output('beneficios-distribucion', 'figure'),
     Output('ventas-gastos-scatter', 'figure')],
    [Input('meses-dropdown', 'value')]
)
def update_graphs(selected_months):
    filtered_data = data[data['Mes'].isin(selected_months)]

    ventas_fig = px.area(filtered_data, x='Mes', y='Ventas', title='Ventas Mensuales')
    gastos_fig = px.line(filtered_data, x='Mes', y='Gastos', title='Gastos Mensuales', markers=True)
    beneficios_fig = px.bar(filtered_data, x='Beneficios', y='Mes', orientation='h', title='Distribución de Beneficios')
    scatter_fig = px.scatter(filtered_data, x='Ventas', y='Gastos', title='Relación entre Ventas y Gastos', text='Mes')

    return ventas_fig, gastos_fig, beneficios_fig, scatter_fig

app.layout = html.Div(children=[
    html.H1(children='Dashboard Interactivo'),

    html.Div(children='Visualización de datos mensuales.'),

    # Dropdown para seleccionar meses
    dcc.Dropdown(
        id='meses-dropdown',
        options=[{'label': mes, 'value': mes} for mes in meses],
        value=meses,
        multi=True
    ),

    # Contenedor de gráficos en 4 columnas
    html.Div([
        dcc.Graph(id='ventas-mensuales'),
        dcc.Graph(id='gastos-mensuales'),
        dcc.Graph(id='beneficios-distribucion'),
        dcc.Graph(id='ventas-gastos-scatter')
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(4, 1fr)',
        'gap': '20px',
        'marginTop': '20px'
    })
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)


