from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao:

    @staticmethod
    def getUmiditaMedie(int_mese_selezionato):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
            return [], False
        cursor = cnx.cursor(dictionary=True)
        query = """
                select s.Localita, avg(s.Umidita) as Umidita_media
                from situazione s
                where month(s.data) = %s
                group by s.Localita
                """
        cursor.execute(query, (int_mese_selezionato,))
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result, True


