import numpy as np
from dash import dcc, html, Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from .data_calculator import shots_assits as df_asist_shots


layout = dbc.Container([
    dcc.Store(id="store"),
    dcc.Store(id="selected_equipos"),
    dcc.Store(id="selected_equipo"),
    dcc.Store(id="selected_quarter"),
    dbc.Card(
        dbc.CardBody([
            html.H5("Distribución de tiros"),
            html.Hr(),
            html.Div(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                                    [
                                        dbc.Row(
                                            dbc.Col(
                                                dbc.InputGroup(
                                                    [
                                                        dcc.Dropdown(
                                                            id='equipo-dropdown',
                                                            options=df_asist_shots.Equipo.unique(),
                                                            clearable=False,
                                                            style={"width": 300},
                                                            multi=False,
                                                            value="Alemania",
                                                            className="mx-2"
                                                        ),
                                                        dcc.Dropdown(
                                                            id='quarter-dropdown',
                                                            options=[
                                                                {'label': 'Mostrar Todos', 'value': 'Todos'},
                                                                * [{'label': quarter, 'value': quarter} for quarter in df_asist_shots.Cuarto.unique()]
                                                            ],
                                                            clearable=False,
                                                            style={"width": 300},
                                                            multi=False,
                                                            value='Todos',
                                                            className="mx-2"
                                                        ),
                                                    ]
                                                ),
                                            )
                                        ),
                                        dbc.Row(
                                            dbc.Col([
                                                dcc.Graph(id="sankey-diagram", style={'height': '800px', 'width': '100%'})
                                            ])
                                        )
                                    ],
                        title="Distribución de tiros por equipo",
                        )
                    ],
                flush=True,),
            ),
            html.Div(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                                    [
                                        dbc.Row(
                                            dbc.Col(
                                                dbc.InputGroup(
                                                    [
                                                        dcc.Dropdown(
                                                            id='quarter2-dropdown',
                                                            options=[
                                                                {'label': 'Mostrar Todos', 'value': 'Todos'},
                                                                * [{'label': quarter, 'value': quarter} for quarter in df_asist_shots.Cuarto.unique()]
                                                            ],
                                                            clearable=False,
                                                            style={"width": 300},
                                                            multi=True,
                                                            value="Todos",
                                                            className="mx-2"
                                                        )
                                                    ]
                                                ),
                                            )
                                        ),
                                        dbc.Row(
                                            dbc.Col([
                                                dcc.Graph(id="sunburst-graph", style={'height': '800px', 'width': '100%'})
                                            ])
                                        )
                                    ],
                        title="Distribución de tiros de los equipos",
                        )
                    ],
                flush=True,),
            ),
        ]), className="mt-4"
    )], fluid = True
)

# Define una función para crear un Gráfico Sunburst
def create_sunburst(selected_quarter):
    if selected_quarter != 'Todos':
        shots_df = df_asist_shots[(df_asist_shots['Cuarto'] == selected_quarter)]
    else:
        shots_df = df_asist_shots

    shots_df.loc[shots_df['Jugador Asistente'] != 'Unassisted', 'Jugador Asistente'] = "Assisted"

    # Crear el gráfico Sunburst
    fig = px.sunburst(shots_df, path=['Tipo de Tiro', 'Jugador Asistente', 'Equipo'], title='Gráfico Sunburst de Tiros')

    return fig


