from inspect import getsourcefile
import os.path

class Ref():
	langs = ['Spanish', 'English']
	def __init__(self):
		raw_path = os.path.abspath(getsourcefile(lambda:0))
		#define language
		language = ''
		word = ''
		for l in raw_path:
			word += l
			if l == '\\'or l == '/':
				for lang in self.langs:
					if word[:-1] == lang:
						language = word[:-1]
				word = ''
		self.lang = language
		# Cleaning of path
		current_path = ''
		add = ''
		for l in raw_path:
		    add += l
		    if add[:-1] == language or add[:-1] == 'Languages':
		        add = ''
		    elif l == '\\' or l == '/':
		        current_path += add
		        add = ''
		self.current_dir = os.path.dirname(current_path)
		#parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

	def __call__(self):
		return self.current_dir, self.lang
    
if __name__ == '__main__':
    Ref()
    print(Ref()())