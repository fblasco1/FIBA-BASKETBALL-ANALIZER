import pandas as pd
import stats_advanced as sa

def calculate_stats_advanced(df):
    result = df.groupby(["Equipo"]).sum()

    equipos_prueba = result.index

    data_eight_factors = {
        "Equipo": equipos_prueba,
        "Possesions": [sa.possesions(result.loc[equipo, "TCi"],result.loc[equipo, "TO"], result.loc[equipo, "TLi"], result.loc[equipo, "REBO"]) for equipo in equipos_prueba],
        "Plays": [sa.plays(result.loc[equipo, "TCi"],result.loc[equipo, "TO"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
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