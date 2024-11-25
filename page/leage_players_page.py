from dash import dcc, html, Input, Output, callback  # Componentes principales de Dash para construir el dashboard y manejar interactividad
import dash_bootstrap_components as dbc  # Componentes estilizados con Bootstrap para diseño
import plotly.express as px  # Biblioteca para crear gráficos interactivos
import pandas as pd  # Biblioteca para manipulación de datos con DataFrames
from components.card_TC_average_Top import AverageCardTC  # Componente para mostrar el promedio de Tiros de Campo
from components.card_TC1_average_Top import AverageCardTC1  # Componente para el promedio de Tiros Libres
from components.card_ataque_Top import CardAtaque  # Componente para métricas de Ataque
from components.card_defensa_Top import CardDefensa  # Componente para métricas de Defensa

# --- Carga y preprocesamiento de datos ---

# Leer los datos del archivo Excel
df = pd.read_excel("jugadores.xlsx")

# Crear una columna "Ataque" calculada como una métrica personalizada ofensiva
df["Ataque"] = (
    (df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]
    - (df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"]
)

# Crear una columna "Defensa" calculada como una métrica personalizada defensiva
df["Defensa"] = (
    (df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) 
    / df["Minutos Jugados"]
    - (df["Faltas Personales Cometidas"]) / df["Minutos Jugados"]
)

# Limitar los valores de las métricas "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

# Calcular una métrica compuesta "PER Aproximado" como el promedio de varias métricas clave
df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]) / 5

# Ordenar el DataFrame por "PER Aproximado" en orden descendente
df = df.sort_values(by='PER Aproximado', ascending=False).reset_index(drop=True)

# Define una paleta de colores personalizada basada en el esquema viridis
viridis_colors = [
    "#440154", "#482878", "#3e4a89", "#31688e", 
    "#26828e", "#1f9e89", "#35b779", "#6ece58", 
    "#b8de29", "#fde725"
]

# --- Layout del dashboard ---

leage_players = dbc.Container([
    # Fila para las tarjetas de estadísticas clave
    dbc.Row([
        dbc.Col(id='tc-average-container', width="auto"),  # Contenedor para promedio de Tiros de Campo
        dbc.Col(id='tc1-average-container', width="auto"),  # Contenedor para promedio de Tiros Libres
        dbc.Col(id='ataque-container', width="auto"),  # Contenedor para métricas de Ataque
        dbc.Col(id='defensa-container', width="auto")  # Contenedor para métricas de Defensa
    ], style={"margin-bottom": "1rem"}),  # Espaciado inferior

    # Fila con el Dropdown para seleccionar el rango de jugadores
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-top-n',  # ID del componente Dropdown
                options=[  # Opciones generadas dinámicamente basadas en el número de jugadores
                    {'label': f'Top {i-9} - {i}', 'value': i} for i in range(10, len(df)+10, 10)
                ],
                value=10,  # Valor predeterminado
                clearable=False,  # No permite limpiar la selección
                style={"width": "50%", "margin-top": "1rem"}  # Estilo personalizado
            ), width=12)  # Ocupar toda la fila
    ], style={"margin-bottom": "1rem"}),  # Espaciado inferior

    # Gráfico interactivo para visualizar jugadores por rango
    dcc.Graph(id='graph-top-players'),
], style={"padding-top": "3rem"})  # Padding superior

# --- Callback para actualizar el gráfico y las tarjetas ---

@callback(
    [
        Output('graph-top-players', 'figure'),  # Actualiza el gráfico de jugadores
        Output('tc-average-container', 'children'),  # Actualiza la tarjeta de Tiros de Campo
        Output('tc1-average-container', 'children'),  # Actualiza la tarjeta de Tiros Libres
        Output('ataque-container', 'children'),  # Actualiza la tarjeta de Ataque
        Output('defensa-container', 'children')  # Actualiza la tarjeta de Defensa
    ],
    [Input('dropdown-top-n', 'value')]  # Escucha cambios en el valor seleccionado del Dropdown
)
def update_graph_and_label(top_n):
    """
    Actualiza el gráfico y las tarjetas según el rango seleccionado en el Dropdown.

    :param top_n: Número máximo de jugadores seleccionados en el rango.
    :return: Gráfico actualizado y componentes de las tarjetas.
    """
    # Determinar el rango de jugadores
    start_idx = top_n - 10  # Índice inicial del rango
    end_idx = min(top_n, len(df))  # Índice final (no exceder el número total de jugadores)
    
    # Seleccionar los jugadores dentro del rango especificado
    top_players = df.iloc[start_idx:end_idx].sort_values(by='PER Aproximado', ascending=True)
    
    # Crear el gráfico de barras horizontal usando Plotly Express
    fig = px.bar(
        top_players,  # Datos de los jugadores seleccionados
        y='Nombre',  # Eje Y: Nombres de los jugadores
        x='PER Aproximado',  # Eje X: Valor de PER Aproximado
        title=f"Jugadores {start_idx + 1} a {end_idx} por PER Aproximado (Orden Invertido)",  # Título dinámico
        labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},  # Etiquetas personalizadas
        color='PER Aproximado',  # Colorea las barras según el valor de PER Aproximado
        color_discrete_sequence=viridis_colors,  # Paleta de colores personalizada
        orientation="h"  # Orientación horizontal
    )

    # Actualizar las tarjetas usando componentes existentes y los jugadores seleccionados
    return (
        fig,
        AverageCardTC(top_players),  # Tarjeta para Tiros de Campo
        AverageCardTC1(top_players),  # Tarjeta para Tiros Libres
        CardAtaque(top_players),  # Tarjeta para Ataque
        CardDefensa(top_players)  # Tarjeta para Defensa
    )
