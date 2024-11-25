from dash import html  # Importa componentes HTML para construir la interfaz
import dash_bootstrap_components as dbc  # Importa componentes Bootstrap para diseño estilizado

# --- Sidebar (barra de navegación lateral) ---

sidebar = html.Div(  # Contenedor principal del sidebar
    [
        # --- Encabezado del Sidebar ---
        html.Div(
            [
                # Imagen del logo de la federación
                html.Img(
                    src="./assets/images/federacion_baloncesto.png",  # Ruta de la imagen
                    style={"width": "3rem"}  # Ajusta el ancho de la imagen
                ),
                # Título del Sidebar
                html.H4("WorldCup", className="m-0"),  # Título con clase CSS para márgenes
            ],
            className="sidebar-header",  # Clase CSS para estilo del encabezado
        ),
        
        html.Hr(),  # Línea horizontal de separación
        
        # --- Navegación con enlaces ---
        dbc.Nav(
            [
                # --- Enlace a la página "League Results" ---
                dbc.NavLink(
                    [
                        # Icono para el enlace
                        html.I(className="tf-icons bx bx-trophy fas fa-home"),  
                        # Texto del enlace
                        html.Span("Leage Results", className="me-2"),  
                    ],
                    href="/",  # Ruta a la que redirige el enlace
                    active="exact",  # Marca el enlace como activo si coincide exactamente con la ruta
                    className="pe-3"  # Clase CSS para espaciado a la derecha
                ),
                
                # --- Enlace a la página "Players" ---
                dbc.NavLink(
                    [
                        # Icono para el enlace
                        html.I(className="menu-icon tf-icons bx bx-group"),  
                        # Texto del enlace
                        html.Span("Players"),
                    ],
                    href="/players",  # Ruta a la que redirige el enlace
                    active="exact",  # Marca el enlace como activo si coincide exactamente con la ruta
                    className="pe-3",  # Clase CSS para espaciado a la derecha
                ),
                
                # --- Enlace a la página "Scatter" ---
                dbc.NavLink(
                    [
                        # Icono para el enlace
                        html.I(className="menu-icon tf-icons bx bx-info-circle"),  
                        # Texto del enlace
                        html.Span("Scatter"),
                    ],
                    href="/scatter",  # Ruta a la que redirige el enlace
                    active="exact",  # Marca el enlace como activo si coincide exactamente con la ruta
                    className="pe-3",  # Clase CSS para espaciado a la derecha
                ),
                
                # --- Enlace a la página "About" ---
                dbc.NavLink(
                    [
                        # Icono para el enlace
                        html.I(className="menu-icon tf-icons bx bx-info-circle"),  
                        # Texto del enlace
                        html.Span("About"),
                    ],
                    href="/about",  # Ruta a la que redirige el enlace
                    active="exact",  # Marca el enlace como activo si coincide exactamente con la ruta
                    className="pe-3",  # Clase CSS para espaciado a la derecha
                ),
            ],
            vertical=True,  # Disposición vertical de los enlaces
            pills=True,  # Estilo de pestañas activas para los enlaces
        ),
    ],
    className="sidebar bg-menu-theme",  # Clase CSS para estilo general del sidebar
)
