from dash import  dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_excel("jugadores.xlsx")

# Crear columnas de ataque y defensa
df["Ataque"] = ((df["Puntos Totales"] + df["Rebotes Ofensivos"] + df["Asistencias"]) / df["Minutos Jugados"]) - ((df["Tapones Recibidos"] + df["Pérdidas"]) / df["Minutos Jugados"])
df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

# Limitar los valores de "Ataque" y "Defensa" entre 0 y 1
df["Ataque"] = df["Ataque"].clip(0, 1)
df["Defensa"] = df["Defensa"].clip(0, 1)

df['PER Aproximado'] = (df["TCP1 (%)"] + df["TCP2 (%)"] + df["TCP3 (%)"] + df["Ataque"] + df["Defensa"]) / 5

top_10_jugadores = df.nlargest(10, 'PER Aproximado').sort_values(by='PER Aproximado', ascending=True)

leage_players = dbc.Container([
    dcc.Graph(figure=px.bar(top_10_jugadores, y='Nombre', x='PER Aproximado', title="PER Aproximado de los Jugadores de Baloncesto",
                            labels={'PER Aproximado': 'PER Aproximado', 'Nombre': 'Jugador'},
                            color='PER Aproximado', color_continuous_scale='greens', orientation="h")),

],style={"padding-top": "3rem"})