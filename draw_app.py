from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

comPort = 'COM4'
comPortBaud = 9600

class DrawWidget(Widget):
	def on_touch_down(self, touch):
		color = (random(), random(), random())
		with self.canvas:
			Color(*color)
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
			touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]


class MyDrawApp(App):
	def build(self):
		parent = Widget()
		self.painter = DrawWidget()
		clear_btn = Button(text='Clear')
		clear_btn.bind(on_release=self.clear_canvas)
		parent.add_widget(self.painter)
		parent.add_widget(clear_btn)
		return parent

	def clear_canvas(self, obj):
		self.painter.canvas.clear()

if __name__ == '__main__':
	MyDrawApp().run()