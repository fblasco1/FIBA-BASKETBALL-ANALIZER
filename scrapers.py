from selenium import webdriver
from bs4 import BeautifulSoup as bs

import time

# Set up the Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

def format_actions_fiba_basketball(quarter, actions, game_data, team):
    for action in actions:
            jugador = action.find('div', {'class': 'action'}).find('span', {'class': 'athlete-name'})
            if jugador == None:
                game_data[team]["actions"].append(
                    {
                        "quarter": quarter,
                        "player": "Equipo",
                        "action": action.find('div', {'class': 'action'}).find('span', {'class': 'action-description'}).text
                    }
                )
            if jugador != None:
                game_data[team]["actions"].append(
                    {
                        "quarter": quarter,
                        "player": jugador.text,
                        "action": action.find('div', {'class': 'action'}).find('span', {'class': 'action-description'}).text
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
            games.append({
                 "link": link_game
            })
    
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