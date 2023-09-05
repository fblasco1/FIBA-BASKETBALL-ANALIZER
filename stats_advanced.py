def convertir_minutos(self):
    """
    Convierte MM:SS EN Minutos
    """
    try:
        return int(self.minutos.split(":")[0]) + int(self.minutos.split(":")[1]) / 60
    except ValueError:
        return int(self.minutos.split(".")[0]) + int(self.minutos.split(".")[1]) / 60
    
    
def plays(tci, per, tli):
    """
    Estima el numero de jugadas que un equipo tiene durante un partido/temporada.
    """
    return round(tci + per + 0.44 * tli, 2)
    

def possesions(tci, per, tli, rebo):
    """
    Estima el numero de posesiones que un equipo tiene durante un partido/temporada.
    """
    return round(tci + per + 0.44 * tli - rebo, 2)
    

def pts_plays(pts, tci, per, tli):
    """
    Mide los puntos de un equipo o jugador por jugada.
    """
    _plays = plays(tci, per, tli)
    if _plays == 0:
        return 0
    else:
        return round(pts / _plays, 2)


def pts_poss(pts, tci, per, tli, rebo):
    """
    Mide los puntos de un equipo o jugador por posesiones.
    """
    _possesions = possesions(tci, per, tli, rebo)
    if _possesions == 0:
        return 0
    else:
        return round(pts/_possesions)


def oer_plays(pts, tci, per, tli):
    """
    Ajusta la anotación de un equipo a 100 jugadas.
    """
    _pts_plays = pts_plays(pts, tci, per, tli)
    if _pts_plays == 0:
        return 0
    else:
        return round(_pts_plays*100,2)


def der_plays(pts_opp, tci_opp, per_opp, tli_opp):
    """
    Ajusta la defensa de un equipo a 100 jugadas.
    """
    _plays_opp = plays(tci_opp, per_opp, tli_opp)
    if _plays_opp == 0:
        return 0
    else:
        return round(100 * (pts_opp / _plays_opp), 2)

def oer_poss(pts, tci, per, tli,rebo):
    """
    Ajusta la anotación de un equipo a 100 posesiones.
    """
    _possesions = possesions(tci, per, tli,rebo)
    if _possesions == 0:
        return 0
    else:
        return round(100 * (pts / _possesions), 2)

def der_poss(pts_opp, tci_opp, per_opp, tli_opp,rebo_opp):
    """
    Ajusta la defensa de un equipo a 100 posesiones.
    """
    _possesions = possesions(tci_opp, per_opp, tli_opp,rebo_opp)
    if _possesions == 0:
        return 0
    else:
        return round((pts_opp/_possesions)*100, 2)
    

def eFG(tci, tcc, t3c):
    """
    Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5
    respecto del estandar de porcentaje de tiro de campo.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * ((tcc + 0.5 * t3c) / tci), 2)

def true_shooting(pts, tci, tli):
    """
    Ajusta el porcentaje de tiro de campo de un equipo o jugador incluyendo el tiro libre.
    Abarca todas las vías de anotación.
    """
    if tci == 0 and tli == 0:
        return 0
    else:
        return round((pts/(2* (tci + 0.44 * tli)))*100, 2)
    

def ORB(rebo, rebd_opp):
    """
    Mide el porcentaje de rebotes ofensivos de un equipo sobre los disponibles.
    """
    if rebo == 0 and rebd_opp == 0:
        return 0
    else:
        return round(100 * (rebo / (rebo + rebd_opp)), 2)

def DRB(rebd, rebo_opp):
    """
    Mide el porcentaje de rebotes defensivos de un equipo sobre los disponibles.
    """
    if rebo_opp == 0 and rebd == 0:
        return 0
    else: 
        return round(100 * (rebd / (rebd + rebo_opp)), 2)


def ast_poss(ast, tci, per, tli, rebo):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de posesiones.
    """
    _possesions = possesions(tci, per, tli, rebo)
    if _possesions == 0:
        return 0
    else:
        return round(100 * (ast/_possesions), 2)


