import mouse
import time

def runSolution(s):


    print("play solution %s" % (s))
    down = False
    for c in s:
        print("goTo %s" % (c))
        if (not down):
            mouse.moveTo(c)
            mouse.mouseDown()
            down = True
        else :
            mouse.dragTo(c)
    mouse.mouseUp()
    time.sleep(0.1)
