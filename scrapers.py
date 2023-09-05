from selenium import webdriver
from bs4 import BeautifulSoup as bs

import time
import pandas as pd
from stats_advanced import eFG, ratio_tl, ORB, DRB, perdidas_plays

# Set up the Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

def format_actions_fiba_basketball(quarter, actions, game_data, team):
    for action in actions:
            jugador = action.find('div', {'class': 'action'}).find('span', {'class': 'athlete-name'})
            action_description = action.find('div', {'class': 'action'}).find('span', {'class': 'action-description'}).text
            if jugador == None:
                game_data[team]["actions"].append(
                    {
                        "quarter": quarter,
                        "player": "Equipo",
                        "action": action_description
                    }
                )
            if jugador != None:
                if action_description in "Hizo la asistencia":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "ASISTENCIA"
                        }
                    )
                if action_description in "Rebote Ofensivo":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "REBOTE OFENSIVO"
                        }
                    )
                if action_description in "Rebote Defensivo":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "REBOTE DEFENSIVO"
                        }
                    )
                if action_description in "Bloqueó el tiro":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "TAPA"
                        }
                    )
                if action_description in "Pérdida de balón":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "PERDIDA"
                        }
                    )
                if action_description in "Robo":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "RECUPERO"
                        }
                    )
                if action_description in "":
                    game_data[team]["actions"].append(
                        {
                            "quarter": quarter,
                            "player": jugador.text,
                            "action": "RECUPERO"
                        }
                    )

    return game_data


def scraper_fixture_fiba_basketball(link):
    driver.get(link)
    time.sleep(5)

    html = driver.page_source

    soup = bs(html, 'html.parser')

    games = []

    html_games = soup.find_all('div', {'class': "game_item"})

    for game in html_games:
        link_game = game.find('div', {'class': 'participants'}).find('a').get('href')
        if link_game != None:
            print(link_game)
            games.append(link_game)
    
    return games


