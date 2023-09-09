from datetime import datetime
import pandas as pd
import src.scrapers as scrapers

from src.analize_fiba_basketball import calculate_stats_advanced, shots_assited

#hoy = datetime.now().strftime("%m-%d-%Y")
#
#fixture = scrapers.scraper_fixture_fiba_basketball("https://www.fiba.basketball/es/basketballworldcup/2023/games")
#
#df_stats = scrapers.scraper_boxscore_fiba_basketball(fixture)
#
#df_pbps = scrapers.scraper_actions_fiba_basketball(fixture)
#
#with pd.ExcelWriter(hoy + '.xlsx', engine='xlsxwriter') as writer:  
#    # Guardar el DataFrame df1 en la hoja "Hoja1"
#    df_stats.to_excel(writer, sheet_name='Stats', index=False)
#    
#    # Guardar el DataFrame df2 en la hoja "Hoja2"
#    df_pbps.to_excel(writer, sheet_name='PBP', index=False)

df_stats = calculate_stats_advanced(pd.read_excel('09-08-2023.xlsx', sheet_name='Stats'))
df_pbps = pd.read_excel('09-08-2023.xlsx', sheet_name='PBP')
df_asist_shots = shots_assited(df_pbps) 