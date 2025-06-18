import string
import random
import time

import game
import solver
import mouse

def generateLetterArray():
    return [[random.choice(string.ascii_uppercase) for i in range(4)] for j in range(4)]




testProblem = generateLetterArray()
print("test problem:")
solver.printArray(testProblem)

print(",".join(map(lambda c: "'" + c + "'", solver.flatten(testProblem))))

solutions = solver.solve(testProblem)
for s in solutions[0:2]:
    game.runSolution(s)