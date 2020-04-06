from kivymd.app import MDApp
from kivy.lang import Builder
import os
from BL.database import DataBase
from kivy.uix.screenmanager import ScreenManager
from Screens.start_screen import StartScreen
from Screens.main_screen import MainScreen
from kivymd.uix.snackbar import Snackbar
from BL.utils import read_refresh_token


class IDocApp(MDApp):

	# Подгружаемые с сервера данные о пользователях
	user_data = {}
	local_id = None
	id_token = None

	# Общие поля
	db = None
	logged = None
	sm = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.accent_palette = 'Cyan'

	def build(self):
		self.db = DataBase()
		self.logged = False
		self.sm = ScreenManager()

		refresh_token = read_refresh_token()

		if not refresh_token:
			self.logged = False
		elif self.db.login_refresh_token(refresh_token):
			self.logged = True
		else:
			Snackbar(text='Не удалось подгрузить данные').show()
		self.load_kv_from_dir('{}/UI'.format(self.directory))
		self.sm.add_widget(MainScreen())
		self.sm.add_widget(StartScreen())

		if self.logged:
			self.sm.current = 'main'
		else:
			self.sm.current = 'start'

		return self.sm

	def load_kv_from_dir(self, _dir):
		for kv in os.listdir(_dir):
			if os.path.isdir('{}/{}'.format(_dir, kv)):
				continue
			else:
				with open('{}/{}'.format(_dir, kv), encoding='utf8') as f:
					Builder.load_string(f.read())


directory = os.path.dirname(__file__)
app = IDocApp()
app.run()

# TODO: добавить везде методы on_leave
