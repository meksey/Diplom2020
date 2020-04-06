from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from BL.utils import convert_timestamp_to_datetime


class TestingView(Screen):

    def on_enter(self, *args):
        user_testings = MDApp.get_running_app().user_data['data']

        for date, answers in sorted(user_testings.items(), reverse=True, key=lambda item: item[0]):
            date_obj = convert_timestamp_to_datetime(date)
            date = date_obj.strftime('%d %B %Y')
            card = TestingViewCard(date=date, answers=answers)
            self.ids.testings_grid.add_widget(card)


class TestingViewCard(BoxLayout):
    date = StringProperty('Неизвестно')
    answers = DictProperty()
    questions = {
        11: ['Вы употребляли вчера алкоголь?',
             {'A': 'Да, крепкий алкоголь', 'B': 'Да, слабоалкогольные напитки', 'C': 'Нет'}],
        12: ['Сколько вы спали прошлой ночью?', {'A': '1-5 часов', 'B': '6-8 часов', 'C': '9-12 часов'}],
        13: ['Сколько раз за день вы поели?', {'A': '1 раз', 'B': '2-3 раза', 'C': 'Больше 3 раз'}],
        14: ['У вас вчера болела голова?', {'A': 'Да', 'B': 'Да, но не сильно', 'C': 'Нет'}],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for question, answer in self.answers.items():
            q = self.questions[int(question)][0]
            ans = self.questions[int(question)][1][answer]
            row = TestingViewRow(question=q, answer=ans)
            self.ids.answers.add_widget(row)


class TestingViewRow(BoxLayout):
    question = StringProperty('Вопрос')
    answer = StringProperty('Ответ')
