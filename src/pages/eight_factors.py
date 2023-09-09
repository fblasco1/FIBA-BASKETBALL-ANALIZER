from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from .data_generator import df_stats


layout = dbc.Container([
    dcc.Store(id="store"),
    dbc.Card(
        dbc.CardBody([
            html.H5("8 Factores"),
            html.Hr(),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dcc.Dropdown(
                                    id='equipo1-dropdown',
                                    options=df_stats.Equipo.unique(),
                                    value="Canadá",
                                    clearable=False,
                                    style={"width": 300},
                                    multi=False,
                                ),
                                dcc.Dropdown(
                                    id='equipo2-dropdown',
                                    options=df_stats.Equipo.unique(),
                                    value="Italia",
                                    clearable=False,
                                    style={"width": 300},
                                    multi=False,
                                    className="mx-2"
                                ),
                            ]
                        ),
                    ]
                )
            ),
            dbc.Tabs(
                [
                    dbc.Tab(label="Ofensiva", tab_id="ataque"),
                    dbc.Tab(label="Defensiva", tab_id="defensa"),
                ],
                id="tabs",
                active_tab="ataque",
                class_name="mt-4"
            ),
            html.Div(id="tab-content", className="p-1")
        ]), className="mt-4"
    )], fluid = True
)
    

# Define una función para actualizar los gráficos de barras
@callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), 
     Input('equipo1-dropdown', 'value'),
     Input('equipo2-dropdown', 'value')
    ]
)
def update_factor_charts(active_tab, equipo1, equipo2):
    if active_tab == "ataque":
        factores = ["eFG%", "%TO", "%ORB", "Ratio TL"]
    if active_tab == "defensa":
        factores = ["OPP_eFG%", "OPP_%TO", "%DRB", "OPP_Ratio TL"]

    # Inicializa una lista para almacenar los gráficos de barras
    charts = []

    # Crea gráficos de barras para cada factor en 4 columnas
    for factor in factores:
        datos_equipo1 = df_stats[df_stats['Equipo'] == equipo1]
        datos_equipo2 = df_stats[df_stats['Equipo'] == equipo2]

        fig = go.Figure(data=[
            go.Bar(name=equipo1, x=[equipo1], y=datos_equipo1[factor], marker_color='blue'),
            go.Bar(name=equipo2, x=[equipo2], y=datos_equipo2[factor], marker_color='green')
        ])

        fig.update_layout(
            title=f'{factor}',
            xaxis_title='Equipos',
            yaxis_title='Valor',
            barmode='group'
        )
        charts.append(dcc.Graph(figure=fig))

    # Divide los gráficos en 4 columnas
    cols = [dbc.Col(chart, width=3) for chart in charts]

    return dbc.Row(cols)