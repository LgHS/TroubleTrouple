import string
import random
import time

import solver
import mouse


def generateLetterArray():
    return [[random.choice(string.ascii_uppercase) for i in range(4)] for j in range(4)]


def printArray(array):
    print("\n".join(list(map(lambda r: " ".join(r), array))))


testProblem = generateLetterArray()
print("test problem:")
printArray(testProblem)

print(",".join(map(lambda c: "'" + c + "'", solver.flatten(testProblem))))

solutions = solver.solve(testProblem)
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

# print(str(list(solver.findPath(['I','Q','Y','R','R','W','M','R','P','G','R','K','Z','X','I','Q'], "IQ", []))))
