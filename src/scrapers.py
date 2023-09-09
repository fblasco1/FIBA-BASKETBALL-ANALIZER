from selenium import webdriver
from bs4 import BeautifulSoup as bs

import time
import pandas as pd

# Set up the Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

def format_actions_fiba_basketball(id, team, opponent, team_winner, quarter, actions):
    game = {
        "id": [],
        "team": [],
        "opponent": [],
        "quarter": [],
        "clock": [],
        "player": [],
        "action": [],
        "result": [],
        "team_winner": [],
    }
    for action in actions:
        clock = action.find('div', {'class': 'occurrence-info'}).find('span', {'class': 'time'}).text
        jugador = action.find('div', {'class': 'action'}).find('span', {'class': 'athlete-name'})
        action_description = action.find('div', {'class': 'action'}).find('span', {'class': 'action-description'}).text
        game["id"].append(id)
        game["team"].append(team)
        game["opponent"].append(opponent)
        game["quarter"].append(quarter)
        game["clock"].append(clock)
        game["team_winner"].append(team_winner)
        if jugador == None:
            game["player"].append("Equipo")
        elif jugador != None:
            game["player"].append(jugador.text)
        if "Rebote ofensivo" in action_description:
            game["action"].append("REBOTE OFENSIVO")
            game["result"].append(2)
        elif "Rebote defensivo" in action_description:
            game["action"].append("REBOTE DEFENSIVO")
            game["result"].append(2)
        elif "Hizo la asistencia" in action_description:
            game["action"].append("ASISTENCIA")
            game["result"].append(2)
        elif "Bloqueó el tiro" in action_description:
            game["action"].append("BLOQUEO")
            game["result"].append(2)
        elif "Pérdida de balón" in action_description:
            game["action"].append("PERDIDA")
            game["result"].append(2)
        elif "Robo" in action_description:
            game["action"].append("RECUPERO")
            game["result"].append(2)
        elif "Bandeja anotada" in action_description or "Bandeja anotado" in action_description or "2pts anotado" in action_description or "Palmeo anotado" in action_description or "Mate anotado" in action_description:
            game["action"].append("2P")
            game["result"].append(1)
        elif "Bandeja fallada" in action_description or "Bandeja fallado" in action_description or "Bandeja bloqueado" in action_description or "2pts fallado" in action_description or "Palmeo fallado" in action_description or "Mate fallado" in action_description or "Mate bloqueado" in action_description:
            game["action"].append("2P")
            game["result"].append(0)
        elif "3pts anotado" in action_description:
            game["action"].append("3P")
            game["result"].append(1)
        elif "3pts fallado" in action_description:
            game["action"].append("3P")
            game["result"].append(0)
        elif "tiros libres anotado" in action_description or "Tiro libre anotado" in action_description:
            game["action"].append("1P")
            game["result"].append(1)
        elif "tiros libres fallado" in action_description or "Tiro libre fallado" in action_description:
            game["action"].append("1P")
            game["result"].append(0)
        elif "Sustitución en" in action_description:
            game["action"].append("SUSTITUCIÓN")
            game["result"].append("Entra")
        elif "Sustitución fuera" in action_description:
            game["action"].append("SUSTITUCIÓN")
            game["result"].append("Sale")
        elif "Falta recibida" in action_description:
            game["action"].append("FR")
            game["result"].append(2)
        elif "Falta de ataque" in action_description or "Falta personal" in action_description or "falta técnica" in action_description or "Falta técnica" in action_description or "Falta antideportiva" in action_description:
            game["action"].append("FP")
            game["result"].append(2)
        elif "Salto inicial ganado" in action_description:
            game["action"].append("SI")
            game["result"].append(1)
        elif "Salto inicial perdido" in action_description:
            game["action"].append("SI")
            game["result"].append(0)
        else:
            game["action"].append(action_description)
            game["result"].append(2)
    
    return pd.DataFrame(game)


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


def scraper_actions_fiba_basketball(links):
    pbps = []
    for link in links:
        game_data = []
        print("pbp " + link)
        driver.get("https://www.fiba.basketball" + link + "#|tab=play_by_play")
        time.sleep(5)

        html = driver.page_source

        soup = bs(html, 'html.parser')

        if soup.find('div', {'class': "game-page-no-content"}).text == "El partido no ha comenzado.": 
            continue

        team_a = soup.find('div', {'class': "team-A"}).find('span', {'class': "team-name"}).text
        team_b = soup.find('div', {'class': "team-B"}).find('span', {'class': "team-name"}).text
        score_a = int(soup.find('div', {'class': "game-info"}).find('div', {'class': "final-score"}).find('span', {'class': "score-A"}).text)
        score_b = int(soup.find('div', {'class': "game-info"}).find('div', {'class': "final-score"}).find('span', {'class': "score-B"}).text)

        if score_a > score_b:
            team_w = team_a
        if score_a < score_b:
            team_w = team_b

        game_data.append(format_actions_fiba_basketball(link, team_a, team_b, team_w, 4, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q4'}).find_all('li', {'class': "action-item x--team-A"})))
        game_data.append(format_actions_fiba_basketball(link, team_a, team_b, team_w, 3, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q3'}).find_all('li', {'class': "action-item x--team-A"})))
        game_data.append(format_actions_fiba_basketball(link, team_a, team_b, team_w, 2, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q2'}).find_all('li', {'class': "action-item x--team-A"})))
        game_data.append(format_actions_fiba_basketball(link, team_a, team_b, team_w, 1, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q1'}).find_all('li', {'class': "action-item x--team-A"})))

        game_data.append(format_actions_fiba_basketball(link, team_b, team_a, team_w, 4, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q4'}).find_all('li', {'class': "action-item x--team-B"})))
        game_data.append(format_actions_fiba_basketball(link, team_b, team_a, team_w, 3, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q3'}).find_all('li', {'class': "action-item x--team-B"})))
        game_data.append(format_actions_fiba_basketball(link, team_b, team_a, team_w, 2, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q2'}).find_all('li', {'class': "action-item x--team-B"})))
        game_data.append(format_actions_fiba_basketball(link, team_b, team_a, team_w, 1, soup.find('ul', {'class': 'actions-list period_select_dependable', 'data_period_name': 'Q1'}).find_all('li', {'class': "action-item x--team-B"})))

        pbps.append(pd.concat(game_data))

    return pd.concat(pbps)


def scraper_boxscore_fiba_basketball(links):
    games = []
    i = 0
    for link in links:
        print(link)
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