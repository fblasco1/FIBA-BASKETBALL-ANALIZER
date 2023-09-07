from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

layout = dbc.Container([
       dbc.Card(
        dbc.CardBody(
            [
                html.H3("Tubscout FIBA WC 2023 analizer ", className="card-title"),
                html.H5("¿Que es la estadística descriptiva?", className="card-subtitle"),
                html.P(
                    "La estadística descriptiva es una disciplina que se encarga de recoger, \
                    almacenar, ordenar, realizar tablas o gráficos y calcular parámetros básicos sobre el conjunto de datos. \
                    \
                    A continuación vamos a definir las métricas de estadística avanzada que utilizaremos para analizar el basquet y la copa del mundo.",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
                html.H5("Efective Field Goal Percentange (eFG%)", className="card-subtitle"),
                html.P(
                    "Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 \
                    respecto del estandar de porcentaje de tiro de campo.",
                    className="card-text",
                ),
                html.P(
                    "eFG% = 100 * (TCc + 0.5 * 3Pc / TCi)",
                    className="card-text",
                ),
                html.Hr(),
            ]
        ), className="mt-2 p-2"
    )]
)