from dash import html  # Importa componentes HTML para construir la interfaz
import dash_bootstrap_components as dbc  # Importa componentes Bootstrap para diseño estilizado
import pandas as pd  # Importa pandas para manipular y analizar datos en DataFrames

# --- Carga y preprocesamiento de datos ---

# Cargar datos desde un archivo Excel
df = pd.read_excel("jugadores.xlsx")

# Crear una columna "Defensa" en el DataFrame
# Calcula una métrica personalizada basada en estadísticas defensivas y penalizaciones
df["Defensa"] = (
    (df["Recuperaciones"] + df["Rebotes Defensivos"] + df["Tapones Cometidos"] + df["Faltas Personales Recibidas"])
    / df["Minutos Jugados"]  # Métricas defensivas positivas normalizadas por minutos jugados
    - df["Faltas Personales Cometidas"] / df["Minutos Jugados"]  # Penalización por métricas negativas
)

# Limitar los valores de la métrica "Defensa" entre 0 y 1 para mantener consistencia
df["Defensa"] = df["Defensa"].clip(0, 1)

# --- Componente de la tarjeta personalizada ---

def CardDefensa(players_df):
    """
    Genera una tarjeta que muestra el promedio de la métrica "Defensa" para los jugadores seleccionados.
    
    :param players_df: DataFrame con los datos de los jugadores seleccionados.
    :return: Un componente Dash Card con diseño Bootstrap.
    """
    
    # Calcular el promedio de la columna "Defensa" en el DataFrame proporcionado
    tcp2_average = players_df["Defensa"].mean()
    
    # Formatear el promedio como texto con dos decimales seguido de un porcentaje
    average_text = f"{tcp2_average:.2f}%"
    
    # Crear el contenido de la tarjeta usando un diseño de filas y columnas
    card_content = dbc.Row([
        # Columna con el texto grande del promedio
        dbc.Col(html.Div(
            average_text,  # Muestra el promedio calculado
            style={  # Estilo CSS para el texto
                "font-size": "2.5rem",  # Tamaño grande del texto
                "font-weight": "bold",  # Negrita
                "color": "#5a6e7f",  # Color azul grisáceo
                "textAlign": "center"  # Centrado horizontalmente
            }
        ), width="auto"),  # El ancho se ajusta automáticamente al contenido
        
        # Columna con una descripción del promedio
        dbc.Col(html.Div([
            # Etiqueta con el texto explicativo
            html.P(
                ["Promedio Participación", html.Br(), "Defensa"],  # Etiqueta con salto de línea
                style={
                    "font-size": "1rem",  # Tamaño de fuente más pequeño
                    "color": "#5a6e7f",  # Mismo color azul grisáceo
                    "textAlign": "center"  # Texto centrado
                }
            )
        ]), width="auto", style={  # Estilo CSS adicional para centrar vertical y horizontalmente
            "display": "flex",
            "flex-direction": "column",  # Dirección de los elementos dentro de la columna
            "align-items": "center",  # Alinear horizontalmente en el centro
            "justify-content": "center"  # Alinear verticalmente en el centro
        })
    ], justify="center", align="center", style={"gap": "1rem"})  # Centrar el contenido de las columnas con un espacio entre ellas

    # Crear la tarjeta principal utilizando el contenido creado
    return dbc.Card(
        dbc.CardBody(card_content),  # El cuerpo de la tarjeta contiene el diseño de filas y columnas
        style={  # Estilo personalizado para la tarjeta
            "width": "18rem",  # Ancho fijo de la tarjeta
            "padding": "1.5rem",  # Espaciado interno
            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)"  # Sombra suave para un efecto de profundidad
        }
    )
