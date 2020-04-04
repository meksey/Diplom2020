from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class TestScreen(Screen):
	pass


class PatientCard:
	pass


class TestApp(MDApp):
	sm = None

	def __init__(self, **kwargs):
		self.title = "MyApp"
		self.theme_cls.primary_palette = "Blue"
		super().__init__(**kwargs)


	def build(self):
		with open('My.kv', encoding='utf8') as f:
			Builder.load_string(f.read())
		self.sm = ScreenManager()
		self.sm.add_widget(TestScreen())
		self.sm.current = 'test_screen'
		return self.sm



if __name__ == "__main__":
	TestApp().run()
