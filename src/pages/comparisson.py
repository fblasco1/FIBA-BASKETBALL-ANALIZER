from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from PIL import Image
from .data_calculator import df_stats

layout = dbc.Container([
    dcc.Store(id="store"),
    dbc.Card(
        dbc.CardBody([
            html.H5("Comparador en contexto"),
            html.Hr(),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.InputGroup(
                            [
                                dbc.Label("Metrica en Y"),
                                dcc.Dropdown(
                                    id='metricaY-dropdown',
                                    options=df_stats.columns[1:],
                                    clearable=False,
                                    style={"width": 300},
                                    multi=False,
                                    value="OER_POSS",
                                    className="mx-2"
                                ),
                                dbc.Label("Metrica en X", className="mx-2"),
                                dcc.Dropdown(
                                    id='metricaX-dropdown',
                                    options=df_stats.columns[1:],
                                    clearable=False,
                                    style={"width": 300},
                                    multi=False,
                                    value="DER_POSS",
                                    className="mx-2"
                                ),
                            ]
                        ),
                    ]
                )
            ),
            dbc.Row(
                dbc.Col([
                    dbc.Label("Paises"),
                    dcc.Dropdown(
                        id='equipos-dropdown',
                        options=[
                            {'label': 'Seleccionar Todos', 'value': 'Todos'},
                            * [{'label': equipo, 'value': equipo} for equipo in df_stats.Equipo.unique()]
                        ],
                        value='Todos',
                        clearable=False,
                        multi=True,
                    ),
                ]),    
            ),
            dbc.Row(
                dbc.Col([
                    dcc.Graph(id="scatter-plot")
                ])
            )
        ]), className="mt-4"
    )], fluid = True
)

# Función para obtener la ruta de la bandera de un país
def obtener_ruta_bandera(pais):
    # Convierte el nombre del país a minúsculas y reemplaza espacios en blanco con '_'
    nombre_archivo = pais.lower().replace(" ", "_") + ".png"
    
    return f"D:\Escritorio\FIBA\\flags\{nombre_archivo}"

# Función para crear un scatter plot con imágenes en lugar de puntos
def crear_scatter_plot(data, metrica_x, metrica_y):
    # Calcular los valores promedio de las métricas seleccionadas
    promedio_x = data[metrica_x].mean()
    promedio_y = data[metrica_y].mean()

    fig = px.scatter(
            data,
            x=metrica_x,
            y=metrica_y
        )
    
    for index, row in data.iterrows():
        ruta_bandera = obtener_ruta_bandera(row["Equipo"])
        im = Image.open(ruta_bandera)

        fig.add_layout_image(
            x=row[metrica_x],
            y=row[metrica_y],
            source=im,
            xref="x",
            yref="y",
            sizex=3,
            sizey=3,
            xanchor="center",
            yanchor="middle",
        )
    
    # Agregar líneas horizontales y verticales para el promedio del torneo
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=min(data[metrica_x]) -5,
            x1=max(data[metrica_x]) +5,
            y0=promedio_y,
            y1=promedio_y,
            line=dict(color="blue", width=2),
        )
    )

    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=promedio_x,
            x1=promedio_x,
            y0=min(data[metrica_y]) - 5,
            y1=max(data[metrica_y]) + 5,
            line=dict(color="blue", width=2),
        )
    )

    fig.update_layout(
        xaxis_title=metrica_x,
        yaxis_title=metrica_y,
        showlegend=False,
    )

    return fig

# Actualizar la función de callback para utilizar el scatter plot personalizado
@callback(
    Output('scatter-plot', 'figure'),
    Input('metricaX-dropdown', 'value'),
    Input('metricaY-dropdown', 'value'),
    Input('equipos-dropdown', 'value')
)
def actualizar_scatter_plot(metrica_x, metrica_y, equipos_seleccionados):
    if 'Todos' in equipos_seleccionados:
        # Si se selecciona "Seleccionar Todos", se muestran todos los equipos
        data_filtrada = df_stats
    else:
        # Filtrar los datos por los equipos seleccionados
        data_filtrada = df_stats[df_stats['Equipo'].isin(equipos_seleccionados)]

    return crear_scatter_plot(data_filtrada, metrica_x, metrica_y)