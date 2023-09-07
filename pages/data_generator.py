import pandas as pd

from analize_fiba_basketball import calculate_stats_advanced 

#import scrapers

#hoy = datetime.now().strftime("%m-%d-%Y")

#fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")

#df = scrapers.scraper_boxscore_fiba_basketball(fixture)

#df.to_csv(hoy + '.csv')

df_stats = pd.read_excel('09-05-2023.xlsx')

df = calculate_stats_advanced(df_stats)