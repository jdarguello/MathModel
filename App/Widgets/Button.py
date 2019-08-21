import ipywidgets as widgets
button = widgets.Button(description='Display Chart')
out = widgets.Output()
def on_button_clicked(b):
    button.description = 'clicked'
    with out:
        print('Ay')

button.on_click(on_button_clicked)
widgets.VBox([button, out])