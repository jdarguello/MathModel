import os

class list_files():
    def __init__(self, startpath):
        for root, dirs, files in os.walk(startpath):
            level = self.enc(root).replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(self.enc(root))))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

    def enc(self, s):
        return s.encode('utf-8', 'surrogateescape').decode('utf-8')

if __name__ == '__main__':
    anterior = os.path.dirname(os.path.realpath(__file__))
    list_files(anterior)
