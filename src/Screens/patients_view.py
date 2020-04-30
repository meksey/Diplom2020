from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar



class PatientView(Screen):
    app_instance = None
    patients = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = MDApp.get_running_app()

    def on_enter(self, *args):
        self.load_grid()

    def load_grid(self):
        patients = self.app_instance.db.get_patients_info()

        if not patients:
            Snackbar(text='У вас нет ни одного пациента').show()
            return

        for key, value in patients.items():
            fio = '{} {} {}'.format(value.get('surname', ''), value.get('name', ''), value.get('patronymic', ''))
            card = PatientCard(fio=fio)
            self.ids.grid.add_widget(card)

    # Добавить пациента
    def add_patient(self, patient_id):
        if not patient_id:
            Snackbar(text='Введите нуникальный номер пациента').show()
            return 0
        if not self.app_instance.db.add_patient(patient_local_id=patient_id):
            Snackbar(text='Проверьте правильность ввода ID').show()
            return 0
        Snackbar(text='Пациент успешно добавлен').show()
        self.ids.grid.clear_widgets()
        self.load_grid()
        return 1

    def on_leave(self, *args):
        self.ids.grid.clear_widgets()


class PatientCard(BoxLayout):
    fio = StringProperty('Малюгин Алексей Владимирович')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
