# app.py

from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from components.NavbarVertical import sidebar  # Importamos el sidebar desde NavbarVertical
from components.Footer import Footer
from page.leage_players_page import leage_players
from page.players_page import players_page_content
from page.about import about_page_content

# Inicializamos la aplicación
app = Dash(__name__,title="Basket Analitics",
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True)

server = app.server

# Definimos el layout de la aplicación
app.layout = html.Div(
    className="layout-wrapper layout-content-navbar",
    children=[
        html.Div(
            className="layout-container",
            children=[
                dcc.Location(id="url"),
                html.Aside(
                    className="",
                    children=[sidebar]
                ),
                html.Div(
                    className="layout-page",
                    children=[
                        html.Div(
                            className="content-wrapper",
                            children=[
                                html.Div(
                                    className="container-xxl flex-grow-1 container-p-y p-0",
                                    id="page-content",
                                    children=[]
                                ),
                                html.Footer(
                                    className="content-footer footer bg-footer-theme",
                                    children=[Footer],
                                    style={"margin-left": "6rem"}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def routing(path):
    if path == "/":
        return leage_players
    elif path == "/players":
        return players_page_content
    elif path == "/about":
        return about_page_content
    else:
        return html.H2("404"), html.P("Página no encontrada.")

# Callback para actualizar el contenido según la pagina seleccionada
#@callback(
#    Output("page-content", "children"),
#    Input("url", "pathname")
#)
# Funcion de cambio de pagina 
#def display_page(pathname):
#    if pathname == "/":
#        return html.H2("League Players"), html.P("Esta es la página de torneos.")
#    elif pathname == "/players":
#        return players_page_content  # Llama al contenido de la página de Players
#    elif pathname == "/about":
#        return html.H2("About"), html.P("Esta es la página de información.")
#    else:
#        return html.H2("404"), html.P("Página no encontrada.")

# Componente dcc.Location para rastrear la URL actual
#app.layout.children.insert(0, dcc.Location(id="url"))

# Ejecutamos la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)