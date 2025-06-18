import mouse
import time

def runSolution(s):


    print("play solution %s" % (s))
    down = False
    for c in s:
        print("goTo %s" % (c))
        mouse.moveTo(c)
        if (not down):
            mouse.mouseDown()
            down = True
        time.sleep(0.2)
    mouse.mouseUp()
    time.sleep(0.1)
