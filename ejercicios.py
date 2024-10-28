from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd 
import matplotlib.pyplot as plt
from math import pi

ds = pd.read_excel("jugadores.xlsx")

ds["porcentaje_rebotes"] = ds["Rebotes Ofensivos"]/ds["Nº Partidos jugados"]
ds["porcentaje_faltas"]  = ds["Faltas Personales Cometidas"]/ds["Nº Partidos jugados"]
ds["porcentaje_tapones"] = ds["Tapones Cometidos"]/ds["Nº Partidos jugados"]

ds.head()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('penguins.csv')
df['media_pico'] = df[['bill_length_mm', 'bill_depth_mm']].mean(axis=1)


def radarChart(player_name):

    # Filtrar el dataframe por el nombre del jugador
    player_data = ds[ds['Nombre'] == player_name]

    if player_data.empty:
        print(f"No se encontró al jugador {player_name} en el dataset.")
        return

    # Columnas que usaremos para el radar
    categories = ['TCP2 (%)', 'TCP3 (%)', 'TCP1 (%)', 'porcentaje_rebotes', 'porcentaje_faltas', 'porcentaje_tapones']
    
    # Obtener los valores del jugador en esas categorías
    values = player_data[categories].values.flatten().tolist()

    # Cerrar el gráfico anterior si lo hay
    plt.clf()

    # Preparar los ángulos del radar
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # Cerrar el círculo

    values += values[:1]  # Cerrar el gráfico

    # Inicializar el gráfico
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Dibujar el gráfico de radar
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)

    # Ajustes de las categorías y etiquetas
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Añadir título
    plt.title(f'Estadísticas de {player_name}', size=15, color='blue', y=1.1)
    
    return plt

player_name = 'Juan Pérez'

texto = html.H1(children="Grafica de pinguinos")
tabla = dash_table.DataTable(data=df.to_dict('records'), page_size=10)
mi_grafica = dcc.Graph(figure={})
radar_chart = radarChart(player_name)
radio = dcc.RadioItems(options=['Por sexo', 'Por isla'], value='Por sexo')

app.layout = dbc.Container([texto, tabla, radio, mi_grafica, radar_chart])

@app.callback(
    Output(mi_grafica, component_property="figure"),
    Input(radio, component_property= "value")
)
def actualizaGrafica(valor):
    if valor == 'Por sexo':
        fig = px.histogram(df, x="media_pico", color="sex")
    else:
        fig = px.histogram(df, x="media_pico", color="island")
    return fig


if __name__ == '__main__':
    app.run(debug=True)

    