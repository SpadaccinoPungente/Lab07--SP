import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._mese_selezionato = 0

    def handle_umidita_media(self, e):
        if self._mese_selezionato == 0:
            self._view.create_alert("Selezionare un mese!")
            return
        self._view.lst_result.controls.clear()
        umidita_medie, _ = self._model.getUmiditaMedie(self._mese_selezionato)
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for row in umidita_medie:
            self._view.lst_result.controls.append(ft.Text(f"{row['Localita']}: {row['Umidita_media']}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        pass

    def read_mese(self, e):
        self._mese_selezionato = int(e.control.value)

