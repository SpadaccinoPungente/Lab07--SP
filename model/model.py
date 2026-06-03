import copy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._sequenza_ottima = []
        self._costo_minimo = float('inf')
        self._situazioni15gg = []

    def getUmiditaMedie(self, int_mese_selezionato):
        return MeteoDao.getUmiditaMedie(int_mese_selezionato)

    """
    Sapendo che nel database sono presenti 3 città (Milano, Torino, Genova), supponiamo che un tecnico 
    debba fare delle analisi della durata di un giorno in ciascuna città.
    Le analisi hanno un costo per ogni giornata, determinato dalla somma di due contributi: 
    - un fattore costante (di valore 100) quando il tecnico si deve spostare di città in due giorni successivi
    - un fattore variabile pari al valore numerico dell’umidità della città nel giorno considerato. 

    Si trovi la sequenza delle città da visitare nei primi 15 giorni del mese selezionato, tale da minimizzare il 
    costo complessivo rispettando i seguenti vincoli:
    - In nessuna città si possono trascorrere più di 6 giornate (anche non consecutive) 
    - Scelta una città, il tecnico non si può spostare prima di aver trascorso 3 giorni consecutivi. 
    """

    # WRAPPER PUBBLICO
    def getSequenzaOttima(self, int_mese_selezionato):
        self._sequenza_ottima = []  # sarà una lista di situazioni
        self._costo_minimo = float('inf')
        self._situazioni15gg, _ = MeteoDao.getSituazioni15gg(int_mese_selezionato)

        self._ricorsione([], 0)
        return self._sequenza_ottima, self._costo_minimo

    # METODO RICORSIVO
    def _ricorsione(self, parziale, giornata_corrente):
        costo_attuale = self.getCosto(parziale)

        if costo_attuale >= self._costo_minimo: return  # branch and bound

        if len(parziale) == 15:
            self._costo_minimo = costo_attuale
            self._sequenza_ottima = copy.deepcopy(parziale)
            return

        situazioni_candidate = [s for s in self._situazioni15gg if s.data.day == giornata_corrente + 1]

        for s in situazioni_candidate:
            if self.isValida(parziale, s):
                parziale.append(s)
                self._ricorsione(parziale, giornata_corrente + 1)
                parziale.pop()

    # METODI HELPER
    def isValida(self, parziale, situazione_candidata):
        giorni_totali_citta = sum(1 for s in parziale if s.localita == situazione_candidata.localita)
        if giorni_totali_citta >= 6: return False

        if len(parziale) > 0 and situazione_candidata.localita != parziale[-1].localita:
            if len(parziale) < 3: return False
            # Controlla se i tre giorni precedenti appartengono alla stessa città che stiamo lasciando
            if parziale[-2].localita != parziale[-1].localita or parziale[-3].localita != parziale[-1].localita: return False

        return True

    def getCosto(self, parziale):
        costo = 0
        for i, curr in enumerate(parziale):
            if i > 0 and curr.localita != parziale[i - 1].localita:
                costo += 100
            costo += curr.umidita
        return costo

"""
# VERSIONE PIU' OTTIMIZZATA CON CALCOLO DEL COSTO ON-THE-GO PER NON RIFARLO A OGNI ITERAZIONE

# WRAPPER PUBBLICO
def getSequenzaOttima(self, int_mese_selezionato):
    self._sequenza_ottima = []
    self._costo_minimo = float('inf')
    self._situazioni15gg, _ = MeteoDao.getSituazioni15gg(int_mese_selezionato)

    # Passiamo 0 come costo iniziale alla ricorsione
    self._ricorsione([], 0, 0)
    return self._sequenza_ottima, self._costo_minimo

# METODO RICORSIVO
def _ricorsione(self, parziale, giornata_corrente, costo_attuale):

    # Branch and bound immediato ed efficiente (O(1))
    if costo_attuale >= self._costo_minimo: 
        return

    if len(parziale) == 15:
        self._costo_minimo = costo_attuale
        self._sequenza_ottima = copy.deepcopy(parziale)
        return

    situazioni_candidate = [s for s in self._situazioni15gg if s.data.day == giornata_corrente + 1]

    for s in situazioni_candidate:
        if self.isValida(parziale, s):
            # Calcoliamo l'incremento di costo per questo specifico passo
            incremento = s.umidita
            if len(parziale) > 0 and s.localita != parziale[-1].localita:
                incremento += 100
            
            parziale.append(s)
            # Passiamo il costo aggiornato al livello successivo
            self._ricorsione(parziale, giornata_corrente + 1, costo_attuale + incremento)
            parziale.pop()

# METODI HELPER
def isValida(self, parziale, situazione_candidata):
    # Vincolo 1: Max 6 giornate totali per città
    giorni_totali_citta = sum(1 for s in parziale if s.localita == situazione_candidata.localita)
    if giorni_totali_citta >= 6: 
        return False

    # Vincolo 2: Minimo 3 giorni consecutivi prima di spostarsi
    if len(parziale) > 0 and situazione_candidata.localita != parziale[-1].localita:
        if len(parziale) < 3: 
            return False
        # Se i tre giorni precedenti non sono la stessa città, non posso cambiare
        if parziale[-2].localita != parziale[-1].localita or parziale[-3].localita != parziale[-1].localita:
            return False

    return True
"""