# Define una función para crear el Sankey Diagram
def create_sankey_diagram(selected_equipo, selected_quarter):
    # Filtrar el DataFrame según las selecciones
    if selected_quarter == 'Todos':
        filtered_df = df_asist_shots[(df_asist_shots['Equipo'] == selected_equipo)]
    else:
        filtered_df = df_asist_shots[(df_asist_shots['Equipo'] == selected_equipo) & (df_asist_shots['Cuarto'] == selected_quarter)]

    # Crear nodos y enlaces para el Sankey Diagram
    nodes = [
        {'label': 'ASSIST'}, 
        {'label': 'UNASSIST'}
    ]

    # Obtener los nombres de los jugadores asistentes y ejecutantes del DataFrame
    jugadores_asistidor = np.append(filtered_df['Jugador Asistente'].unique(), "Non Player")
    jugadores_ejecutante = filtered_df['Jugador Ejecutante'].unique()


    # Agregar los nombres de jugadores asistentes y ejecutantes al conjunto de nodos con etiquetas específicas
    nodes.extend([{'label': "ASIST_" + jugador} for jugador in jugadores_asistidor])
    nodes.extend([{'label': "EJECUTANTE_" + jugador} for jugador in jugadores_ejecutante])
    nodes.extend([{'label': '1P'}, {'label': '2P'}, {'label': '3P'}])

    links = []

    # Crear enlaces ASSIST -> JUGADOR ASISTIDOR con valor de cantidad
    for jugador_asistidor in jugadores_asistidor:
        cantidad_asistencias = filtered_df[(filtered_df['Jugador Asistente'] != 'Unassisted') & (filtered_df['Jugador Asistente'] == jugador_asistidor)].shape[0]
        links.append({'source': 0, 'target': nodes.index({'label': "ASIST_" + jugador_asistidor}), 'value': cantidad_asistencias})

    cantidad_no_asisitidos = filtered_df[(filtered_df['Jugador Asistente'] == 'Unassisted')].shape[0]
    links.append({'source': 1, 'target': nodes.index({'label': "ASIST_Non Player"}), 'value': cantidad_no_asisitidos})

    # Crear enlaces NON ASIST -> TIPO DE TIRO con valor de cantidad
    for tiro in ['1P', '2P', '3P']:
        cantidad_tiros_unassisted = filtered_df[(filtered_df['Jugador Asistente'] == 'Unassisted') & (filtered_df['Tipo de Tiro'] == tiro)].shape[0]
        links.append({'source': nodes.index({'label': "ASIST_Non Player"}), 'target': nodes.index({'label': tiro}), 'value': cantidad_tiros_unassisted})

    # Crear enlaces JUGADOR ASISTIDOR -> TIPO DE TIRO con valor de cantidad
    for jugador_asistidor in jugadores_asistidor:
        for tiro in ['1P', '2P', '3P']:
            cantidad_tiros_asistidos = filtered_df[(filtered_df['Jugador Asistente'] != 'Unassisted') & (filtered_df['Jugador Asistente'] == jugador_asistidor) & (filtered_df['Tipo de Tiro'] == tiro)].shape[0]
            links.append({'source': nodes.index({'label': "ASIST_" + jugador_asistidor}), 'target': nodes.index({'label': tiro}), 'value': cantidad_tiros_asistidos})

    # Crear enlaces TIPO DE TIRO -> JUGADOR EJECUTANTE con valor de cantidad
    for tiro in ['1P', '2P', '3P']:
        for jugador_ejecutante in jugadores_ejecutante:
            cantidad_tiros_ejecutante = filtered_df[(filtered_df['Jugador Asistente'] != 'Unassisted') & (filtered_df['Tipo de Tiro'] == tiro) & (filtered_df['Jugador Ejecutante'] == jugador_ejecutante)].shape[0]
            links.append({'source': nodes.index({'label': tiro}), 'target': nodes.index({'label': "EJECUTANTE_" + jugador_ejecutante}), 'value': cantidad_tiros_ejecutante})

    # Crear el objeto figura del Sankey Diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[node['label'] for node in nodes],
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
        ),
    ))

    return fig

# Callback para actualizar el Sankey Diagram cuando se cambian las selecciones
@callback(
    Output("sankey-diagram", "figure"),
    [Input("equipo-dropdown", "value"), Input("quarter-dropdown", "value")]
)
def update_sankey_diagram(selected_equipo, selected_quarter):
    return create_sankey_diagram(selected_equipo, selected_quarter)

# Callback para actualizar el Sankey Diagram cuando se cambian las selecciones
@callback(
    Output("sunburst-graph", "figure"),
    [Input("quarter2-dropdown", "value")]
)
def update_sunburst_graph(selected_quarter2):
    return create_sunburst(selected_quarter2)