from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty, DictProperty, StringProperty, ListProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout


class TestingScreen(Screen):
	questions = {
		'Вы употребляли вчера алкоголь?': ['Да, крепкий алкоголь', 'Да, слабоалкогольные напитки', 'Нет'],
		'Сколько вы спали прошлой ночью?': ['1-5 часов', '6-8 часов', '9-12 часов'],
		'Сколько раз за день вы поели?': ['1 раз', '2-3 раза', 'Больше 3 раз'],
		'У вас вчера болела голова?': ['Да', 'Да, но не сильно', 'Нет'],
		'У вас голова?': ['Да', 'Да, но не сильно', 'Нет', 'Нет, но не сильно'],
	}

	q_current = NumericProperty()
	q_count = NumericProperty()
	answers = DictProperty()

	def on_enter(self, *args):
		self.q_count = len(self.questions)
		self.q_current = 0

		for q, a in self.questions.items():
			card = QuestionCard(text=q, testing_screen=self)
			i = 1
			for variant in a:
				card.add_height()
				card.ids.answers_vars.add_widget(QuestionRow(
					question_number=1,
					text=variant,
					question_card=card,
					checkbox_group=q,
				))
				i += 1
			i = 0
			self.ids.grid.add_widget(card)

	def on_answers(self, obj, value):
		self.q_current = len(value)
		if self.q_current == self.q_count:
			self.ids.done_btn.disabled = False

	def update_answers(self, question, answer):
		self.answers.update({question: answer})

	def save(self):
		print(self.answers)
		app_instance = MDApp.get_running_app()
		app_instance.db.patch_daily_testing(app_instance.local_id, app_instance.id_token, {})

	def on_leave(self, *args):
		self.ids.grid.clear_widgets()
		self.q_current = 0
		self.q_count = 0
		self.answers = {}
		self.ids.done_btn.disabled = True


class QuestionCard(BoxLayout):
	text = StringProperty()
	card_height = NumericProperty(10)
	selected_answer = StringProperty()
	testing_screen = ObjectProperty()

	def on_selected_answer(self, obj, value):
		self.testing_screen.update_answers(self.text, self.selected_answer)

	def add_height(self):
		self.card_height = self.card_height + 50


class QuestionRow(BoxLayout):
	question_number = NumericProperty()
	text = StringProperty()
	checkbox_group = StringProperty()
	question_card = ObjectProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.checkbox = self.ids.question_check
		self.checkbox.bind(active=self.on_checkbox_active)

	def on_checkbox_active(self, checkbox, value):
		if value:
			self.question_card.selected_answer = self.text
