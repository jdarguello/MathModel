import ipywidgets as widgets
import subprocess
button = widgets.Button(description='Data Selection')
out = widgets.Output()
def on_button_clicked(b):
    with out:
        language = lang.value()
        try:
            subprocess.run("jupyter lab Languages/" + language + "/data.ipynb")
        except:
            subprocess.run("jupyter lab 'Languages/" + language + "/data.ipynb'")
button.on_click(on_button_clicked)
widgets.VBox([button, out])

class A:
	def __init__(self):
		print("hola, soy A")

class B:
	def __init__(self):
		print("hola, soy B")

class C(A,B):
	def __init__(self):
		print("C?")
		super().__init__()
		super(A, self).__init__()

C()
