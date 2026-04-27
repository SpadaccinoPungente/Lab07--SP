import flet as ft


class View(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()

        # Page initialization.
        self._page = page
        self._page.title = "Laboratorio 07 - Ricorsione"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        # Controller (created and initialized in main.py))
        self._controller = None

        # Definition of graphical elements.
        self._title = None
        self.dd_mese: ft.Dropdown = None
        self.btn_umidita: ft.ElevatedButton = None
        self.btn_calcola_sequenza: ft.ElevatedButton = None
        self.lst_result: ft.ListView = None

    def load_interface(self):
        # Page title.
        self._title = ft.Text(value="Analisi meteo", color="blue", size=24)
        self._page.controls.append(self._title)

        # Row elements: dd_mese, btn_umidita, btn_calcola_sequenza.
        self.dd_mese = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="1", text="Gennaio"),
                ft.dropdown.Option(key="2", text="Febbraio"),
                ft.dropdown.Option(key="3", text="Marzo"),
                ft.dropdown.Option(key="4", text="Aprile"),
                ft.dropdown.Option(key="5", text="Maggio"),
                ft.dropdown.Option(key="6", text="Giugno"),
                ft.dropdown.Option(key="7", text="Luglio"),
                ft.dropdown.Option(key="8", text="Agosto"),
                ft.dropdown.Option(key="9", text="Settembre"),
                ft.dropdown.Option(key="10", text="Ottobre"),
                ft.dropdown.Option(key="11", text="Novembre"),
                ft.dropdown.Option(key="12", text="Dicembre"),],
            label="Mese",
            width=200,
            hint_text="Selezionare un mese",
            on_change=self._controller.read_mese)

        self.btn_umidita = ft.ElevatedButton(
            text="Umidità media",
            tooltip="Verifica l'umidità media per città, nel mese selezionato",
            on_click=self._controller.handle_umidita_media)

        self.btn_calcola_sequenza = ft.ElevatedButton(
            text="Calcola sequenza",
            tooltip="Calcola la sequenza ottimale per le analisi",
            on_click=self._controller.handle_sequenza)

        # Creation of row1.
        row1 = ft.Row(controls=[
            self.dd_mese,
            self.btn_umidita,
            self.btn_calcola_sequenza],
            alignment=ft.MainAxisAlignment.CENTER)

        # List View where the reply is printed.
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        self._page.controls.extend([row1, self.lst_result])
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        self._page.dialog = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
