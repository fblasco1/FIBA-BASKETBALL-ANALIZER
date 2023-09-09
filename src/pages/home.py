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

                html.H5("Possesions", className="card-subtitle"),
                html.P("Es la fórmula que estima cuantas posesiones jugo un equipo y se basa en la suma de tiros de campo intentados, pérdidas \
                       y tiros libres ajustados por una constante calculada (0.44), a eso se le resta los rebotes ofensivos ya que la posesión finaliza cuando recupera el equipo que defiende" , className="card-text"),
                html.P("Poss = TCi + 0.44 * TLi + Per - RO", className="card-text"),
                html.Hr(),
            
                html.H5("Plays", className="card-subtitle"),
                html.P("Es lo mismo que las posesiones con la diferencia que si hay rebote ofensivo no se resta.", className="card-text"),
                html.P("Plays = TCi + 0.44 * TLi + Per", className="card-text"),
                html.Hr(),

                html.H5("Ofensive Efficiency Ratio (OER)", className="card-subtitle"),
                html.P("Mide la eficiencia ofensiva de un jugador o equipo cada 100 posesiones.", className="card-text"),
                html.P("OER = 100 * (PTS / Possessions)", className="card-text"),
                html.Hr(),

                html.H5("Defensive Efficiency Rating (DER)", className="card-subtitle"),
                html.P("Mide la eficiencia defensiva de un jugador o equipo cada 100 posesiones.", className="card-text"),
                html.P("DER = 100 * (PTS Opponent/ Possessions Opponent)", className="card-text"),
                html.Hr(),

                html.H5("True Shooting Percentage (TS%)", className="card-subtitle"),
                html.P("Ajusta el porcentaje de tiro de campo de un equipo o jugador incluyendo el tiro libre. Abarca todas las vías de anotación.", className="card-text"),
                html.P("TS% = 100 * (PTS / (2 * (TCi + 0.44 * TLi)))", className="card-text"),
                html.Hr(),

                html.H5("Effective Field Goal Percentage (eFG%)", className="card-subtitle"),
                html.P("Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5 respecto del estándar de porcentaje de tiro de campo.", className="card-text"),
                html.P("eFG% = 100 * ((TCC + 0.5 * T3C) / TCi)", className="card-text"),
                html.Hr(),

                html.H5("Points per Shot (PPS) from Two-Pointers", className="card-subtitle"),
                html.P("Mide los puntos por tiro de 2 de un jugador o equipo.", className="card-text"),
                html.P("PPS = (2Pc * 2) / 2Pi", className="card-text"),
                html.Hr(),

                html.H5("Points per Shot (PPS) from Three-Pointers", className="card-subtitle"),
                html.P("Mide los puntos por tiro de 3 de un jugador o equipo.", className="card-text"),
                html.P("PPS = (3Pc * 3) / 3Pi", className="card-text"),
                html.Hr(),

                html.H5("Assists per Possession", className="card-subtitle"),
                html.P("Ajusta la cantidad de asistencias de un jugador o equipo según la cantidad de posesiones.", className="card-text"),
                html.P("Assists per Possession = 100 * (AST / Possessions)", className="card-text"),
                html.Hr(),

                html.H5("Assists per Play", className="card-subtitle"),
                html.P("Ajusta la cantidad de asistencias de un jugador o equipo según la cantidad de jugadas.", className="card-text"),
                html.P("Assists per Play = 100 * (AST / Plays)", className="card-text"),
                html.Hr(),

                html.H5("Assist-Percentage Ratio (AST% Ratio)", className="card-subtitle"),
                html.P("Ajusta la cantidad de asistencias de un jugador o equipo según la cantidad de pérdidas.", className="card-text"),
                html.P("AST% Ratio = AST / PER", className="card-text"),
                html.Hr(),

                html.H5("Field Goals Assisted Percentage (FG% Assisted)", className="card-subtitle"),
                html.P("Mide el porcentaje de tiros de campo asistidos por un equipo.", className="card-text"),
                html.P("FG% Assisted = 100 * (AST / TCC)", className="card-text"),
                html.Hr(),

                html.H5("Steals per Possession (STL per Poss)", className="card-subtitle"),
                html.P("Ajusta la cantidad de robos de un equipo o jugador cada 100 posesiones del rival.", className="card-text"),
                html.P("STL per Poss = 100 * (STL / Possessions by Opponent)", className="card-text"),
                html.Hr(),

                html.H5("Steals per Play (STL per Play)", className="card-subtitle"),
                html.P("Ajusta la cantidad de robos de un equipo o jugador cada 100 jugadas del rival.", className="card-text"),
                html.P("STL per Play = 100 * (STL / Plays by Opponent)", className="card-text"),
                html.Hr(),

                html.H5("Turnovers per Possession (TO per Poss)", className="card-subtitle"),
                html.P("Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 posesiones.", className="card-text"),
                html.P("TO per Poss = 100 * (TO / Possessions)", className="card-text"),
                html.Hr(),

                html.H5("Turnovers per Play (TO per Play)", className="card-subtitle"),
                html.P("Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 jugadas.", className="card-text"),
                html.P("TO per Play = 100 * (TO / Plays)", className="card-text"),
                html.Hr(),

                html.H5("Block Percentage (BLK%)", className="card-subtitle"),
                html.P("Ajusta la cantidad de bloqueos de un equipo o jugador según la cantidad de tiros de 2 intentados del rival.", className="card-text"),
                html.P("BLK% = 100 * (BLK / 2Pc by Opponent)", className="card-text"),
                html.Hr(),

                html.H5("Free Throw Rate (FTR)", className="card-subtitle"),
                html.P("Mide la asiduidad con la que un jugador o equipo va a la línea de libres.", className="card-text"),
                html.P("FTR = 100 * (TLc / TCi)", className="card-text"),
                html.Hr(),

                html.H5("Two-Point Rate (2P%)", className="card-subtitle"),
                html.P("Mide la asiduidad con la que un jugador o equipo tira de 2.", className="card-text"),
                html.P("2P% = 100 * (2Pc / TCi)", className="card-text"),
                html.Hr(),

                html.H5("Three-Point Rate (3P%)", className="card-subtitle"),
                html.P("Mide la asiduidad con la que un jugador o equipo tira de 3.", className="card-text"),
                html.P("3P% = 100 * (3Pc / TCi)", className="card-text"),
                html.Hr(),

                html.H5("Points per Free Throw (PPS FT)", className="card-subtitle"),
                html.P("Mide los puntos por tiro de libre de un jugador o equipo.", className="card-text"),
                html.P("PPS FT = TLc / TLi", className="card-text"),
                html.Hr(),

                html.H5("Turnovers per Possession (TO per Poss)", className="card-subtitle"),
                html.P("Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 posesiones.", className="card-text"),
                html.P("TO per Poss = 100 * (TO / Possessions)", className="card-text"),
                html.Hr(),

                html.H5("Turnovers per Play (TO per Play)", className="card-subtitle"),
                html.P("Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 jugadas.", className="card-text"),
                html.P("TO per Play = 100 * (TO / Plays)", className="card-text"),
                html.Hr(),
            ]
        ), className="mt-2 p-2"
    )]
)