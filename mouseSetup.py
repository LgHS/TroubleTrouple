import time
from datetime import datetime
import pyautogui
import json
import setup

def takeWhenNotMoving():
    lastPosition = None
    lastPositionTime = datetime.now()
    while True:
        position = pyautogui.position()
        if (position != lastPosition):
            lastPosition = position
            lastPositionTime = datetime.now()
        elif (lastPositionTime.timestamp() + 2 < datetime.now().timestamp()):
            return position
        time.sleep(0.2)

data = {
}
print("go to first box")
p = takeWhenNotMoving()
data['firstPosition'] = p

print("go to last box")
data['lastPosition'] = takeWhenNotMoving()



with open(setup.setup_path, 'w') as f:
    json.dump(data, f)