from IPython.display import *
from traitlets import HasTraits, observe, directional_link
from ipywidgets import Dropdown

class Droppy(HasTraits):
	"""
		Desarrollo de dropdown y obtención de información
		de los mismos.
	"""
	Answer = False
	def __init__(self, options, **kwargs):
		if kwargs:
			self.widget = Dropdown(
				options = options,
				value=kwargs['value']
				)
		else:
			self.widget = Dropdown(options = options)

	def __call__(self):
		return self.widget.value

	@observe('widget')
	def _observe_widget(self, change):
		self.Answer = change['new']

class Down():
	def __init__(self, options = ['English', 'Spanish'], value = 'English'):
		self.Drop = Droppy(options, value=value)
		display(self.Drop.widget)

	def value(self):
		return self.Drop()