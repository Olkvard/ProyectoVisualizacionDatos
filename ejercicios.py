from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from math import pi

# Cargar datos
df = pd.read_excel("jugadores.xlsx")

# Crear columnas de ataque y defensa
df["Ataque"] = ((df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]) - ((df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"])
df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

# Limitar los valores de "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]) / 5

# Inicializar la aplicación
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def radar_chart(player_name, category_labels=None):
    player_data = df[df['Nombre'] == player_name]
    if player_data.empty:
        return go.Figure()

    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'Ataque', 'Defensa']
    values = player_data[categories].values.flatten().tolist()

    # Añadir el primer valor al final para cerrar el gráfico
    values += values[:1]
    categories += categories[:1]

    # Crear gráfico de radar con Plotly
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker=dict(color='blue')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False, range=[0, 1])),
        showlegend=False,
        title=f'Estadísticas de {player_name}'
    )
    
    if category_labels:
        fig.update_traces(theta=category_labels)

    return fig

# Layout de la app
app.layout = dbc.Container([
    html.H1("Gráfica de jugadores"),
    dcc.Graph(figure=px.bar(df, x='Nombre', y='PER Aproximado', title="PER Aproximado de los Jugadores de Baloncesto",
                            labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},
                            color='PER Aproximado', color_continuous_scale='Blues')),
    dcc.Dropdown(id='player-dropdown', options=[{'label': name, 'value': name} for name in df['Nombre'].unique()],
                 placeholder="Selecciona un jugador"),
    dcc.Graph(id="radar-chart"),
])

# Callback para actualizar el gráfico de radar
@app.callback(
    Output("radar-chart", "figure"),
    Input("player-dropdown", "value")
)
def update_radar_chart(player_name):
    if player_name:
        return radar_chart(player_name, category_labels=['Tiros de 2', 'Tiros de 3', 'Tiros Libres', 'Ataque', 'Defensa'])
    return go.Figure()

# Iniciar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
