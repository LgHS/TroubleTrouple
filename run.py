import ocrdev.step1Capture
import ocrdev.step2OCR
import solver
import time
import mouse

ocrdev.step1Capture.capture()
letters=ocrdev.step2OCR.analyseImage()

print("problem:")
solver.printArray(letters)

solutions = solver.solve(letters)

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
