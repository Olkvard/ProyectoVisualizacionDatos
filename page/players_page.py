from dash import html, dcc, callback, Output, Input  # Componentes principales de Dash
import dash_bootstrap_components as dbc  # Para el diseño y estilo con Bootstrap
import plotly.graph_objects as go  # Para gráficos personalizados como gráficos de radar
import pandas as pd  # Para manipular datos con DataFrames

# --- Carga y preprocesamiento de datos ---

# Cargar datos desde un archivo Excel
df = pd.read_excel("jugadores.xlsx")

# Crear una columna "Ataque" basada en métricas ofensivas y penalizaciones
df["Ataque"] = (
    (df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]
    - (df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"]
)

# Crear una columna "Defensa" basada en métricas defensivas y penalizaciones
df["Defensa"] = (
    (df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"])
    / df["Minutos Jugados"]
    - (df["Faltas Personales Cometidas"]) / df["Minutos Jugados"]
)

# Limitar las métricas "Ataque" y "Defensa" para que estén entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

# Calcular el "PER Aproximado" como una métrica compuesta basada en varias estadísticas clave
df['PER Aproximado'] = (
    df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]
) / 5

# Paleta de colores accesibles para los gráficos
COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Azul, naranja, verde, rojo, púrpura

# --- Función para generar un gráfico de radar ---

def radar_chart(player_names, category_labels=None):
    """
    Genera un gráfico de radar que compara estadísticas de jugadores seleccionados.
    
    :param player_names: Lista de nombres de jugadores a incluir en el gráfico.
    :param category_labels: Etiquetas de las categorías del gráfico.
    :return: Gráfico de radar como objeto `go.Figure`.
    """
    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'Ataque', 'Defensa']  # Estadísticas para el radar
    fig = go.Figure()  # Crear una figura vacía

    # Iterar sobre los jugadores seleccionados
    for i, player_name in enumerate(player_names):
        # Filtrar datos del jugador actual
        player_data = df[df['Nombre'] == player_name]
        if player_data.empty:  # Saltar si no hay datos para el jugador
            continue

        # Obtener los valores de las métricas seleccionadas y cerrar el círculo del radar
        values = player_data[categories].values.flatten().tolist()
        values += values[:1]  # Añadir el primer valor al final para cerrar el gráfico

        # Ajustar etiquetas de las categorías
        category_labels = category_labels or categories
        category_labels += category_labels[:1]

        # Añadir una traza para el jugador al gráfico de radar
        fig.add_trace(go.Scatterpolar(
            r=values,  # Valores de las métricas
            theta=category_labels,  # Etiquetas de las categorías
            fill='toself',  # Rellenar el área bajo la línea
            name=player_name,  # Nombre del jugador
            marker=dict(color=COLORS[i % len(COLORS)]),  # Usar un color accesible
            opacity=0.6  # Transparencia para el relleno
        ))

    # Configurar el diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,  # Mostrar líneas radiales
                range=[0, 1]  # Establecer el rango del eje radial
            )
        ),
        showlegend=True,  # Mostrar la leyenda con los nombres de los jugadores
        title="Comparación de Estadísticas de Jugadores"  # Título del gráfico
    )

    return fig

# --- Layout de la página ---

players_page_content = dbc.Container([  # Contenedor principal de la página
    html.H1("Gráfica de jugadores"),  # Título de la página
    
    # Dropdown para seleccionar jugadores
    dcc.Dropdown(
        id='player-dropdown',  # ID del componente
        options=[{'label': name, 'value': name} for name in df['Nombre'].unique()],  # Opciones basadas en los nombres de los jugadores
        multi=True,  # Permitir seleccionar múltiples jugadores
        placeholder="Selecciona hasta 5 jugadores"  # Texto de ayuda
    ),
    
    # Gráfico de radar
    dcc.Graph(id="radar-chart"),  # Gráfico interactivo que se actualizará dinámicamente
], style={"padding-top": "40px"})  # Separar el contenido de la parte superior

# --- Callback para actualizar el gráfico de radar ---

@callback(
    Output("radar-chart", "figure"),  # Salida: Gráfico de radar
    Input("player-dropdown", "value")  # Entrada: Jugadores seleccionados desde el Dropdown
)
def update_radar_chart(player_name):
    """
    Callback que actualiza el gráfico de radar en función de los jugadores seleccionados.
    
    :param player_name: Lista de nombres de los jugadores seleccionados.
    :return: Figura del gráfico de radar actualizada.
    """
    if player_name:  # Si hay jugadores seleccionados
        # Validar que no se seleccionen más de 5 jugadores
        if len(player_name) > 5:
            player_name = player_name[:5]  # Limitar la lista a los primeros 5 jugadores
            print("Has seleccionado más de 5 jugadores. Solo los primeros 5 se incluirán en el gráfico.")

        # Generar el gráfico de radar con los jugadores seleccionados
        return radar_chart(player_name, category_labels=['Tiros de 2', 'Tiros de 3', 'Tiros Libres', 'Ataque', 'Defensa'])

    # Si no hay jugadores seleccionados, devolver un gráfico vacío
    return go.Figure()
