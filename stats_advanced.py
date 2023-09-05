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
    

def fpace(self, possesionop):
    """
    Estima el ritmo de juego que se desarrolla a lo largo de un partido.
    """
    if type(self.minutos) == str: 
        if self.convertir_minutos() == 0:
            self.pace = 0
        else:
            self.pace = 40 * (self.possesions() + possesionop) / (2 * (self.convertir_minutos() / 5))
    else:
        if self.minutos == 0:
            self.pace = 0
        else:
            self.pace = 40 * (self.possesions() + possesionop) / (2 * (self.minutos / 5))
    return round(self.pace, 2)

def pts_plays(self):
    """
    Mide los puntos de un equipo o jugador por jugada.
    """
    if self.plays == 0:
        self.ptsplays = 0
    else:
        self.ptsplays = self.puntos/self.fplays()
    return round(self.ptsplays, 2)

def pts_poss(self):
    """
    Mide los puntos de un equipo o jugador por posesiones.
    """
    if self.possesions() == 0:
        self.ptsposs = 0
    else:
        self.ptsposs = self.puntos/self.possesions()
    return round(self.ptsposs, 2)

def off_rtg_plays(self):
    """
    Ajusta la anotación de un equipo a 100 jugadas.
    """
    if self.plays == 0:
        self.effOffPlays = 0
    else:
        self.effOffPlays = (self.puntos/self.fplays())*100
    return round(self.effOffPlays, 2)

def def_rtg_plays(self, playsop):
    """
    Ajusta la defensa de un equipo a 100 jugadas.
    """
    if self.plays == 0:
        self.effDefPlays = 0
    else:
        self.effDefPlays = (self.puntos/playsop)*100
    return round(self.effDefPlays, 2)

def off_rtg_poss(self):
    """
    Ajusta la anotación de un equipo a 100 posesiones.
    """
    if self.possesions() == 0:
        self.effOff = 0
    else:
        self.effOff = (self.puntos/self.possesions())*100
    return round(self.effOff, 2)

def def_rtg_poss(self, possesionop):
    """
    Ajusta la defensa de un equipo a 100 posesiones.
    """
    if possesionop == 0:
        self.efDef = 0
    else:
        self.efDef = (self.puntos/possesionop)*100
    return round(self.efDEF, 2)

def eFG(tci, tcc, t3c):
    """
    Ajusta el porcentaje de tiro de campo de un equipo o jugador corrigiendo el valor del tiro de 3 en 1.5
    respecto del estandar de porcentaje de tiro de campo.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * ((tcc + 0.5 * t3c) / tci), 2)

def true_shooting(self):
    """
    Ajusta el porcentaje de tiro de campo de un equipo o jugador incluyendo el tiro libre.
    Abarca todas las vías de anotación.
    """
    if self.tiroscampointentados == 0 and self.tiroslibresintentados == 0:
        self.ts = 0
    else:
        self.ts = (self.puntos/(2* (self.tiroscampointentados + 0.44 * self.tiroslibresintentados)))*100
    return round(self.ts, 2)

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

def asist_poss(self):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de posesiones.
    """
    if self.possesions() == 0:
        self.tAS = 0
    else:
        self.tAS = self.asistencias * 100 / self.possesions()
    return round(self.tAS, 2)

def asist_plays(self):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de jugadas.
    Hollinger Asist Ratio.
    """
    if self.fplays() == 0:
        self.tASPlays = 0
    else:
        self.tASPlays = self.asistencias * 100 / self.fplays()
    return round(self.tASPlays, 2)

def asist_per_ratio(self):
    """
    Ajusta la cantidad de asistencias de un jugador o equipo segun la cantidad de pérdidas.
    """
    if self.perdidas == 0:
        self.tASPER = 0
    else:
        self.tASPER = self.asistencias / self.perdidas
    return round(self.tASPER, 2)

def porc_asist(self):
    """
    Mide el porcentaje de tiros de campo asistidos por un equipo
    """
    if self.asistencias == 0:
        self.tTCAS = 0
    else:
        self.tTCAS = self.asistencias * 100 / self.tiroscampoconvertidos
    return round(self.tTCAS, 2)

def recuperos_poss(self, possesionop):
    """
    Ajusta la cantidad de recuperos de un equipo o jugador cada 100 posesiones del rival.
    """
    if possesionop == 0:
        self.tREC = 0
    else:
        self.tREC = self.recuperos * 100 / possesionop
    return round(self.tREC, 2)

def recuperos_plays(self, playsop):
    """
    Ajusta la cantidad de recuperos de un equipo o jugador cada 100 plays del rival.
    """
    if playsop == 0:
        self.tRECPlays = 0
    else:
        self.tRECPlays = self.recuperos * 100 / playsop
    return round(self.tRECPlays, 2)

def perdidas_poss(self):
    """
    Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 posesiones.
    """
    if self.possesions() == 0:
        self.tPER = 0
    else:
        self.tPER = self.perdidas * 100 / self.possesions()
    return round(self.tPER, 2)

def perdidas_plays(tci, per, tli):
    """
    Ajusta la cantidad de pérdidas de un equipo o jugador cada 100 plays.
    """
    _plays = plays(tci, per, tli)
    if  _plays == 0:
        return 0
    else:
        return round(100 * (per / _plays), 2)
 
    
def tapones_ratio(self, doblesintentadosop):
    """
    Ajusta la cantidad de tapones de un equipo o jugador según la cantidad de tiros de 2 intentados del rival.
    """
    if doblesintentadosop == 0:
        self.tTAP = 0
    else:
        self.tTAP = 100 * (self.tapones / doblesintentadosop)
    return round(self.tTAP, 2)

def ratio_tl(tci, tli):
    """
    Mide la asiduidad con la que un jugador o equipo va a la linea de libres.
    """
    if tci == 0:
        return 0
    else:
        return round(100 * (tli / tci), 2) 
    

def ratio_2p(self):
    """
    Mide la asiduidad con la que un jugador o equipo tira de 2.
    """
    if self.tiroscampointentados == 0:
        self.ratio2p = 0
    else:
        self.ratio2p = 100 * (self.doblesconvertidos / self.tiroscampointentados)
    return round(self.ratio2p, 2)

def ratio_3p(self):
    """
    Mide la asiduidad con la que un jugador o equipo tira de 3.
    """
    if self.tiroscampointentados == 0:
        self.ratio3p = 0
    else:
        self.ratio3p = 100 * (self.triplesconvertidos / self.tiroscampointentados)
    return round(self.ratio3p, 2)

def pps_tl(self):
    """
    Mide los puntos por tiro de libre de un jugador o equipo.
    """
    if self.tiroslibresintentados == 0:
        self.ppsTL = 0
    else:
        self.ppsTL = self.tiroslibresconvertidos / self.tiroslibresintentados
    return round(self.ppsTL, 2)

def pps_2p(self):
    """
    Mide los puntos por tiro de 2 de un jugador o equipo.
    """
    if self.doblesintentados == 0:
        self.pps2P = 0
    else:
        self.pps2P = (self.doblesconvertidos * 2 / self.doblesintentados)
    return round(self.pps2P, 2)

def pps_3p(self):
    """
    Mide los puntos por tiro de 3 de un jugador o equipo.
    """
    if self.triplesintentados == 0:
        self.pps3P = 0
    else:
        self.pps3P = (self.triplesconvertidos * 3 / self.triplesintentados)
    return round(self.pps3P, 2)

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