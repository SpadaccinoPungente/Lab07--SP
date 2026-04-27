import flet as ft

from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # View, model.
        self._view = view
        self._model = model

        # Other attributes.
        self._mese = 0

    def handle_umidita_media(self, e):
        # Control on self._mese.
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese dal menù a tendina.")
            return

        # Get the requested result from the model.
        umidita = self._model.get_umidita_media(self._mese)

        # Clear the listview.
        self._view.lst_result.controls.clear()

        # Display the results.
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato è:"))

        for loc, umi in umidita.items():
            self._view.lst_result.controls.append(ft.Text(f"{loc}: {umi:.4f}"))

        self._view.update_page()

    def handle_sequenza(self, e):
        # Control on self._mese.
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese dal menù a tendina.")
            return

        # Clear the listview.
        self._view.lst_result.controls.clear()

        # Get the requested result from the model.
        sequenza, costo = self._model.calcola_sequenza(self._mese)

        # Clear the listview.
        self._view.lst_result.controls.clear()

        # Display the results.
        if not sequenza:
            self._view.lst_result.controls.append(ft.Text("Nessuna sequenza valida trovata per i vincoli imposti."))
        else:
            self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
            for s in sequenza:
                self._view.lst_result.controls.append(
                    ft.Text(f"[{s.Localita} - {s.Data}] Umidità = {s.Umidita}"))

        self._view.update_page()

    def read_mese(self, e):
        # The key of the ft.dropdown.Option object.
        self._mese = int(e.control.value)

