from kivymd.app import MDApp
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import Screen
# from kivy.uix.textinput import TextInput

from Mobile_App import Mobile_Main


class MainApp(MDApp):

    def build(self):
        screen = Screen()
        self.theme_cls.primary_palette = 'Green'
        # main_layout = BoxLayout(orientation='vertical')
        # self.solution = TextInput(background_color='black', foreground_color='white')
        #
        # main_layout.add_widget(self.solution)
        button = MDRectangleFlatButton(text='Bekaxdd', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        screen.add_widget(button)
        return screen

if __name__ == '__main__':
    app = MainApp()
    app.run()