import ocrdev.step1Capture
import ocrdev.step2OCR
import solver
import time
import mouse
import game

ocrdev.step1Capture.capture()
letters=ocrdev.step2OCR.analyseImage()

print("problem:")
solver.printArray(letters)

solutions = solver.solve(letters)

for s in solutions[0:10]:
    game.runSolution(s)

# print(str(list(solver.findPath(['I','Q','Y','R','R','W','M','R','P','G','R','K','Z','X','I','Q'], "IQ", []))))
