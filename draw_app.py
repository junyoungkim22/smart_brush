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

class UserScreen(GridLayout):
	def __init__(self, **kwargs):
	    super(UserScreen, self).__init__(**kwargs)
	    self.cols = 2
	    self.add_widget(Label(text='User Name'))
	    self.username = TextInput(multiline=False)
	    self.add_widget(self.username)
	    self.add_widget(Label(text='password'))
	    self.password = TextInput(password=True, multiline=False)
	    self.add_widget(self.password)
	    self.draw_screen = DrawWidget()
	    self.add_widget(self.draw_screen)



class MyDrawApp(App):
	def build(self):
		return UserScreen();
		#return DrawWidget()

if __name__ == '__main__':
	MyDrawApp().run()