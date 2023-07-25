from kivy.app import App
from Mobile_App import Mobile_Main


class MainApp(App):

    def build(self):
        self.figure = Mobile_Main.Figure1


if __name__ == '__main__':
    app = MainApp()
    app.run()