from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from io import BytesIO
import base64

# Cargar datos
df = pd.read_excel("jugadores.xlsx")

# Crear columnas de ataque y defensa
df["Ataque"] = ((df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]) - ((df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"])
df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

# Limitar los valores de "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"])/5
# Inicializar la aplicación
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def radar_chart(player_name, category_labels):
    # Filtrar los datos del jugador
    player_data = df[df['Nombre'] == player_name]
    if player_data.empty:
        return None

    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'Ataque', 'Defensa']
    values = player_data[categories].values.flatten().tolist()
    
    # Configurar el gráfico de radar
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_xticks(angles[:-1])
    if category_labels:
        ax.set_xticklabels(category_labels)
    else:
        ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    plt.title(f'Estadísticas de {player_name}', size=15, color='blue', y=1.1)

    # Convertir el gráfico en imagen
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return f"data:image/png;base64,{data}"

# Layout de la app
app.layout = dbc.Container([
    html.H1("Gráfica de jugadores"),
    dcc.Graph(figure = px.bar(df, x='Nombre', y='PER Aproximado', title="PER Aproximado de los Jugadores de Baloncesto",
             labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},
             color='PER Aproximado', color_continuous_scale='Blues')),
    dcc.Dropdown(id='player-dropdown', options=[{'label': name, 'value': name} for name in df['Nombre'].unique()], placeholder="Selecciona un jugador"),
    html.Img(id="radar-chart", style={"width": "50%", "margin": "auto"}),
])

# Callback para actualizar el gráfico de radar
@app.callback(
    Output("radar-chart", "src"),
    Input("player-dropdown", "value")
)
def update_radar_chart(player_name):
    if player_name:
        return radar_chart(player_name, category_labels=['Tiros de 2', 'Tiros de 3', 'Tiros Libres', 'Ataque', 'Defensa'])
    return None

# Iniciar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
