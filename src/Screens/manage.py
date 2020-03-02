from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from BL.utils import convert_timestamp_to_datetime
from kivymd.app import MDApp


class ManageScreen(Screen):

	last_testing_time = StringProperty('Последнее тестирование: Неизвестно')

	def on_enter(self, *args):

		date = MDApp.get_running_app().user_data['lastTestingTime']
		date_obj = convert_timestamp_to_datetime(date)
		self.last_testing_time = 'Последнее тестирование: ' + date_obj.strftime('%d %B %Y')

		recs = {
			'Рекоммендации по питанию': ['Есть меньше мучного', 'Пить больше кофе', 'Питаться энергией солнца'],
			'Рекоммендации по образу жизни': ['Больше проводить времени на улице', 'Меньше курить', 'Не находиться на солнце слишком много'],
		}

		for key, value in recs.items():
			self.ids.grid.add_widget(RecommendationCard(category=key, variants=value))
			self.ids.grid.add_widget(RecommendationCard(category=key, variants=value))



class RecommendationCard(BoxLayout):
	category = StringProperty()
	variants = ListProperty()

	def on_kv_post(self, base_widget):
		for el in self.variants:
			self.ids.rec_list.add_widget(RecommendationRow(variant=el))


class RecommendationRow(BoxLayout):
	variant = StringProperty()


