from inspect import getsourcefile
import os.path

class Ref():
	def __init__(self, language):
		raw_path = os.path.abspath(getsourcefile(lambda:0))
		# Cleaning of path
		current_path = ''
		add = ''
		for l in raw_path:
		    add += l
		    if add[:-1] == language or add[:-1] == 'Languages':
		        add = ''
		    elif l == '\\':
		        current_path += add
		        add = ''
		self.current_dir = os.path.dirname(current_path)
		#parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

	def __call__(self):
		return self.current_dir