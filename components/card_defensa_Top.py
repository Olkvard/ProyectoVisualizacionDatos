from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_excel("jugadores.xlsx")

df["Defensa"] = ((df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"]) / df["Minutos Jugados"]) - (df["Faltas Personales Cometidas"] / df["Minutos Jugados"])

df["Defensa"] = df["Defensa"].clip(0, 1)

# Componente de la tarjeta
def CardDefensa(players_df):
    # Calcular el promedio de TCP2 (%) para el DataFrame de jugadores seleccionado
    tcp2_average = players_df["Defensa"].mean()
    
    # Texto de promedio
    average_text = f"{tcp2_average:.2f}%"
    
    # Contenido de la tarjeta con estilo personalizado
    card_content = dbc.Row([
        dbc.Col(html.Div(
            average_text,
            style={"font-size": "2.5rem", "font-weight": "bold", "color": "#5a6e7f", "textAlign": "center"}
        ), width="auto"),
        
        dbc.Col(html.Div([
            html.P(["Promedio Participación", html.Br(), "Defensa"], 
                   style={"font-size": "1rem", "color": "#5a6e7f", "textAlign": "center"})
        ]), width="auto", style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center"})
    ], justify="center", align="center", style={"gap": "1rem"})

    # Tarjeta con el contenido
    return dbc.Card(
        dbc.CardBody(card_content),
        style={"width": "18rem", "padding": "1.5rem", "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"}
    )
