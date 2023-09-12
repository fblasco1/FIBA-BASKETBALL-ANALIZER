from datetime import datetime
import pandas as pd
import scrapers

from analize_fiba_basketball import calculate_stats_advanced, shots_assited

hoy = datetime.now().strftime("%m-%d-%Y")

fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")

scrapers.scraper_boxscore_fiba_basketball(fixture).to_csv(hoy + '_boxscore.csv')

scrapers.scraper_actions_fiba_basketball(fixture).to_csv(hoy + '_pbp.csv')