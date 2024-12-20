from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
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

# Inicializar la aplicación
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def radar_chart(player_names, category_labels=None):
    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'Ataque', 'Defensa']
    fig = go.Figure()

    # Colores para los jugadores
    colors = ['blue', 'red']

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
            marker=dict(color=colors[i % len(colors)]),
            opacity=0.6
        ))

    # Configuración del diseño del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False, range=[0, 1]
            )
        ),
        showlegend=True,
        title="Comparación de Estadísticas de Jugadores"
    )

    return fig

top_10_jugadores = df.nlargest(10, 'PER Aproximado').sort_values(by='PER Aproximado', ascending=True)

# Layout de la app
app.layout = dbc.Container([
    html.H1("Gráfica de jugadores"),
    dcc.Graph(figure=px.bar(top_10_jugadores, y='Nombre', x='PER Aproximado', title="PER Aproximado de los Jugadores de Baloncesto",
                            labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},
                            color='PER Aproximado', color_continuous_scale='blues', orientation="h")),
    dcc.Dropdown(
        id='player-dropdown', 
        options=[{'label': name, 'value': name} for name in df['Nombre'].unique()],
        multi=True,
        placeholder="Selecciona uno o dos jugadores"
    ),
    dcc.Graph(id="radar-chart"),

    # Añadir scatterplot layout
    html.Hr(),
    html.H2("Análisis de dispersión de atributos"),
    dbc.Row([
        dbc.Col([
            html.Label("Eje X:"),
            dcc.Dropdown(
                id="scatter-x-dropdown",
                options=[{'label': col, 'value': col} for col in df.columns if col not in ["Nombre"]],
                value="Minutos Jugados",
                clearable=False,
            )
        ], width=6),
        dbc.Col([
            html.Label("Eje Y:"),
            dcc.Dropdown(
                id="scatter-y-dropdown",
                options=[{'label': col, 'value': col} for col in df.columns if col not in ["Nombre"]],
                value="Puntos Totales",
                clearable=False,
            )
        ], width=6),
    ]),
    dcc.Graph(id="scatter-plot"),
], style={"backgroundColor": "#f0f0f0", "padding": "20px"})


# Callback para actualizar el gráfico de radar
@app.callback(
    Output("radar-chart", "figure"),
    Input("player-dropdown", "value")
)
def update_radar_chart(player_names):
    # Asegurarse de que `player_names` es una lista y de que contiene uno o dos jugadores
    if player_names and len(player_names) > 0:
        return radar_chart(player_names, category_labels=['Tiros de 2', 'Tiros de 3', 'Tiros Libres', 'Ataque', 'Defensa'])
    return go.Figure()

# Callback para actualizar el scatterplot
@app.callback(
    Output("scatter-plot", "figure"),
    Input("scatter-x-dropdown", "value"),
    Input("scatter-y-dropdown", "value")
)
def update_scatter_plot(x_axis, y_axis):
    # Crear el gráfico de dispersión sin los nombres
    fig = px.scatter(
        df, x=x_axis, y=y_axis,
        title=f"Relación entre {x_axis} y {y_axis}",
        labels={x_axis: x_axis, y_axis: y_axis},
        color="PER Aproximado",
        color_continuous_scale="blues",
        hover_name="Nombre",
    )

    # Personalizar el diseño
    fig.update_layout(
        plot_bgcolor="white",                  # Fondo oscuro para el gráfico
        paper_bgcolor="white",                 # Fondo oscuro para el área exterior
        font=dict(color="black"),              # Color de texto blanco
        title_font=dict(size=20),              # Tamaño de la fuente del título
        xaxis=dict(
            showgrid=True,                     # Mostrar líneas de la cuadrícula en eje X
            gridcolor="gray",                  # Color de la cuadrícula
            zeroline=False,                    # Quitar línea cero
            title_font=dict(size=16)           # Tamaño de la fuente para título del eje X
        ),
        yaxis=dict(
            showgrid=True,                     # Mostrar líneas de la cuadrícula en eje Y
            gridcolor="gray",                  # Color de la cuadrícula
            zeroline=False,                    # Quitar línea cero
            title_font=dict(size=16)           # Tamaño de la fuente para título del eje Y
        ),
        coloraxis_colorbar=dict(
            title="PER Aproximado",            # Título de la barra de color
            thicknessmode="pixels",            # Ancho de la barra de color en píxeles
            thickness=15,
            lenmode="fraction",                # Altura de la barra de color como fracción
            len=0.6,
            yanchor="middle",
            y=0.5
        )
    )

    # Configurar hovertemplate y redondear el PER Aproximado a 3 decimales
    fig.update_traces(
        marker=dict(size=8, opacity=0.8),
        hovertemplate=(
            "<b>Jugador</b>: %{hovertext}<br>"
            f"<b>{x_axis}</b>: %{{x}}<br>"
            f"<b>{y_axis}</b>: %{{y}}<br>"
            "<b>PER Aproximado</b>: %{marker.color:.3f}<extra></extra>"
        )
    )

    return fig

# Iniciar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