def ast_plays(ast, tci, per, tli):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de jugadas.
    Hollinger Asist Ratio.
    """
    _plays = _plays(tci, per, tli)
    if _plays == 0:
        return 0
    else:
        return round(100 * (ast / _plays),2)


def asist_per_ratio(ast, per):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de pérdidas.
    """
    if per == 0:
        return 0
    else:
       return round(ast/per, 2)
    

def tc_assisted(ast, tcc):
    """
    Mide el porcentaje de tiros de campo asistidos por un equipo
    """
    if ast == 0:
        return 0
    else:
        return round(100 * (ast / tcc), 2)
    
def rec_poss(rec, tci_opp, per_opp, tli_opp,rebo_opp):
    """
    Ajusta la cantidad de recuperos de un equipo o jugador cada 100 posesiones del rival.
    """
    _possesions = possesions(tci_opp, per_opp, tli_opp,rebo_opp)
    if _possesions == 0:
        return 0
    else:
        return round((rec/_possesions)*100, 2)


def rec_plays(rec, tci_opp, per_opp, tli_opp):
    """
    Ajusta la cantidad de recuperos de un equipo o jugador cada 100 plays del rival.
    """
    _plays = plays(tci_opp, per_opp, tli_opp)
    if _possesions == 0:
        return 0
    else:
        return round((rec/_plays)*100, 2)


def per_poss(per, tci_opp, per_opp, tli_opp,rebo_opp):
    """
    Ajusta la cantidad de perdidas de un equipo o jugador cada 100 posesiones.
    """
    _possesions = possesions(tci_opp, per_opp, tli_opp,rebo_opp)
    if _possesions == 0:
        return 0
    else:
        return round((per/_possesions)*100, 2)


def per_plays(per, tci_opp, per_opp, tli_opp):
    """
    Ajusta la cantidad de perdidas de un equipo o jugador cada 100 plays.
    """
    _plays = plays(tci_opp, per_opp, tli_opp)
    if _possesions == 0:
        return 0
    else:
        return round((per/_plays)*100, 2)
 
    
def tapones_ratio(tap, _2Pi_opp):
    """
    Ajusta la cantidad de tapones de un equipo o jugador según la cantidad de tiros de 2 intentados del rival.
    """
    if _2Pi_opp == 0:
        return 0
    else:
        return round(100 * (tap / _2Pi), 2)


def ratio_tl(tci, tlc):
    """
    Mide la asiduidad con la que un jugador o equipo va a la linea de libres.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * (tlc / tci), 2) 
    

def ratio_2p(_2Pc, tci):
    """
    Mide la asiduidad con la que un jugador o equipo tira de 2.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * (_2Pc / tci), 2)


def ratio_3p(_3Pc, tci):
    """
    Mide la asiduidad con la que un jugador o equipo tira de 3.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * (_3Pc / tci), 2)


def pps_tl(tlc, tli):
    """
    Mide los puntos por tiro de libre de un jugador o equipo.
    """
    if tli == 0:
        return 0
    else:
        return round(tlc / tli, 2)


def pps_2p(_2Pi, _2Pc):
    """
    Mide los puntos por tiro de 2 de un jugador o equipo.
    """
    if _2Pi == 0:
        return 0
    else:
       return round(_2Pc * 2 / _2Pi, 2)
    

def pps_3p(_3Pi, _3Pc):
    """
    Mide los puntos por tiro de 3 de un jugador o equipo.
    """
    if _3Pi == 0:
        return 0
    else:
        return round(_3Pc * 3 / _3Pi, 2)
    

def pts_ro(self):
    """
    Mide los puntos por rebote ofensivo de un jugador o equipo.
    """
    if self.reboff == 0:
        self.ppORB = 0
    else:
        self.ppORB = self.secondchance / self.reboff
    return round(self.ppORB, 2)


def USG(self, tcijugador, tlijugador, perjugador, minjugador, tciequipo, tliequipo, perequipo, mintotales):
    minutesjug = self.convertir_minutos(minjugador)
    minutesequipo = self.convertir_minutos(mintotales)
    if self.fplays() == 0:
        self.usg = 0
    else:
        self.usg = (((tcijugador + 0.44 * tlijugador + perjugador) * (minutesequipo/5))/((tciequipo + 0.44 * tliequipo + perequipo) * (minutesjug))) * 100
    
    return round(self.usg, 2)