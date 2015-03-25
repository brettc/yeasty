from base import *

# Just import everything to register it...
# import series, sizes, dump
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module == 'base.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
