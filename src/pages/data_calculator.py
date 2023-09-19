import pandas as pd
from .analize_fiba_basketball import calculate_stats_advanced, shots_assited, stats

team_stats = pd.read_csv('D:/Escritorio/FIBA/src/data/09-11-2023_boxscore.csv', encoding='utf-8')
df_stats = calculate_stats_advanced(team_stats)

pbp = pd.read_csv('D:/Escritorio/FIBA/src/data/09-11-2023_pbp.csv', encoding='utf-8')
lineups = pd.read_csv('D:/Escritorio/FIBA/src/data/lineups.csv', encoding='utf-8')
stats(pbp, lineups)
shots_assits = shots_assited(pbp)

