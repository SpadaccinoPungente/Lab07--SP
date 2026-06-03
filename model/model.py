from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def getUmiditaMedie(self, int_mese_selezionato):
        return MeteoDao.getUmiditaMedie(int_mese_selezionato)
