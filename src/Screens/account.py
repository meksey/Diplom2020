from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from threading import Thread
import threading


class AccountScreen(Screen):
	user_name = StringProperty()
	user_surname = StringProperty()
	user_patronymic = StringProperty()
	email = StringProperty()
	vk_link = StringProperty()
	telegram_link = StringProperty()
	country = StringProperty()
	city = StringProperty()
	med = StringProperty()

	app_instance = MDApp.get_running_app()

	current_user = {}
	new_user = {}

	thread = None

	def on_enter(self, *args):
		self.current_user = self.app_instance.user_data

		if 'email' in self.current_user:
			self.email = self.current_user['email']
		if 'name' in self.current_user:
			self.user_name = self.current_user['name']
		if 'surname' in self.current_user:
			self.user_surname = self.current_user['surname']
		if 'patronymic' in self.current_user:
			self.user_patronymic = self.current_user['patronymic']
		if 'vk' in self.current_user:
			self.vk_link = self.current_user['vk']
		if 'telegram' in self.current_user:
			self.telegram_link = self.current_user['telegram']
		if 'country' in self.current_user:
			self.country = self.current_user['country']
		if 'city' in self.current_user:
			self.city = self.current_user['city']
		if 'med' in self.current_user:
			self.med = self.current_user['med']

	def update_data(self, field, value):
		self.new_user[field] = value

	def do_update(self):
		temp_user_data = self.current_user.copy()
		if 'data' in temp_user_data:
			del temp_user_data['data']

		set_old = set(temp_user_data.items())
		set_new = set(self.new_user.items())
		update_dict = dict(set_new - set_old)

		if not update_dict:
			print('Ни одного значения не изменнено')
			return

		app = self.app_instance

		# Запись изиенений в БД
		to_upload = app.db.patch_account_data(app.local_id, app.id_token, update_dict)
		if not to_upload:
			Snackbar(text='Данные не удалось загрузить на сервер').show()
			return 0

		app.user_data = {**app.user_data, **update_dict}
		Snackbar(text='Данные успешно обновлены').show()
