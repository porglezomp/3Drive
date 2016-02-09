import random
import RPi.GPIO as GPIO
import time
import cv2
import sys
import itertools

img = cv2.imread(sys.argv[1])

height, width = img.shape[0], img.shape[1]

delay = 0.005

xPins = [18, 23, 24, 25]
yPins = [22, 27, 17, 4]
zPins = [8, 7]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set all of the GPIO pins to output mode
for pin in itertools.chain(xPins, yPins, zPins):
  GPIO.setup(pin, GPIO.OUT)  
  GPIO.output(pin, False)


def moveAxis(pins):
  def move(*inputs):
    assert len(inputs) == len(pins)
    for i, pin in enumerate(pins):
      GPIO.output(pin, inputs[i])
  return move

moveX = moveAxis(xPins)
moveY = moveAxis(yPins)
moveZ = moveAxis(zPins)

NEGATIVE_PATTERN = [(1, 0, 1, 0), (1, 0, 0, 1), (0, 1, 0, 1), (0, 1, 1, 0)]
POSITIVE_PATTERN = [(0, 1, 1, 0), (0, 1, 0, 1), (1, 0, 0, 1), (1, 0, 1, 0)]


def movePattern(mover,  pattern):
  def motion(steps):
    for _ in range(steps):
      for w1, w2, w3, w4 in pattern:
        mover(w1, w2, w3, w4)
        time.sleep(delay)
  return motion

moveLeft = movePattern(moveX, NEGATIVE_PATTERN)
moveYDown = movePattern(moveY, NEGATIVE_PATTERN)
moveRight = movePattern(moveX, POSITIVE_PATTERN)
moveYUp = movePattern(moveY, POSITIVE_PATTERN)


def drawDot():
  moveZ(0, 0)
  time.sleep(0.2)
  moveZ(0, 1)
  time.sleep(0.34)
  moveZ(0, 0)
  time.sleep(0.2)
  moveZ(1, 0)
  time.sleep(0.5)


for x in range(width):
  for y in range(height):
    print "Row: {}\nCol: {}".format(x, y)
    percentDone = (x * y) / (width * height)
    print "Percent complete: {}%".format(percentDone)
    red = img[y, x, 2]
    green = img[y, x, 1]
    blue = img[y, x, 0]

    if red != 255 and green != 255 and blue != 255:
      drawDot()
    moveRight(1)

  #Go back to the start of the row
  moveLeft(height)
  moveYUp(1)

moveYDown(width)
