from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:

    @staticmethod
    def get_all_situazioni() -> list[Situazione]:
        """Restituisce una lista di tutte le situazioni meteorologiche presenti a database."""

        result = []
        cnx = DBConnect.get_connection()

        if cnx is not None:
            query = """SELECT Localita, Data, Umidita
                       FROM situazione 
                       ORDER BY Data ASC"""

            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query)

            # row è un dict: {"Localita": "...", "Data": ..., "Umidita": ...}
            # **row lo scompatta in parametri nominati corrispondenti agli attributi della dataclass
            for row in cursor: result.append(Situazione(**row))

            cursor.close()
            cnx.close()
        else: print("Connessione fallita")
        return result

    @staticmethod
    def get_umidita_media(mese: int) -> dict:
        """Restituisce un dizionario {Localita: Umidita_media} per il mese indicato."""

        result = {}
        cnx = DBConnect.get_connection()

        if cnx is not None:
            query = """SELECT Localita, AVG(Umidita) as Media
                       FROM situazione
                       WHERE MONTH (Data) = %s
                       GROUP BY Localita"""

            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query, (mese,))

            for row in cursor: result[row["Localita"]] = row["Media"]

            cursor.close()
            cnx.close()
        else: print("Connessione fallita")
        return result

    @staticmethod
    def get_situazioni_prime_meta(mese: int) -> list[Situazione]:
        """Restituisce una lista delle situazioni meteorologiche dei primi 15 giorni del mese."""

        result = []
        cnx = DBConnect.get_connection()

        if cnx is not None:
            query = """SELECT Localita, Data, Umidita
                       FROM situazione
                       WHERE MONTH (Data) = %s AND DAY (Data) <= 15
                       ORDER BY Data ASC"""

            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query, (mese,))

            # row è un dict: {"Localita": "...", "Data": ..., "Umidita": ...}
            # **row lo scompatta in parametri nominati corrispondenti agli attributi della dataclass
            for row in cursor: result.append(Situazione(**row))

            cursor.close()
            cnx.close()
        else: print("Connessione fallita")
        return result



