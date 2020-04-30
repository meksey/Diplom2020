from time import sleep
from threading import Thread

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivymd.uix.spinner import MDSpinner


KV = r'''
ScreenManager:
    Screen:
        name: 'start'
        Button:
            size_hint: .5, .5
            pos_hint: {'center': (.5, .5)}
            text: 'hit me!'
            on_press: app.start_task()
        
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(30), dp(30)

        
    Screen:
        name: 'loading'
        Label:
            text: 'loading…\n' + '.' * (app.count % 15)
    Screen:
        name: 'done'
        Label:
            text: 'done!'
'''


class Application(MDApp):
    count = NumericProperty()

    def build(self):
        return Builder.load_string(KV)

    def start_task(self):
        self.root.current = 'loading'
        Thread(target=self._slow_task).start()

    def _slow_task(self):
        for i in range(10):
            sleep(.3)
            self.count += 1

        self.root.current = 'done'


if __name__ == "__main__":
    Application().run()