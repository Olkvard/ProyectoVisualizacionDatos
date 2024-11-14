from dash import html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="./assets/images/federacion_baloncesto.png", style={"width": "3rem"}),
                html.H4("WorldCup", className="m-0"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="tf-icons bx bx-trophy fas fa-home"), html.Span("Leage Results" , className="me-2")],
                    href="/",
                    active="exact",
                    className="pe-3"
                ),
                dbc.NavLink(
                    [
                        html.I(className="menu-icon tf-icons bx bx-group"),
                        html.Span("Players"),
                    ],
                    href="/players",
                    active="exact",
                    className="pe-3"
                ),
                dbc.NavLink(
                    [
                        html.I(className="menu-icon tf-icons bx bx-info-circle"),
                        html.Span("Scatter"),
                    ],
                    href="/scatter",
                    active="exact",
                    className="pe-3",
                ),
                dbc.NavLink(
                    [
                        html.I(className="menu-icon tf-icons bx bx-info-circle"),
                        html.Span("About"),
                    ],
                    href="/about",
                    active="exact",
                    className="pe-3",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar bg-menu-theme",
)