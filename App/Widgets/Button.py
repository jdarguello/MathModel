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