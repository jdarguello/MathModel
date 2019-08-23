import ipywidgets as widgets
import subprocess

class Button():
	def __init__(self, name='Data Selection'):
		button = widgets.Button(description='Data Selection')
		out = widgets.Output()
		button.on_click(self.on_button_clicked)
		widgets.VBox([button, out])
	def on_button_clicked(self, b):
	    with out:
	        subprocess.run("jupyter lab Languages/" + lang.value() + "/data.ipynb")
