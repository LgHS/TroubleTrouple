import json
import time

import pyautogui
import setup

with open(setup.setup_path, 'r') as file:
    data =json.load(file)

positions = []
for i in range(16):
    positions.append({"x":0, "y":0})

positions[0]["x"] = data["firstPosition"][0]
positions[0]["y"] = data["firstPosition"][1]
positions[15]["x"] = data["lastPosition"][0]
positions[15]["y"] = data["lastPosition"][1]

width = positions[15]["x"] - positions[0]["x"]
height = positions[15]["y"] - positions[0]["y"]

for i in range(1,15):
    positions[i]["x"] = positions[0]["x"] + int(i%4)*(width/3)
    positions[i]["y"] = positions[0]["y"] + int(i/4)*(height/3)


def moveTo(i):
    pyautogui.moveTo(positions[i]["x"], positions[i]["y"], 0.2)

def dragTo(i):
    p=pyautogui.position()
    pyautogui.drag(positions[i]["x"]-p.x, positions[i]["y"]-p.y, duration=0.2, button="left")

def mouseDown():
    print("mouse down")
    pyautogui.mouseDown()

def mouseUp():
    print("mouse up")
    pyautogui.mouseUp()
