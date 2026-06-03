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

    @staticmethod
    def getSituazioni15gg(int_mese_selezionato):
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione fallita")
            return [], False

        cursor = cnx.cursor(dictionary=True)
        query = """
                select s.Localita, s.Data, s.Umidita 
                from situazione s
                where month(s.Data) = %s and day(s.data) <= 15
                order by s.data asc
                """
        cursor.execute(query, (int_mese_selezionato,))

        result = []
        for row in cursor: result.append(Situazione(row['Localita'], row['Data'], row['Umidita']))
        cursor.close()
        cnx.close()
        return result, True


