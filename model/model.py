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
        # Condizione terminale
        # if:
        # Ricorsione
        # else:
        pass

