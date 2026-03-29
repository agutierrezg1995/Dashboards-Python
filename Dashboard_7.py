import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Datos ficticios
np.random.seed(42)
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
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
    html.H1(children='Dashboard Interactivo', style={'textAlign': 'center', 'color': '#4CAF50'}),

    html.Div(children='Visualización de datos mensuales.', style={'textAlign': 'center'}),

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

    # Gráfico de superficie 3D para ventas
    ventas_fig = go.Figure(data=[go.Surface(z=[filtered_data['Ventas']], x=filtered_data['Mes'], y=['Ventas'], colorscale='Viridis')])
    ventas_fig.update_layout(title='Ventas Mensuales', title_font_size=20, title_font_color='#4CAF50', scene=dict(
        xaxis_title='Mes',
        yaxis_title='',
        zaxis_title='Ventas'
    ))

    # Gráfico de líneas 3D para gastos
    gastos_fig = go.Figure(data=[go.Scatter3d(x=filtered_data['Mes'], y=['Gastos']*len(filtered_data), z=filtered_data['Gastos'], mode='lines+markers', marker=dict(size=8, color='red', symbol='circle'))])
    gastos_fig.update_layout(title='Gastos Mensuales', title_font_size=20, title_font_color='red', scene=dict(
        xaxis_title='Mes',
        yaxis_title='',
        zaxis_title='Gastos'
    ))

    # Gráfico de barras 3D para beneficios (simulado con barras horizontales)
    beneficios_fig = go.Figure(data=[go.Bar(x=filtered_data['Beneficios'], y=filtered_data['Mes'], orientation='h', marker=dict(color='blue'))])
    beneficios_fig.update_layout(title='Distribución de Beneficios', title_font_size=20, title_font_color='blue')

    # Gráfico de dispersión 3D para la relación entre ventas y gastos
    scatter_fig = go.Figure(data=[go.Scatter3d(x=filtered_data['Ventas'], y=filtered_data['Gastos'], z=[0]*len(filtered_data), mode='markers+text', marker=dict(size=10, color='purple', symbol='diamond'), text=filtered_data['Mes'])])
    scatter_fig.update_layout(title='Relación entre Ventas y Gastos', title_font_size=20, title_font_color='purple', scene=dict(
        xaxis_title='Ventas',
        yaxis_title='Gastos',
        zaxis_title=''
    ))

    return ventas_fig, gastos_fig, beneficios_fig, scatter_fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
