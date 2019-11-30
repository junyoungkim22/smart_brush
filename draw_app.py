from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from draw_widget import DrawWidget


class MyDrawApp(App):
    def build(self):
        parent = Widget()
        self.painter = DrawWidget()
        clear_btn = Button(text='Clear')
        clear_btn.bind(on_release=self.clear_canvas)
        start_btn = Button(text="Start")
        start_btn.bind(on_release=self.draw_start)

        parent.add_widget(self.painter)
        parent.add_widget(clear_btn)
        parent.add_widget(start_btn)
        return parent

    def draw_start(self, obj):
        self.painter.open_serial() 
    def clear_canvas(self, obj):
        self.painter.canvas.clear()

if __name__ == '__main__':
    MyDrawApp().run()