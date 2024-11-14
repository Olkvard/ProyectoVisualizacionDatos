# average_card.py

from dash import html
import dash_bootstrap_components as dbc
import base64

# Cargar una imagen de balón en formato base64 (opcional)
# Si tienes una imagen local del balón, puedes codificarla en base64 y luego pegar el string aquí
# image_path = "ruta/a/balon.png"
# with open(image_path, "rb") as image_file:
#     base64_image = base64.b64encode(image_file.read()).decode()

# Componente de la tarjeta
def AverageCard(players_df):
    # Calcular el promedio de TCP2 (%) para el DataFrame de jugadores seleccionado
    tcp2_average = players_df["TC (%)"].mean()
    
    # Texto de promedio
    average_text = f"{tcp2_average:.2f}%"
    
    # Contenido de la tarjeta con estilo personalizado
    card_content = dbc.Row([
        dbc.Col(html.Div(
            average_text,
            style={"font-size": "2.5rem", "font-weight": "bold", "color": "#5a6e7f", "textAlign": "center"}
        ), width="auto"),
        
        dbc.Col(html.Div([
            html.Img(
                src="https://img.icons8.com/ios-filled/100/000000/soccer-ball.png",  # Icono en línea
                style={"height": "60px", "width": "60px"}
            ),
            html.P(["Promedio", html.Br(), "Tiros de Campo (%)"], 
                   style={"font-size": "1rem", "color": "#5a6e7f", "textAlign": "center"})
        ]), width="auto", style={"display": "flex", "align-items": "center", "justify-content": "center"})
    ], justify="center", align="center", style={"gap": "1rem"})

    # Tarjeta con el contenido
    return dbc.Card(
        dbc.CardBody(card_content),
        style={"width": "18rem", "padding": "1.5rem", "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"}
    )
