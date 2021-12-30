from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window


class TaaSApp(App):
    pass
    # def build(self):
    #     mainLayout = BoxLayout(orientation='vertical')
    #     return mainLayout


def main():
    Window.top, Window.left = (100, 100)
    Window.clearcolor = (0.5, 0.5, 0.5, 1)
    TaaSApp().run()


if __name__ == '__main__':
    main()
    # x = AsyncImage(source='https://i.stack.imgur.com/gN9W5.png')
