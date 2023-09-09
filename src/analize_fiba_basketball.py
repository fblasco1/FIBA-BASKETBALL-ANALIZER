import pandas as pd
import src.stats_advanced as sa

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
    shots_result_1 = shot_df[shot_df['result'] == 1]

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