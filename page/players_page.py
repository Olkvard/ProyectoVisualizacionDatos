from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Cargar datos
df = pd.read_excel("jugadores.xlsx")

# Crear columnas de ataque y defensa
df["Ataque"] = ((df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]) - ((df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"])
df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

# Limitar los valores de "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]) / 5

# Paleta de colores accesibles
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Azul, naranja, verde, rojo, púrpura


def radar_chart(player_names, category_labels=None):
    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'Ataque', 'Defensa']
    fig = go.Figure()

    # Generar los datos para cada jugador
    for i, player_name in enumerate(player_names):
        player_data = df[df['Nombre'] == player_name]
        if player_data.empty:
            continue

        values = player_data[categories].values.flatten().tolist()
        values += values[:1]  # Cerrar el círculo de datos
        category_labels = category_labels or categories
        category_labels += category_labels[:1]

        # Añadir traza de radar para cada jugador
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=category_labels,
            fill='toself',
            name=player_name,
            marker=dict(color=COLORS[i % len(COLORS)]),  # Usar colores accesibles
            opacity=0.6  # Transparencia para el relleno
        ))

    # Configuración del diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 1]
            )
        ),
        showlegend=True,
        title="Comparación de Estadísticas de Jugadores"
    )

    return fig


# Layout de la app
players_page_content = dbc.Container([
    html.H1("Gráfica de jugadores"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': name, 'value': name} for name in df['Nombre'].unique()],
        multi=True,
        placeholder="Selecciona hasta 5 jugadores"
    ),
    dcc.Graph(id="radar-chart"),
], style={"padding-top": "40px"})


# Callback para actualizar el gráfico de radar
@callback(
    Output("radar-chart", "figure"),
    Input("player-dropdown", "value")
)
def update_radar_chart(player_name):
    if player_name:
        # Validar el límite de selección de jugadores
        if len(player_name) > 5:
            player_name = player_name[:5]  # Limitar a los primeros 5 jugadores
            print("Has seleccionado más de 5 jugadores. Solo los primeros 5 se incluirán en el gráfico.")

        return radar_chart(player_name, category_labels=['Tiros de 2', 'Tiros de 3', 'Tiros Libres', 'Ataque', 'Defensa'])

    return go.Figure()
