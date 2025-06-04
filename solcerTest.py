import string
import random

import solver


def generateLetterArray():
    return [[random.choice(string.ascii_uppercase) for i in range(4)] for j in range(4)]


def printArray(array):
    print("\n".join(list(map(lambda r: " ".join(r), array))))



testProblem=generateLetterArray()
print("test problem:")
printArray(testProblem)

print(",".join(map(lambda c : "'"+c+"'", solver.flatten(testProblem))))


solver.solve(testProblem)

#print(str(list(solver.findPath(['I','Q','Y','R','R','W','M','R','P','G','R','K','Z','X','I','Q'], "IQ", []))))
