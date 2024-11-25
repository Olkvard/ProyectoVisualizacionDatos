from dash import Dash, html, dcc, callback, Output, Input  # Importa componentes de Dash
import dash_bootstrap_components as dbc  # Biblioteca para diseño basado en Bootstrap
import plotly.express as px  # Para crear gráficos interactivos
import pandas as pd  # Biblioteca para manipulación de datos

# --- Carga y preprocesamiento de datos ---

# Cargar datos desde un archivo Excel
df = pd.read_excel("jugadores.xlsx")

# Crear columnas calculadas para métricas personalizadas (Ataque y Defensa)
df["Ataque"] = (
    (df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]  # Métricas ofensivas
    - (df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"]  # Penalización por métricas negativas
)
df["Defensa"] = (
    (df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"])
    / df["Minutos Jugados"]  # Métricas defensivas positivas
    - df["Faltas Personales Cometidas"] / df["Minutos Jugados"]  # Penalización por métricas negativas
)

# Limitar las métricas "Ataque" y "Defensa" para que estén entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

# Calcular el "PER Aproximado" como promedio de varias métricas
df["PER Aproximado"] = (
    df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]
) / 5

# --- Layout de la aplicación ---

scatter = dbc.Container(  # Contenedor principal de la página
    [
        html.Hr(),  # Separador horizontal
        html.H2("Análisis de dispersión de atributos"),  # Título de la página
        dbc.Row([  # Fila con dos dropdowns para seleccionar ejes X e Y
            dbc.Col(
                [
                    html.Label("Eje X:"),  # Etiqueta para el dropdown del eje X
                    dcc.Dropdown(
                        id="scatter-x-dropdown",  # ID del componente
                        options=[{'label': col, 'value': col} for col in df.columns if col not in ["Nombre"]],
                        value="Minutos Jugados",  # Valor predeterminado
                        clearable=False,  # No permite limpiar la selección
                    ),
                ],
                width=6,  # La columna ocupa 6 unidades de ancho
            ),
            dbc.Col(
                [
                    html.Label("Eje Y:"),  # Etiqueta para el dropdown del eje Y
                    dcc.Dropdown(
                        id="scatter-y-dropdown",  # ID del componente
                        options=[{'label': col, 'value': col} for col in df.columns if col not in ["Nombre"]],
                        value="Puntos Totales",  # Valor predeterminado
                        clearable=False,  # No permite limpiar la selección
                    ),
                ],
                width=6,  # La columna ocupa 6 unidades de ancho
            ),
        ]),
        dcc.Graph(id="scatter-plot"),  # Gráfico interactivo que se actualizará dinámicamente
    ],
    style={"backgroundColor": "#f0f0f0", "padding": "20px"},  # Estilo del contenedor
)

# --- Callback para actualizar el gráfico ---

@callback(
    Output("scatter-plot", "figure"),  # Salida: Figura del gráfico
    [
        Input("scatter-x-dropdown", "value"),  # Entrada: Valor seleccionado en el dropdown del eje X
        Input("scatter-y-dropdown", "value"),  # Entrada: Valor seleccionado en el dropdown del eje Y
    ],
)
def update_scatter_plot(x_axis, y_axis):
    """
    Actualiza el gráfico de dispersión según los ejes seleccionados por el usuario.

    :param x_axis: Columna seleccionada para el eje X.
    :param y_axis: Columna seleccionada para el eje Y.
    :return: Figura actualizada del gráfico de dispersión.
    """
    # Crear gráfico de dispersión con Plotly Express
    fig = px.scatter(
        df,  # DataFrame con los datos
        x=x_axis,  # Eje X
        y=y_axis,  # Eje Y
        title=f"Relación entre {x_axis} y {y_axis}",  # Título dinámico
        labels={x_axis: x_axis, y_axis: y_axis},  # Etiquetas dinámicas para los ejes
        color="PER Aproximado",  # Colorea los puntos según el valor de PER Aproximado
        color_continuous_scale="blues",  # Escala de colores
        hover_name="Nombre",  # Muestra el nombre del jugador al pasar el ratón
    )

    # Personalizar el diseño del gráfico
    fig.update_layout(
        plot_bgcolor="white",  # Fondo blanco del gráfico
        paper_bgcolor="white",  # Fondo blanco de la página
        font=dict(color="black"),  # Color negro para el texto
        title_font=dict(size=20),  # Tamaño de fuente del título
        xaxis=dict(
            showgrid=True,  # Mostrar líneas de la cuadrícula
            gridcolor="gray",  # Color de la cuadrícula
            zeroline=False,  # Ocultar la línea cero
            title_font=dict(size=16),  # Tamaño de la fuente del título del eje
        ),
        yaxis=dict(
            showgrid=True,  # Mostrar líneas de la cuadrícula
            gridcolor="gray",  # Color de la cuadrícula
            zeroline=False,  # Ocultar la línea cero
            title_font=dict(size=16),  # Tamaño de la fuente del título del eje
        ),
        coloraxis_colorbar=dict(  # Barra de colores
            title="PER Aproximado",  # Título de la barra
            thicknessmode="pixels",  # Modo de grosor en píxeles
            thickness=15,
            lenmode="fraction",  # Altura como fracción del gráfico
            len=0.6,
            yanchor="middle",  # Alinear verticalmente
            y=0.5,
        ),
    )

    # Configurar el diseño de los puntos en el gráfico
    fig.update_traces(
        marker=dict(size=8, opacity=0.8),  # Tamaño y transparencia de los puntos
        hovertemplate=(
            "<b>Jugador</b>: %{hovertext}<br>"
            f"<b>{x_axis}</b>: %{{x}}<br>"
            f"<b>{y_axis}</b>: %{{y}}<br>"
            "<b>PER Aproximado</b>: %{marker.color:.3f}<extra></extra>"
        ),  # Texto emergente al pasar el ratón
    )

    return fig

# --- Iniciar la aplicación ---

if __name__ == "__main__":
    scatter.run_server(debug=True)  # Ejecutar la aplicación en modo debug
