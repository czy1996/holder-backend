import sys
from os.path import abspath
from os.path import dirname

print('***', sys.path)

import app

sys.path.insert(0, abspath(dirname(__file__)))
print('***', sys.path)
application = app.app
