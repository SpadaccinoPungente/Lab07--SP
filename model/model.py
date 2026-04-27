import copy

from database.meteo_dao import MeteoDao


class Model:

    def __init__(self):
        # Carico tutti i dati una sola volta all'avvio
        self._situazioni = MeteoDao.get_all_situazioni()

        # Variabili di stato per la ricorsione
        self._best_sol = []
        self._best_costo = float('inf')

    def get_umidita_media(self, mese):
        sum_umi = {}
        cnt_gg = {}
        medie = {}

        for s in self._situazioni:
            if s.Data.month == mese:
                if s.Localita not in sum_umi:
                    sum_umi[s.Localita] = 0
                    cnt_gg[s.Localita] = 0

                sum_umi[s.Localita] += s.Umidita
                cnt_gg[s.Localita] += 1


        for loc in sum_umi: medie[loc] = sum_umi[loc] / cnt_gg[loc]

        return medie

    """
    2. Risolvere il seguente problema di ottimizzazione mediante un algoritmo ricorsivo:
    
    Sapendo che nel database sono presenti 3 città (Milano, Torino, Genova), supponiamo che un tecnico 
    debba compiere delle analisi tecniche della DURATA DI 1 GIORNO in ciascuna città. 
    
    Le analisi hanno un costo per ogni giornata, determinato dalla somma di DUE CONTRIBUTI: 
    - un FATTORE COSTANTE DI 100 ogniqualvolta il tecnico si deve spostare da una città ad un’altra IN DUE GIORNI SUCCESSIVI, 
    - un fattore variabile pari al valore numerico dell’umidità della città nel giorno considerato. 
    
    Si trovi la sequenza delle città da visitare NEI PRIMI 15 GIORNI DEL MESE selezionato, 
    tale da minimizzare il costo complessivo rispettando i seguenti vincoli:
    - In nessuna città si possono trascorrere più di 6 giornate (anche non consecutive) 
    - Scelta una città, il tecnico non si può spostare prima di aver trascorso 3 giorni consecutivi. 
    """

    def calcola_sequenza(self, mese):
        self._best_sol = []
        self._best_costo = float('inf')
        self.ricorsione([], self.filtra_situazioni_15gg(self._situazioni, mese), 0)
        # situazioni già ordinate
        return self._best_sol, self._best_costo

    # @lru_cache
    def ricorsione(self, parziale, situazioni, costo):

        # BRANCH AND BOUND: Taglio i rami morti
        if costo >= self._best_costo: return

        if len(parziale)==15:
            if costo < self._best_costo:
                self._best_sol = copy.deepcopy(parziale)
                self._best_costo = costo
        else:
            for situazione in situazioni[3*len(parziale):3*len(parziale)+3]:
                # Funziona ma in generale pericoloso. Il modo corretto sarebbe ciclare sulle città filtrando per
                # il giorno esatto: giorno_corrente = len(parziale) + 1, e cercare nella lista situazioni
                # solo gli elementi con Data.day == giorno_corrente.

                parziale.append(situazione)

                # La città inserita non deve superare i 6 giorni totali.
                if self.check_max_6gg(parziale):

                    # Sto cambiando città?
                    if len(parziale) > 1 and parziale[-2].Localita != situazione.Localita:
                        # Sì -> controllo dei 3 giorni minimi.
                        if self.check_min_3gg(parziale):
                            nuovo_costo = costo + 100 + situazione.Umidita
                            self.ricorsione(parziale, situazioni, nuovo_costo)
                    else:
                        # No (o è il primo giorno).
                        nuovo_costo = costo + situazione.Umidita
                        self.ricorsione(parziale, situazioni, nuovo_costo)

                parziale.pop()

    @staticmethod
    def filtra_situazioni_15gg(situazioni, mese):
        situazioni_15gg_mese = []
        for situazione in situazioni:
            if situazione.Data.month == mese and situazione.Data.day <= 15:
                situazioni_15gg_mese.append(situazione)
        return situazioni_15gg_mese

    @staticmethod
    def check_max_6gg(parziale):
        conteggio = sum(1 for s in parziale if s.Localita == parziale[-1].Localita)
        return conteggio <= 6

    @staticmethod
    def check_min_3gg(parziale):
        if len(parziale) <= 3: return False
        return parziale[-3].Localita == parziale[-2].Localita and parziale[-4].Localita == parziale[-2].Localita

    # Corretto ma inutilmente complicato:
    # @staticmethod
    # def check_min_3gg(parziale):
    #     cnt_cons_gg = 0
    #     for i in range(len(parziale)-2, -1, -1):
    #         if parziale[i].Localita == parziale[-2].Localita:
    #             cnt_cons_gg += 1
    #         else: return cnt_cons_gg >= 3
    #     return cnt_cons_gg >= 3 # All'uscita, deve verificare di aver raggiunto i 3 giorni
