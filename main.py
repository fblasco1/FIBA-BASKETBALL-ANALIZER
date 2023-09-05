from datetime import datetime
import pandas as pd
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go


import scrapers

hoy = datetime.now().strftime("%m-%d-%Y")

fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")

df = scrapers.scraper_boxscore_fiba_basketball(fixture)

df.to_csv('C:/Users/franc/Downloads/' + hoy + '.csv')


######################################################################
## Inicializar la aplicación Dash
#app = dash.Dash(__name__)
#
## Definir el diseño de la aplicación
#app.layout = dash.html.Div([
#    dash.html.Nav([
#        dash.html.H1("Dashboard de Comparación de Equipos"),
#    ]),
#    dash.html.Div([
#        dash.dcc.Dropdown(
#            id='equipo1-dropdown',
#            options=[{'label': equipo, 'value': equipo} for equipo in df['Equipo']],
#            value='USA',
#            multi=False
#        ),
#        dash.dcc.Dropdown(
#            id='equipo2-dropdown',
#            options=[{'label': equipo, 'value': equipo} for equipo in df['Equipo']],
#            value='Italia',
#            multi=False
#        ),
#    ], style={'width': '50%', 'display': 'block'}),
#    dash.html.Div(id='graficos',  style={"column-count":"4", "column-rule": "1px solid #bbb" }),
#])
#
## Definir la función para actualizar el gráfico
#@app.callback(
#    Output('graficos', 'children'),
#    Input('equipo1-dropdown', 'value'),
#    Input('equipo2-dropdown', 'value')
#)
#def actualizar_graficos(equipo1, equipo2):
#    graficos = []
#    
#    for metrica in df.columns[1:]:
#        datos_equipo1 = df[df['Equipo'] == equipo1]
#        datos_equipo2 = df[df['Equipo'] == equipo2]
#
#        fig = go.Figure(data=[
#            go.Bar(name=equipo1, x=[equipo1], y=datos_equipo1[metrica], marker_color='blue'),
#            go.Bar(name=equipo2, x=[equipo2], y=datos_equipo2[metrica], marker_color='green')
#        ])
#
#        fig.update_layout(
#            title=f'Comparación de {metrica}',
#            xaxis_title='Equipos',
#            yaxis_title='Valor',
#            barmode='group'
#        )
#
#        graficos.append(
#            dash.html.Div([
#                dash.dcc.Graph(
#                    id=f'grafico-{metrica}',
#                    figure=fig
#                )
#            ])
#        )
#
#    return graficos
#
#
#if __name__ == '__main__':
#    app.run_server(debug=True)