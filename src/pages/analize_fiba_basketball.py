import time
import pandas as pd
import stats_advanced as sa
import ast

def calculate_stats_advanced(df):
    df["Poss"] = df.apply(lambda row: sa.possesions(row['TCi'], row['TO'], row['TLi'], row['REBO']), axis=1)
    df["Plays"] = df.apply(lambda row: sa.plays(row['TCi'], row['TO'], row['TLi']), axis=1)

    result = df.groupby(["Jugadores"]).sum()
    media = df[["Jugadores", "Poss", "Plays"]].groupby(["Jugadores"]).mean()

    equipos_prueba = result.index

    data_eight_factors = {
        "Equipo": equipos_prueba,
        "Possesions": [media.loc[equipo, "Poss"] for equipo in equipos_prueba],
        "Plays": [media.loc[equipo, "Plays"] for equipo in equipos_prueba],
        "OER_POSS": [sa.oer_poss(result.loc[equipo, "Pts"], result.loc[equipo, "TCi"],result.loc[equipo, "TO"], result.loc[equipo, "TLi"], result.loc[equipo, "REBO"]) for equipo in equipos_prueba],
        "DER_POSS": [sa.der_poss(result.loc[equipo, "PTS_OPP"], result.loc[equipo, "TCi_OPP"],result.loc[equipo, "TO_OPP"], result.loc[equipo, "TLi_OPP"], result.loc[equipo, "RO_OPP"]) for equipo in equipos_prueba],
        "OER_PLAYS": [sa.oer_plays(result.loc[equipo, "Pts"], result.loc[equipo, "TCi"],result.loc[equipo, "TO"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
        "DER_PLAYS": [sa.der_plays(result.loc[equipo, "PTS_OPP"], result.loc[equipo, "TCi_OPP"],result.loc[equipo, "TO_OPP"], result.loc[equipo, "TLi_OPP"]) for equipo in equipos_prueba],
        "eFG%": [sa.eFG(result.loc[equipo, "TCi"], result.loc[equipo, "TCc"], result.loc[equipo, "3Pc"]) for equipo in equipos_prueba],
        "TS%": [sa.true_shooting(result.loc[equipo, "Pts"], result.loc[equipo, "TCi"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
        "Ratio 3P": [sa.ratio_3p(result.loc[equipo, "3Pc"], result.loc[equipo, "TCi"]) for equipo in equipos_prueba],
        "PPS 3P": [sa.pps_3p(result.loc[equipo, "3Pi"], result.loc[equipo, "3Pc"]) for equipo in equipos_prueba],
        "Ratio 2P": [sa.ratio_2p(result.loc[equipo, "2Pc"], result.loc[equipo, "2Pi"]) for equipo in equipos_prueba],
        "PPS 2P": [sa.pps_2p(result.loc[equipo, "2Pi"], result.loc[equipo, "2Pc"]) for equipo in equipos_prueba],
        "Ratio TL": [sa.ratio_tl(result.loc[equipo, "TCi"], result.loc[equipo, "TLc"]) for equipo in equipos_prueba],
        "%ORB": [sa.ORB(result.loc[equipo, "REBO"], result.loc[equipo, "RD_OPP"]) for equipo in equipos_prueba],
        "%DRB": [sa.DRB(result.loc[equipo, "REBD"], result.loc[equipo, "RO_OPP"]) for equipo in equipos_prueba],
        "%TO": [sa.per_plays(result.loc[equipo, "TO"], result.loc[equipo, "TCi"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
        "%AST": [sa.ast_plays(result.loc[equipo, "AST"], result.loc[equipo, "TCi"], result.loc[equipo, "TLi"], result.loc[equipo, "TO"]) for equipo in equipos_prueba],
        "AST/TO": [sa.asist_per_ratio(result.loc[equipo, "AST"], result.loc[equipo, "TO"]) for equipo in equipos_prueba],
        "OPP_TS%": [sa.true_shooting(result.loc[equipo, "PTS_OPP"], result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLi_OPP"]) for equipo in equipos_prueba],
        "OPP_eFG%":  [sa.eFG(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TCc_OPP"], result.loc[equipo, "3Pc_OPP"]) for equipo in equipos_prueba],
        "OPP_Ratio 3P": [sa.ratio_3p(result.loc[equipo, "3Pc_OPP"], result.loc[equipo, "TCi_OPP"]) for equipo in equipos_prueba],
        "OPP_PPS 3P": [sa.pps_3p(result.loc[equipo, "3Pi_OPP"], result.loc[equipo, "3Pc_OPP"]) for equipo in equipos_prueba],
        "OPP_Ratio 2P": [sa.ratio_2p(result.loc[equipo, "2Pc_OPP"], result.loc[equipo, "2Pi_OPP"]) for equipo in equipos_prueba],
        "OPP_PPS 2P": [sa.pps_2p(result.loc[equipo, "2Pi_OPP"], result.loc[equipo, "2Pc_OPP"]) for equipo in equipos_prueba],
        "OPP_Ratio TL": [sa.ratio_tl(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLc_OPP"]) for equipo in equipos_prueba],
        "OPP_%ORB": [sa.ORB(result.loc[equipo, "RO_OPP"], result.loc[equipo, "REBD"]) for equipo in equipos_prueba],
        "OPP_%DRB": [sa.DRB(result.loc[equipo, "RD_OPP"], result.loc[equipo, "REBO"]) for equipo in equipos_prueba],
        "OPP_%TO": [sa.per_plays(result.loc[equipo, "TO_OPP"], result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLi_OPP"]) for equipo in equipos_prueba],
        "OPP_%AST": [sa.ast_plays(result.loc[equipo, "AST_OPP"], result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLi_OPP"], result.loc[equipo, "TO_OPP"]) for equipo in equipos_prueba],
        "OPP_AST/TO": [sa.asist_per_ratio(result.loc[equipo, "AST_OPP"], result.loc[equipo, "TO_OPP"]) for equipo in equipos_prueba],
    }

    return pd.DataFrame(data_eight_factors)

def shots_assited(df):
    df = df.dropna()
    # Filtrar las filas donde la acción es una ASISTENCIA
    assist_df = df[df['action'].str.contains('ASISTENCIA')]

    # Filtrar las filas donde la acción es un TIRO (1P, 2P o 3P)
    shot_types = ['1P', '2P', '3P']
    shot_df = df[df['action'].isin(shot_types)]

    # Unir los DataFrames de asistencia y tiro por las columnas 'id', 'quarter', y 'clock'
    merged_df = assist_df.merge(shot_df, on=['id', 'quarter', 'clock'], suffixes=('_asistencia', '_tiro'), how='inner')

    # Crear un nuevo DataFrame con las columnas requeridas, incluyendo 'action' (tipo de tiro)
    assisted_shots = pd.DataFrame({
        'ID': merged_df['id'],
        'Cuarto': merged_df['quarter'],
        'Clock': merged_df['clock'],
        'Jugador Asistente': merged_df['player_asistencia'],
        'Jugador Ejecutante': merged_df['player_tiro'],
        'Equipo': merged_df['team_asistencia'],
        'Tipo de Tiro': merged_df['action_tiro']
    })

    # Filtrar las filas donde 'result' es igual a 1
    shots_result_1 = shot_df[shot_df['result'] == "1"]

    # Filtrar las filas que no tienen una asistencia asociada (basado en id, clock y quarter)
    unassisted_shots = shots_result_1[~shots_result_1.set_index(['id', 'clock', 'quarter']).index.isin(assist_df.set_index(['id', 'clock', 'quarter']).index)]

    # Crear un nuevo DataFrame con las columnas requeridas
    unassisted_shots_df = pd.DataFrame({
        'ID': unassisted_shots['id'],
        'Cuarto': unassisted_shots['quarter'],
        'Clock': unassisted_shots['clock'],
        'Jugador Ejecutante': unassisted_shots['player'],
        'Equipo': unassisted_shots['team'],
        'Tipo de Tiro': unassisted_shots['action']
    })

    unassisted_shots_df["Jugador Asistente"] = "Unassisted"

    # Retornar el dataframe
    return pd.concat([unassisted_shots_df, assisted_shots])

#def extract_starters(link):
#    # Set up the Selenium webdriver
#    options = webdriver.ChromeOptions()
#    options.add_argument('--headless')  # Run Chrome in headless mode
#    driver = webdriver.Chrome(options=options)
#
#    driver.get("https://www.fiba.basketball" + link + "#tab=boxscore")
#    time.sleep(5)
#
#    html = driver.page_source
#
#    soup = bs(html, 'html.parser')
#
#    equipoA = soup.find('div', {'class': "team-A"}).find('span', {'class': "team-name"}).text
#    equipoB = soup.find('div', {'class': "team-B"}).find('span', {'class': "team-name"}).text
#
#    inicialesA = soup.find('section', {'class': "box-score_team-A"}).find_all('tr', {'class': 'x--player-is-starter'})
#    inicialesB = soup.find('section', {'class': "box-score_team-B"}).find_all('tr', {'class': 'x--player-is-starter'})
#
#    quintetoA = []
#    quintetoB = []
#
#    for inicial_tr in inicialesA:
#        quintetoA.append(
#            inicial_tr.find('a', {'class': 'player-profile-link'}).text.strip()
#        )
#
#    for inicial_tr in inicialesB:
#        quintetoB.append(
#            inicial_tr.find('a', {'class': 'player-profile-link'}).text.strip()
#        )
#    
#    return pd.DataFrame({
#        'id': [link, link],
#        'Equipo': [equipoA, equipoB],
#        'Quinteto': [quintetoA, quintetoB],
#        'PTS': [0, 0] ,
#        'FGm': [0, 0] ,
#        'FGa': [0, 0] ,
#        '2Pm': [0, 0] ,
#        '2Pa': [0, 0] ,
#        '3Pm': [0, 0] ,
#        '3Pa': [0, 0] ,
#        '1Pm': [0, 0] ,
#        '1Pa': [0, 0] ,
#        'RO' : [0, 0] ,
#        'RD' : [0, 0] ,
#        'RT' : [0, 0] ,
#        'AST': [0, 0] ,
#        'PER': [0, 0] ,
#        'REC': [0, 0] ,
#        'BLQ': [0, 0] ,
#        'POSS': [0, 0] ,
#        'PLAYS': [0, 0] ,
#        'PJ': [0, 0],
#    })

def stats(df, lineups, quarter = "Todos"):
    if quarter == "Todos":
        df[(df["action"] == "Tiempo muerto") | (df["action"] == "SI") | ( df["action"] == "Desafío rechazado") | (df["action"] == "Desafío aceptado")]
    else:
        df = df[df[quarter].isin(quarter) | df["action"] == "Tiempo muerto" | df["action"] == "SI" | df["action"] == "Desafío rechazado" | df["action"] == "Desafío aceptado"]
        
    totales = pd.DataFrame(columns=['id', 'team', 'opponent', 'player', 'quarter','PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD','RT', 'BLQ', 'FR', 'FP', 'Plays'])
    # Filtra las filas donde la acción es SUSTITUCIÓN y el resultado es ENTRA
    partidos_jugador = df[(df['action'] == 'SUSTITUCIÓN') & (df['result'] == 'Entra')]

    partidos_jugador = partidos_jugador.groupby(['team', 'player'])['id'].nunique().reset_index()
    partidos_jugador.columns = ['Equipo', 'Jugador', 'PJ']

    # Cuenta cuántos partidos jugó cada equipo
    partidos_equipo = df.groupby('team')['id'].nunique().reset_index()
    partidos_equipo.columns = ['Equipo', 'PJ']

    lineups['Quinteto'] = lineups['Quinteto'].apply(ast.literal_eval)

    for id_game in df["id"].unique():
        game_actions = df[df["id"] == id_game]
        total_filas = len(game_actions)
        dict_quint = {
             "id": id_game
        }
        for quinteto in lineups[lineups['id'] == id_game].iterrows():
            dict_quint[quinteto[1].Equipo] = quinteto[1].Quinteto
        # Recorre las filas de atrás hacia adelante
        for indice_fila in range(total_filas - 1, -1, -1):
            fila = game_actions.iloc[indice_fila]
            filtro = (totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter)
            if fila.action == "SUSTITUCIÓN" and fila.result == "Sale":
                    print("Hay un cambio SALE: " + fila.player + " " + str(fila.quarter) + " " + str(fila.clock) + " " + str(dict_quint[fila.team]))
                    dict_quint[fila.team].remove(fila.player)
                    print("QUEDAN: " + str(dict_quint[fila.team]))
            if fila.action == "SUSTITUCIÓN" and fila.result == "Entra":
                    print("Hay un cambio ENTRA: " + fila.player + " " + str(dict_quint[fila.team]))
                    dict_quint[fila.team].append(fila.player) 
                    print("QUEDAN: " + str(dict_quint[fila.team]))
                    filtro_q = (lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team])))                    
                    if filtro_q.any():
                        pass
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, dict_quint[fila.team], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                              columns=["id","Equipo","Quinteto","PTS","FGm","FGa","2Pm","2Pa","3Pm","3Pa","1Pm","1Pa","RO","RD","RT","AST","PER","REC","BLQ","POSS","PLAYS","PJ"])
                        lineups = pd.concat([lineups, nueva_fila], ignore_index=True)
            if fila.action == "2P" and fila.result == "1":
                if filtro.any():
                    #JUGADOR
                    totales.loc[filtro, "PTS"] += 2
                    totales.loc[filtro, "FGm"] += 1
                    totales.loc[filtro, "FGa"] += 1
                    totales.loc[filtro, "2Pm"] += 1
                    totales.loc[filtro, "2Pa"] += 1
                    totales.loc[filtro, "Plays"] += 1
                else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                    nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                                          columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                    totales = pd.concat([totales, nueva_fila], ignore_index=True)
                #TOTALES
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "PTS"] += 2
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGm"] += 1
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGa"] += 1
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "2Pm"] += 1
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "2Pa"] += 1
                totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "Plays"] += 1
                #QUINTETO
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PTS"] += 2
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGm"] += 1
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGa"] += 1
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "2Pm"] += 1
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "2Pa"] += 1
                lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "2P" and fila.result == "0":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "PTS"] += 2
                        totales.loc[filtro, "FGm"] += 1
                        totales.loc[filtro, "FGa"] += 1
                        totales.loc[filtro, "2Pm"] += 1
                        totales.loc[filtro, "2Pa"] += 1
                        totales.loc[filtro, "Plays"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "2Pa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "Plays"] += 1
                    #QUINTETO
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "2Pa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "3P" and fila.result == "1":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "PTS"] += 3
                        totales.loc[filtro, "FGm"] += 1
                        totales.loc[filtro, "FGa"] += 1
                        totales.loc[filtro, "3Pm"] += 1
                        totales.loc[filtro, "3Pa"] += 1
                        totales.loc[filtro, "Plays"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 3, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "PTS"] += 3
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGm"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "3Pm"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "3Pa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "Plays"] += 1
                    #TOTALES
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PTS"] += 3
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGm"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "3Pm"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "3Pa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "3P" and fila.result == "0":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "PTS"] += 3
                        totales.loc[filtro, "FGm"] += 1
                        totales.loc[filtro, "FGa"] += 1
                        totales.loc[filtro, "3Pm"] += 1
                        totales.loc[filtro, "3Pa"] += 1
                        totales.loc[filtro, "Plays"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "FGa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "3Pa"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "Plays"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "FGa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "3Pa"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "1P" and fila.result == "1":
                    if filtro.any():
                    #JUGADOR
                        totales.loc[filtro, "PTS"] += 1
                        totales.loc[filtro, "1Pm"] += 1
                        totales.loc[filtro, "1Pa"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "PTS"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "1Pm"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == "TOTALES") & (totales["quarter"] == fila.quarter), "1Pa"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PTS"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "1Pm"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "1Pa"] += 1
            if fila.action == "1P" and fila.result == "0":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "1Pa"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "1Pa"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "1Pa"] += 1
            if fila.action == "ASISTENCIA":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "AST"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "AST"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "AST"] += 1
            if fila.action == "PERDIDA":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "PER"] += 1
                        totales.loc[filtro, "Plays"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "PER"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "Plays"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PER"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "RECUPERO":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "REC"] += 1
                    else:
                        # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "REC"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "REC"] += 1
            if fila.action == "REBOTE OFENSIVO":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "RO"] += 1
                        totales.loc[filtro, "RT"] += 1
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "RO"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "RT"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "RO"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "RT"] += 1
            if fila.action == "REBOTE DEFENSIVO":
                    if filtro.any():    
                        #JUGADOR
                        totales.loc[filtro, "RD"] += 1
                        totales.loc[filtro, "RT"] += 1
                    #TOTALES
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "RD"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "RT"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "RD"] += 1
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "RT"] += 1
            if fila.action == "BLOQUEO":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "BLQ"] += 1
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "BLQ"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "BLQ"] += 1
            if fila.action == "FR":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "FR"] += 1
                        totales.loc[filtro, "Plays"] += 1
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "FR"] += 1
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "Plays"] += 1
                    #QUINTETOS
                    lineups.loc[(lineups["id"] == fila.id) & (lineups["Equipo"] == fila.team) & (lineups["Quinteto"].apply(lambda x: sorted(x) == sorted(dict_quint[fila.team]))), "PLAYS"] += 1
            if fila.action == "FP":
                    if filtro.any():
                        #JUGADOR
                        totales.loc[filtro, "FP"] += 1
                    else:
                    # Si la fila no existe, crear una nueva fila e inicializar las métricas en cero
                        nueva_fila = pd.DataFrame([[fila.id, fila.team, fila.opponent, fila.player, fila.quarter, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]],
                                              columns=['id', 'team', 'opponent', 'player', 'quarter', 'PTS', 'FGm', 'FGa', '2Pm', '2Pa', '3Pm', '3Pa', '1Pm', '1Pa', 'AST', 'PER', 'REC', 'RO', 'RD', 'RT', 'BLQ', 'FR', 'FP', 'Plays'])
                        totales = pd.concat([totales, nueva_fila], ignore_index=True)
                    #TOTALES
                    totales.loc[(totales["id"] == fila.id) & (totales["team"] == fila.team) & (totales["opponent"] == fila.opponent) & (totales["player"] == fila.player) & (totales["quarter"] == fila.quarter), "FP"] += 1

    # Imprimir el DataFrame de quintetos actualizado
    print(lineups[lineups["Equipo"] == 'Alemania'])
    # Imprimir el DataFrame de totales actualizado
    print(totales)  
    
    #Calcular las estadísticas totales.loc para cada jugador y equipo
    #for equipo in df.team.unique():
    #    oponente = df[df["oponnent"] == equipo] 
    #    for jugador in df.loc[df["team"] == equipo, "player"].unique():
    #        i += 1
    #        totales.loc[i, 'Equipo'] = equipo
    #        totales.loc[i, 'Jugador'] = jugador
    #        filtro = (df['player'] == jugador) & (df['team'] == equipo)
    #        totales.loc[i, 'PTS'] = (df[filtro & (df['action'] == '2P') & (df['result'] == '1')].shape[0] * 2) + (df[filtro & (df['action'] == '3P') & (df['result'] == '1')].shape[0] * 3) + df[filtro & (df['action'] == '1P') & (df['result'] == '1')].shape[0]
    #        totales.loc[i, 'FGm'] = df[filtro & (df['action'] == '2P') & (df['result'] == '1')].shape[0] + df[filtro & (df['action'] == '3P') & (df['result'] == '1')].shape[0]
    #        totales.loc[i, 'FGa'] = df[filtro & (df['action'] == '2P')].shape[0] + df[filtro & (df['action'] == '3P')].shape[0]
    #        totales.loc[i, '2Pm'] = df[filtro & (df['action'] == '2P') & (df['result'] == '1')].shape[0]
    #        totales.loc[i, '2Pa'] = df[filtro & (df['action'] == '2P')].shape[0]
    #        totales.loc[i, '3Pm'] = df[filtro & (df['action'] == '3P') & (df['result'] == '1')].shape[0]
    #        totales.loc[i, '3Pa'] = df[filtro & (df['action'] == '3P')].shape[0]
    #        totales.loc[i, '1Pm'] = df[filtro & (df['action'] == '1P') & (df['result'] == '1')].shape[0]
    #        totales.loc[i, '1Pa'] = df[filtro & (df['action'] == '1P')].shape[0]
    #        totales.loc[i, 'RO']  = df[filtro & (df['action'] == 'REBOTE OFENSIVO')].shape[0]
    #        totales.loc[i, 'RD']  = df[filtro & (df['action'] == 'REBOTE DEFENSIVO')].shape[0]
    #        totales.loc[i, 'RT']  = df[filtro & (df['action'].isin(['REBOTE OFENSIVO', 'REBOTE DEFENSIVO']))].shape[0]
    #        totales.loc[i, 'AST'] = df[filtro & (df['action'] == 'ASISTENCIA')].shape[0]
    #        totales.loc[i, 'PER'] = df[filtro & (df['action'] == 'PERDIDA')].shape[0]
    #        totales.loc[i, 'REC'] = df[filtro & (df['action'] == 'RECUPERO')].shape[0]
    #        totales.loc[i, 'BLQ'] = df[filtro & (df['action'] == 'BLOQUEO')].shape[0]
    #        if jugador == "Equipo":
    #            totales.loc[i, 'POSS'] = 0
    #            totales.loc[i, 'PLAYS'] = 0
    #        else:
    #            totales.loc[i, 'POSS'] = totales.loc[i, 'FGa'] + totales.loc[i, 'PER'] + 0.44 * totales.loc[i, '1Pa'] - totales.loc[i, 'RO']
    #            totales.loc[i, 'PLAYS'] = totales.loc[i, 'FGa'] + totales.loc[i, 'PER'] + 0.44 * totales.loc[i, '1Pa']


    #    totales_equipo = totales.groupby("Equipo")[['PTS','FGm','FGa','2Pm','2Pa','3Pm','3Pa','1Pm','1Pa','RO','RD','RT','AST','PER','REC','BLQ','POSS', 'PLAYS']].sum().reset_index()
    #    totales_equipo["Jugador"] = "TOTALES"

    ## Combina los resultados con el DataFrame original
    #totales = pd.merge(totales, partidos_jugador, on=['Equipo', 'Jugador'], how='left')
    #totales.loc[totales["Jugador"] == "Equipo", "PJ"] = totales.loc[totales["Jugador"] == "Equipo", "Equipo"].map(partidos_equipo.set_index("Equipo")["PJ"])
    #totales_equipo = pd.merge(totales_equipo, partidos_equipo, on='Equipo', how='left')
    
    #totales = pd.concat([totales, totales_equipo], ignore_index=True)

    # Calcular las medias por partido para las columnas de estadísticas
    #columnas_estadisticas = ["PTS", "FGm", "FGa", "2Pm", "2Pa", "3Pm", "3Pa", "1Pm", "1Pa", "RO", "RD", "RT", "AST", "PER", "REC", "BLQ", "POSS", "PLAYS"]
    #medias = totales.copy()
    #
    #for columna in columnas_estadisticas:
    #    medias[columna] = round(medias[columna] / medias["PJ"], 2)
    #
    ## Asegurarse de que la columna "PJ" sea de tipo entero (opcional)
    #medias["PJ"] = medias["PJ"].astype(int)
    
    #return totales, medias