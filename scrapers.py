from selenium import webdriver
from bs4 import BeautifulSoup as bs

import time
import pandas as pd

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


def scraper_boxscore_fiba_basketball(links):
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
        
        for boxscore in boxscores:
            boxscore.loc[boxscore["#"] == "Totales", ['TCc']] = boxscore.loc[boxscore["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[0]
            boxscore.loc[boxscore["#"] == "Totales", ['TCi']] = boxscore.loc[boxscore["#"] == "Totales", ['TC']].values[0][0].split(" ")[0].split("/")[1]
            boxscore.loc[boxscore["#"] == "Totales", ['2Pc']] = boxscore.loc[boxscore["#"] == "Totales", ['2 Pts']].values[0][0].split(" ")[0].split("/")[0]
            boxscore.loc[boxscore["#"] == "Totales", ['2Pi']] = boxscore.loc[boxscore["#"] == "Totales", ['2 Pts']].values[0][0].split(" ")[0].split("/")[1]
            boxscore.loc[boxscore["#"] == "Totales", ['3Pc']] = boxscore.loc[boxscore["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[0]
            boxscore.loc[boxscore["#"] == "Totales", ['3Pi']] = boxscore.loc[boxscore["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[1]
            boxscore.loc[boxscore["#"] == "Totales", ['3Pc']] = boxscore.loc[boxscore["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[0]
            boxscore.loc[boxscore["#"] == "Totales", ['3Pi']] = boxscore.loc[boxscore["#"] == "Totales", ['3 Pts']].values[0][0].split(" ")[0].split("/")[1]
            boxscore.loc[boxscore["#"] == "Totales", ['TLc']] = boxscore.loc[boxscore["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[0]
            boxscore.loc[boxscore["#"] == "Totales", ['TLi']] = boxscore.loc[boxscore["#"] == "Totales", ['TL']].values[0][0].split(" ")[0].split("/")[1]
            columnas_convertir = ['Pts', 'TCc', 'TCi', '2Pc', '2Pi', '3Pc', '3Pi', 'TLc', 'TLi', 'REBO', 'REBD', 'REB', 'AST', 'TO', 'ROB', 'BLQ', 'FP']
            boxscore.loc[boxscore["#"] == "Totales", columnas_convertir] = boxscore.loc[boxscore["#"] == "Totales", columnas_convertir].astype(float)
            boxscore.loc[boxscore["#"] == "Totales", ["game"]] = link 

        if boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Pts']].values[0][0] > boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Pts']].values[0][0]:
            boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Res']] = 1
            boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Res']] = 0
        if boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Pts']].values[0][0] < boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Pts']].values[0][0]:
            boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Res']] = 0
            boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Res']] = 1
        
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['PTS_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['Pts']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['PTS_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['Pts']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TCc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TCc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['2Pi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['2Pi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['2Pi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['2Pi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['2Pc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['2Pc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['2Pc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['2Pc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['3Pc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['3Pc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLi_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLi']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLi_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLi']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLc_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLc']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TLc_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TLc']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['RO_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['REBO']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['RO_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['REBO']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['RD_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['REBD']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['RD_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['REBD']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['AST_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['AST']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['AST_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['AST']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TO_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TO']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['TO_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['TO']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['ROB_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['ROB']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['ROB_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['ROB']].values[0][0]
        boxscores[0].loc[boxscores[0]["#"] == "Totales", ['FP_OPP']] = boxscores[1].loc[boxscores[1]["#"] == "Totales", ['FP']].values[0][0]
        boxscores[1].loc[boxscores[1]["#"] == "Totales", ['FP_OPP']] = boxscores[0].loc[boxscores[0]["#"] == "Totales", ['FP']].values[0][0]
        
        games.append(boxscores[0].loc[boxscores[0]["#"] == "Totales"])
        games.append(boxscores[1].loc[boxscores[1]["#"] == "Totales"])

    return pd.concat(games)