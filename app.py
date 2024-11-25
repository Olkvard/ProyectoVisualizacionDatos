# Importación de módulos del sistema para configuración de rutas
import sys
import os

# Configuración del path del módulo actual para facilitar la importación de componentes
module_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__))))
if module_path not in sys.path:
    sys.path.append(module_path)  # Añadimos el directorio actual al path del sistema

# Importación de glob para buscar archivos según patrones específicos
import glob

# Importación de Dash y componentes adicionales
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc  # Componentes Bootstrap para diseño estilizado

# Importación de componentes personalizados
from components.NavbarVertical import sidebar  # Menú lateral de navegación (Sidebar)
from components.Footer import Footer  # Pie de página (Footer)
from page.leage_players_page import leage_players  # Página principal con análisis de jugadores
from page.players_page import players_page_content  # Página para análisis individual de jugadores
from page.about import about_page_content  # Página "Acerca de"
from page.scatter import scatter  # Página de gráfico de dispersión

# --- Configuración de rutas principales ---

# Ruta raíz de la aplicación
ROOT_FOLDER = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))  # Calculamos la carpeta raíz
SRC_FOLDER = os.path.join(ROOT_FOLDER, "src/")  # Carpeta fuente
ASSETS_FOLDER = os.path.join(SRC_FOLDER, "assets")  # Carpeta de recursos (estilos, imágenes, etc.)

# --- Carga de estilos externos (CSS) ---

# Buscamos archivos CSS en la carpeta de assets
external_style_sheet = glob.glob(os.path.join(
    ASSETS_FOLDER, "bootstrap/css") + "/*.css")  # Archivos CSS de Bootstrap
external_style_sheet += glob.glob(os.path.join(ASSETS_FOLDER, "css") + "/*.css")  # Archivos CSS personalizados
external_style_sheet += glob.glob(os.path.join(ASSETS_FOLDER, "fonts") + "/*.css")  # Archivos CSS para fuentes personalizadas

# --- Inicialización de la aplicación Dash ---

app = Dash(
    __name__,  # Nombre de la aplicación
    title="Basket Analytics",  # Título que aparecerá en la pestaña del navegador
    external_stylesheets=[dbc.themes.BOOTSTRAP] + external_style_sheet,  # Añadimos los estilos externos
    suppress_callback_exceptions=True  # Permitir callbacks dinámicos (no definidos al inicio)
)

# Servidor necesario para desplegar la aplicación en plataformas como Heroku
server = app.server

# --- Definición del layout principal de la aplicación ---

app.layout = html.Div(  # Contenedor principal de la aplicación
    className="layout-wrapper layout-content-navbar",  # Clase CSS para estructura general del diseño
    children=[
        html.Div(  # Contenedor para todo el layout
            className="layout-container",  # Clase CSS para estilos
            children=[
                # Componente para manejar rutas dinámicas (URLs)
                dcc.Location(id="url"),  
                
                # Menú lateral (Sidebar)
                html.Aside(
                    className="",  # Clase CSS (vacía para usar estilos predeterminados)
                    children=[sidebar]  # Importamos el componente Sidebar
                ),
                
                # Contenedor principal de la página
                html.Div(
                    className="layout-page",  # Clase CSS para estructura de la página
                    children=[
                        html.Div(  # Contenedor para el contenido principal
                            className="content-wrapper",  # Clase CSS para el contenido
                            children=[
                                html.Div(  # Contenedor para el contenido dinámico
                                    className="container-xxl flex-grow-1 container-p-y p-0",  # Clase CSS para estilos
                                    id="page-content",  # ID donde se cargará el contenido dinámico
                                    children=[]  # Inicialmente vacío
                                ),
                                
                                # Pie de página
                                html.Footer(
                                    className="content-footer footer bg-footer-theme",  # Clase CSS para estilos
                                    children=[Footer],  # Componente Footer importado
                                    style={"margin-left": "6rem"}  # Estilo personalizado
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# --- Callback para manejar el enrutamiento dinámico ---

@callback(
    Output(component_id='page-content', component_property='children'),  # Salida: Contenedor dinámico
    Input(component_id='url', component_property='pathname')  # Entrada: Cambios en la URL
)
def routing(path):
    """
    Función de enrutamiento que devuelve el contenido dinámico de la página 
    basado en la ruta actual de la URL.
    """
    if path == "/":  # Ruta principal
        return leage_players  # Cargar contenido de jugadores por liga
    elif path == "/players":  # Ruta para análisis individual de jugadores
        return players_page_content
    elif path == "/about":  # Ruta "Acerca de"
        return about_page_content
    elif path == "/scatter":  # Ruta para el gráfico de dispersión
        return scatter
    else:  # Ruta no encontrada
        return html.H2("404"), html.P("Página no encontrada.")  # Mensaje de error 404

# --- Ejecución de la aplicación ---

if __name__ == "__main__":
    app.run_server(debug=True)  # Ejecutar la app en modo debug para desarrollo
