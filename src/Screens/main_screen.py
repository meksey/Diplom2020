from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
from BL.utils import convert_timestamp_to_datetime
from datetime import datetime
from kivymd.uix.navigationdrawer import NavigationDrawerIconButton


class MainScreen(Screen):
	toolbar_title = StringProperty('Привет')

	def on_enter(self, *args):

		app_instance = MDApp.get_running_app()
		self.ids.main_sm.current = 'manage' if self.is_test_yet() else 'testing'

		if 'name' in app_instance.user_data:
			self.toolbar_title = 'Привет, ' + app_instance.user_data['name']
		else:
			self.toolbar_title = 'Привет'

	def is_test_yet(self):
		app_instance = MDApp.get_running_app()

		if 'lastTestingTime' not in app_instance.user_data:
			return False

		last_testing_time = convert_timestamp_to_datetime(app_instance.user_data['lastTestingTime'])
		now = datetime.today()

		if now.date() == last_testing_time.date():
			return 1

		return 0
