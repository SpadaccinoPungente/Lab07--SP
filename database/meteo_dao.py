from database.DB_connect import DBConnect
from model.situazione import Situazione

# Questions for future labs:
# 1) Should I create a DAO class or just use normal functions inside the DAO module?
# 2) What is the correct way of implementing the identity map pattern?


class MeteoDao:

    @staticmethod
    def get_all_situazioni() -> list[Situazione]:
        """Restituisce una lista di tutte le situazioni meteorologiche presenti a database."""

        query = """SELECT Localita, Data, Umidita
                   FROM situazione
                   ORDER BY Data ASC"""
        cnx = DBConnect.get_connection()
        result = []

        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            cursor.execute(query)

            # row è un dict: {"Localita": "...", "Data": ..., "Umidita": ...}
            # **row lo scompatta in parametri nominati corrispondenti agli attributi della dataclass
            for row in cursor: result.append(Situazione(**row))

            cursor.close()
            cnx.close()
        else: print("Connessione fallita")
        return result



