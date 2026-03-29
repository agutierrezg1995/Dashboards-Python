import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px

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
    html.H1(children='Dashboard Interactivo'),

    html.Div(children='Visualización de datos mensuales.'),

    dcc.Graph(
        id='ventas-mensuales',
        figure=px.line(data, x='Mes', y='Ventas', title='Ventas Mensuales')
    ),

    dcc.Graph(
        id='gastos-mensuales',
        figure=px.bar(data, x='Mes', y='Gastos', title='Gastos Mensuales')
    ),

    dcc.Graph(
        id='beneficios-distribucion',
        figure=px.pie(data, values='Beneficios', names='Mes', title='Distribución de Beneficios')
    )
])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
