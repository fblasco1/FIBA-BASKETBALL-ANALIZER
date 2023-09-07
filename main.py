from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from pages import home, eight_factors, comparisson, shot_quality

#import scrapers

#hoy = datetime.now().strftime("%m-%d-%Y")

#fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")

#df = scrapers.scraper_boxscore_fiba_basketball(fixture)

#df.to_csv(hoy + '.csv')

# Inicializar la aplicación Dash
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.UNITED], 
           suppress_callback_exceptions=True, 
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    )

navbar = html.Nav([
                dbc.Container([
                    html.A(["FIBA WC 2023"], className="navbar-brand text-white", href="/home"),
                    html.Div([
                        html.Ul([
                            html.Li(
                                html.A("8 Factores", className="nav-link active text-white", href="/eight-factors"), className="nav-item"
                            ),
                            html.Li(
                                html.A("Comparador", className="nav-link text-white", href="/comparisson"), className="nav-item"
                            ),
                            html.Li(
                                html.A("Shot Quality", className="nav-link text-white", href="/shot-quality"), className="nav-item"
                            ),
                        ], className="navbar-nav me-auto")
                    ], className="collapse navbar-collapse")
                ], fluid=True)
            ], className="navbar navbar-expand-lg bg-primary"
        )

# Definir el diseño de la aplicación
app.layout = dbc.Container([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True)

@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/eight-factors':
        return eight_factors.layout
    elif pathname == '/comparisson':
        return comparisson.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)