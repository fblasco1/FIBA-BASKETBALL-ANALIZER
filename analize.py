import pandas as pd
from stats_advanced import eFG, perdidas_plays, ORB, ratio_tl, DRB

def calculate_eight_factors(df: pd.Dataframe(), cols: list, col_team):
    result = df.loc[:, cols]

    for col in cols:
        result[col] = result[col].astype(float)

    result = result.groupby(col_team).sum()

    equipos_prueba = result.index

    data_eight_factors = {
        "Equipo": equipos_prueba,
        "eFG%": [eFG(result.loc[equipo, "TCi"], result.loc[equipo, "TCc"], result.loc[equipo, "3Pc"]) for equipo in equipos_prueba],
        "%TO": [perdidas_plays(result.loc[equipo, "TCi"], result.loc[equipo, "TO"], result.loc[equipo, "TLi"]) for equipo in equipos_prueba],
        "%ORB": [ORB(result.loc[equipo, "REBO"], result.loc[equipo, "RD_OPP"]) for equipo in equipos_prueba],
        "%FT": [ratio_tl(result.loc[equipo, "TCi"], result.loc[equipo, "TLc"]) for equipo in equipos_prueba],
        "OPP_eFG%":  [eFG(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TCc_OPP"], result.loc[equipo, "3Pc_OPP"]) for equipo in equipos_prueba],
        "OPP_%TO": [perdidas_plays(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TO_OPP"], result.loc[equipo, "TLi_OPP"]) for equipo in equipos_prueba],
        "%DRB": [DRB(result.loc[equipo, "REBD"], result.loc[equipo, "RO_OPP"]) for equipo in equipos_prueba],
        "OPP_%FT": [ratio_tl(result.loc[equipo, "TCi_OPP"], result.loc[equipo, "TLc_OPP"]) for equipo in equipos_prueba],
    }

    return pd.DataFrame(data_eight_factors)