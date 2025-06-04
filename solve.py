import string
import random
import time

import solver
import mouse

def solve(array):
    solutions = solver.solve(array)
    for s in solutions:
        print("play solution %s" % (s))
        down=False
        for c in s:
            print("goTo %s" % (c))
            mouse.moveTo(c)
            if(not down):
                mouse.mouseDown()
                down=True
            time.sleep(0.2)
        mouse.mouseUp()

