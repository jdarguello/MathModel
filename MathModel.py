import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

with open('Presentation.ipynb') as f:
	nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': '.'}})

with open('Presentation.ipynb', mode='w', encoding='utf-8') as f:
	nbformat.write(nb, f)