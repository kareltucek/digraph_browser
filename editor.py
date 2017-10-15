#!/usr/bin/python
from lib import *
from geometry import *
from graph import *
import math
import sys

print("loading graph: " + sys.argv[1])

load_graph(sys.argv[1])

init_window()

mainloop()

