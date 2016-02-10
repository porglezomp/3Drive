import random
import RPi.GPIO as GPIO
import time
import cv2
import sys
import itertools

DELAY = 0.005

xPins = [18, 23, 24, 25]
yPins = [22, 27, 17, 4]
zPins = [8, 7]


def moveX(w1, w2, w3, w4):
  GPIO.output(xPins[0], w1)
  GPIO.output(xPins[1], w2)
  GPIO.output(xPins[2], w3)
  GPIO.output(xPins[3], w4)


def moveY(w1, w2, w3, w4):
  GPIO.output(yPins[0], w1)
  GPIO.output(yPins[1], w2)
  GPIO.output(yPins[2], w3)
  GPIO.output(yPins[3], w4)


def moveZ(w1, w2):
  GPIO.output(zPins[0], w1)
  GPIO.output(zPins[1], w2)


def drawDot():
  moveZ(0, 0)
  time.sleep(0.2)
  moveZ(0, 1)
  time.sleep(0.34)
  moveZ(0, 0)
  time.sleep(0.2)
  moveZ(1, 0)
  time.sleep(0.5)


NEGATIVE_PATTERN = [(1,0,1,0), (1,0,0,1), (0,1,0,1), (0,1,1,0)]


def moveLeft(steps):
  for _ in range(steps):
    for w1, w2, w3, w4 in NEGATIVE_PATTERN:
      moveX(w1, w2, w3, w4)
      time.sleep(DELAY)


def moveYDown(steps):
  for _ in range(steps):
    for w1, w2, w3, w4 in NEGATIVE_PATTERN:
      moveY(w1, w2, w3, w4)
      time.sleep(DELAY)


POSITIVE_PATTERN = [(1,0,1,0), (1,0,0,1), (0,1,0,1), (0,1,1,0)]


def moveRight(steps):
  for _ in range(steps):
    for w1, w2, w3, w4 in POSITIVE_PATTERN:
      moveX(w1, w2, w3, w4)
      time.sleep(DELAY)


def moveYUp(steps):
  for _ in range(steps):
    for w1, w2, w3, w4 in POSITIVE_PATTERN:
      moveY(w1, w2, w3, w4)
      time.sleep(DELAY)


if __name__ == '__main__':
  img = cv2.imread(sys.argv[1])

  height, width = img.shape[0], img.shape[1]

  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  # Set all of the GPIO pins to output mode
  for pin in itertools.chain(xPins, yPins, zPins):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

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
