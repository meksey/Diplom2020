from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, DictProperty, StringProperty, ListProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivy.uix.boxlayout import BoxLayout


class TestingScreen(Screen):

	# questions[0] - Вопрос
	# questions[1] - Варианты ответа
	questions = {
		11: ['Вы употребляли вчера алкоголь?', {'A': 'Да, крепкий алкоголь', 'B': 'Да, слабоалкогольные напитки', 'C': 'Нет'}],
		12: ['Сколько вы спали прошлой ночью?', {'A': '1-5 часов', 'B': '6-8 часов', 'C': '9-12 часов'}],
		13: ['Сколько раз за день вы поели?', {'A': '1 раз', 'B': '2-3 раза', 'C': 'Больше 3 раз'}],
		14: ['У вас вчера болела голова?', {'A': 'Да', 'B': 'Да, но не сильно', 'C': 'Нет'}],
	}

	q_current = NumericProperty()
	q_count = NumericProperty()
	answers = DictProperty()

	def on_enter(self, *args):
		self.q_count = len(self.questions)
		self.q_current = 0

		for question_num, question in self.questions.items():
			card = QuestionCard(text=question[0], testing_screen=self, number=question_num)
			i = 1
			for num, variant in question[1].items():
				card.add_height()
				card.ids.answers_vars.add_widget(QuestionRow(
					question_number=num,
					text=variant,
					question_card=card,
					checkbox_group=question[0],
				))
				i += 1
			i = 0
			self.ids.grid.add_widget(card)

	def on_answers(self, obj, value):
		self.q_current = len(value)
		if self.q_current == self.q_count:
			self.ids.done_btn.disabled = False

	def update_answers(self, question_number, answer_variant):
		self.answers.update({question_number: answer_variant})

	def save(self):
		app_instance = MDApp.get_running_app()
		res = app_instance.db.patch_daily_testing(app_instance.local_id, app_instance.id_token, self.answers)

		if not res:
			Snackbar(text='Не удалось записать тестирование на сервер').show()
		else:
			self.manager.current = 'manage'
			app_instance.user_data = {**app_instance.user_data, **{'lastTestingTime': res}}
			Snackbar(text='Данные успешно записаны').show()

	def on_leave(self, *args):
		self.ids.grid.clear_widgets()
		self.q_current = 0
		self.q_count = 0
		self.answers = {}
		self.ids.done_btn.disabled = True


class QuestionCard(BoxLayout):
	number = NumericProperty()
	text = StringProperty()
	card_height = NumericProperty(10)
	selected_answer = StringProperty()
	testing_screen = ObjectProperty()

	def on_selected_answer(self, obj, value):
		self.testing_screen.update_answers(self.number, self.selected_answer)

	def add_height(self):
		self.card_height = self.card_height + 50


class QuestionRow(BoxLayout):
	question_number = StringProperty()
	text = StringProperty()
	checkbox_group = StringProperty()
	question_card = ObjectProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.checkbox = self.ids.question_check
		self.checkbox.bind(active=self.on_checkbox_active)

	def on_checkbox_active(self, checkbox, value):
		if value:
			self.question_card.selected_answer = self.question_number
