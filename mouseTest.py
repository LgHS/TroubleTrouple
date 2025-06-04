import time

import mouse

for i in range(16):
    mouse.moveTo(i)
    time.sleep(0.2)
    