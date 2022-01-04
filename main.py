from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.core.window import Window

import taas


class TaaSGUIApp(App):
    def log(self, text, append=False):
        """Write something to the log box"""
        if append:
            text = f'{self.root.ids.log.text}\n{str(text)}'
        self.root.ids.log.text = str(text)

    def on_auth(self, username, password):
        self.log('Getting auth token...')
        r = taas.get_auth_token(username, password)
        self.log(r, append=True)

    def on_get_campaigns(self, name):
        self.log('Getting test campaigns...')
        r = taas.get_test_campaigns(name)
        self.log(r, append=True)


def main():
    Window.top, Window.left = (100, 100)
    Window.clearcolor = (0.5, 0.5, 0.5, 1)
    TaaSGUIApp().run()


if __name__ == '__main__':
    main()
    # x = AsyncImage(source='https://i.stack.imgur.com/gN9W5.png')
