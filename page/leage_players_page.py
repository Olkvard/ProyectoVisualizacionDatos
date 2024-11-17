from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from components.card_TC_average_Top import AverageCardTC
from components.card_TC1_average_Top import AverageCardTC1
from components.card_ataque_Top import CardAtaque
from components.card_defensa_Top import CardDefensa

# Leer los datos del dataset
df = pd.read_excel("jugadores.xlsx")

# Crear columnas de ataque y defensa
df["Ataque"] = ((df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]) - ((df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"])
df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

# Limitar los valores de "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

# Calcular el PER Aproximado
df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]) / 5

# Ordena el DataFrame por PER Aproximado en orden descendente
df = df.sort_values(by='PER Aproximado', ascending=False).reset_index(drop=True)

# Define los colores de la paleta viridis
viridis_colors = ["#440154", "#482878", "#3e4a89", "#31688e", "#26828e", "#1f9e89", "#35b779", "#6ece58", "#b8de29", "#fde725"]

# Layout del Dashboard
leage_players = dbc.Container([
    # Contenedor para ambas tarjetas
    dbc.Row([
        dbc.Col(id='tc-average-container', width="auto"),
        dbc.Col(id='tc1-average-container', width="auto"),
        dbc.Col(id='ataque-container', width="auto"),
        dbc.Col(id='defensa-container', width="auto")
    ], style={"margin-bottom": "1rem"}),

    # Dropdown para seleccionar el rango de jugadores
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-top-n',
                options=[{'label': f'Top {i-9} - {i}', 'value': i} for i in range(10, len(df)+10, 10)],
                value=10,
                clearable=False,
                style={"width": "50%", "margin-top": "1rem"}
            ), width=12)
    ], style={"margin-bottom": "1rem"}),

    # Gráfico que se actualizará dinámicamente
    dcc.Graph(id='graph-top-players'),
], style={"padding-top": "3rem"})


# Callback para actualizar el gráfico y la tarjeta de promedio según el valor del Dropdown
@callback(
    [Output('graph-top-players', 'figure'),
     Output('tc-average-container', 'children'),
     Output('tc1-average-container', 'children'),
     Output('ataque-container', 'children'),
     Output('defensa-container', 'children')],  # Actualiza el contenedor en lugar de la tarjeta directamente
    [Input('dropdown-top-n', 'value')]
)
def update_graph_and_label(top_n):
    # Calcular los índices de inicio y fin del rango
    start_idx = top_n - 10
    end_idx = min(top_n, len(df))  # Limitar el índice final al total de jugadores
    
    # Filtrar los datos para obtener solo los jugadores en el rango seleccionado y ordenar en ascendente
    top_players = df.iloc[start_idx:end_idx].sort_values(by='PER Aproximado', ascending=True)
    
    # Crear el gráfico de barras actualizado
    fig = px.bar(
        top_players,
        y='Nombre',
        x='PER Aproximado',
        title=f"Jugadores {start_idx + 1} a {end_idx} por PER Aproximado (Orden Invertido)",
        labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},
        color='PER Aproximado',
        color_discrete_sequence=viridis_colors,
        orientation="h"
    )

    # Usar el componente AverageCard pasando los jugadores seleccionados
    return fig, AverageCardTC(top_players), AverageCardTC1(top_players), CardAtaque(top_players), CardDefensa(top_players)