def scraper_actions_fiba_basketball(games):
    pbps = []
    for game in games:
        print(game["link"])
        driver.get("https://www.fiba.basketball" + str(game["link"]) + "#|tab=play_by_play")
        time.sleep(5)

        html = driver.page_source

        soup = bs(html, 'html.parser')

        if soup.find('div', {'class': "game-page-no-content"}).text == "El partido no ha comenzado.": 
            pass

        game_data = {
            "team_a":{
                "name": soup.find('div', {'class': "team-A"}).find('span', {'class': "team-name"}).text,
                "actions": []
            },
            "team_b":{
                "name": soup.find('div', {'class': "team-B"}).find('span', {'class': "team-name"}).text,
                "actions": []
            }
        }

        game_data = format_actions_fiba_basketball(4, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q4'}).find_all('li', {'class': "action-item x--team-A"}), game_data, "team_a")
        game_data = format_actions_fiba_basketball(3, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q3'}).find_all('li', {'class': "action-item x--team-A"}), game_data, "team_a")
        game_data = format_actions_fiba_basketball(2, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q2'}).find_all('li', {'class': "action-item x--team-A"}), game_data, "team_a")
        game_data = format_actions_fiba_basketball(1, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q1'}).find_all('li', {'class': "action-item x--team-A"}), game_data, "team_a")

        game_data = format_actions_fiba_basketball(4, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q4'}).find_all('li', {'class': "action-item x--team-B"}), game_data, "team_b")
        game_data = format_actions_fiba_basketball(3, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q3'}).find_all('li', {'class': "action-item x--team-B"}), game_data, "team_b")
        game_data = format_actions_fiba_basketball(2, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q2'}).find_all('li', {'class': "action-item x--team-B"}), game_data, "team_b")
        game_data = format_actions_fiba_basketball(1, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q1'}).find_all('li', {'class': "action-item x--team-B"}), game_data, "team_b")

        pbps.append(game_data)

    return pbps


def scraper_boxscore_fiba_basketball_four_factors(links):
    games = []
    i = 0
    for link in links:
        i += 1
        driver.get("https://www.fiba.basketball" + link + "#tab=boxscore")
        time.sleep(5)

        html = driver.page_source

        soup = bs(html, 'html.parser')
        
        if soup.find("div", {'class': 'game-page-no-content'}).text == "El partido no ha comenzado.":
            continue

        boxscores = pd.read_html(html)

        boxscores[0].loc[boxscores[0]["#"] == "Totales", ["Jugadores"]] = soup.find('div', {'class': "team-A"}).find('span', {'class': "team-name"}).text

        boxscores[1].loc[boxscores[1]["#"] == "Totales", ["Jugadores"]] = soup.find('div', {'class': "team-B"}).find('span', {'class': "team-name"}).text
        
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['PTS_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Pts']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['PTS_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Pts']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCi']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[1]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCc']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[1].loc[boxscores[0]["#"] == "Totales", ['TCi']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[1]
        boxscores[1].loc[boxscores[0]["#"] == "Totales", ['TCc']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pc']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[1].loc[boxscores[0]["#"] == "Totales", ['3Pc']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLi']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[1]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLc']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[1].loc[boxscores[0]["#"] == "Totales", ['TLi']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[1]
        boxscores[1].loc[boxscores[0]["#"] == "Totales", ['TLc']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TO_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TO']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TO_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TO']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['RO_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['REBO']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['RO_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['REBO']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['RD_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['REBD']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['RD_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['REBD']].values[0][0]

        games.append(boxscores[0].loc[boxscores[0]["#"] == "Totales"])
        games.append(boxscores[1].loc[boxscores[1]["#"] == "Totales"])

    result = pd.concat(games)

    result = result.loc[:, ['Jugadores', 'Pts', 'TCc', 'TCi', '3Pc', 'TLc', 'TLi', 'TO', 'REBO', 'REBD', 'PTS_OPP', 'TCc_OPP', 'TCi_OPP', '3Pc_OPP', 'TLc_OPP', 'TLi_OPP', 'TO_OPP', 'RO_OPP', 'RD_OPP']]

    result["Pts"] = result["Pts"].astype(float)
    result["TCc"] = result["TCc"].astype(float) 
    result["TCi"] = result["TCi"].astype(float)
    result["3Pc"] = result["3Pc"].astype(float)
    result["TLc"] = result["TLc"].astype(float) 
    result["TLi"] = result["TLi"].astype(float)
    result["TO"] = result["TO"].astype(float)
    result["REBO"] = result["REBO"].astype(float) 
    result["REBD"] = result["REBD"].astype(float)
    result["PTS_OPP"] = result["PTS_OPP"].astype(float)
    result["TCc_OPP"] = result["TCc_OPP"].astype(float) 
    result["TCi_OPP"] = result["TCi_OPP"].astype(float)
    result["3Pc_OPP"] = result["3Pc_OPP"].astype(float)
    result["TLc_OPP"] = result["TLc_OPP"].astype(float) 
    result["TLi_OPP"] = result["TLi_OPP"].astype(float)
    result["TO_OPP"] = result["TO_OPP"].astype(float)
    result["RO_OPP"] = result["RO_OPP"].astype(float) 
    result["RD_OPP"] = result["RD_OPP"].astype(float)

    result = result.groupby("Jugadores").sum()

    equipos_prueba = result.index

    data_eight_factors = {
        "Equipo": equipos_prueba,
        #"Poss": [(result.loc[equipos[0], "TCi"] + 0.44 * result.loc[equipos[0], "TLi"] + result.loc[equipos[0], "TO"] - result.loc[equipos[0], "REBO"]), (result.loc[equipos[1], "TCi"] + 0.44 * result.loc[equipos[1], "TLi"] + result.loc[equipos[1], "TO"] - result.loc[equipos[1], "REBO"])],
        "eFG%": [eFG(result.loc[equipo, "TCi"], result.loc[equipo, "TCc"], result.loc[equipo, "3Pc"]) for equipo in equipos_prueba],
        "%TO": [perdidas_plays(result.loc[equipo, "TCi"], result.loc[equipo, "TO"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
        "%ORB": [ORB(result.loc[equipo, "REBO"], result.loc[equipo, "RD_OPP"]) for equipo in equipos_prueba],
        "%FT": [ratio_tl(result.loc[equipo, "TCi"], result.loc[equipo, "TLc"]) for equipo in equipos_prueba],
        "OPP_eFG%":  [eFG(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TCc_OPP"], result.loc[equipo, "3Pc_OPP"]) for equipo in equipos_prueba],
        "OPP_%TO": [perdidas_plays(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TO_OPP"], result.loc[equipo, "TLi_OPP"]) for equipo in equipos_prueba],
        "%DRB": [DRB(result.loc[equipo, "REBD"], result.loc[equipo, "RO_OPP"]) for equipo in equipos_prueba],
        "OPP_%FT": [ratio_tl(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLc_OPP"]) for equipo in equipos_prueba],
    }

    return pd.DataFrame(data_eight_factors)