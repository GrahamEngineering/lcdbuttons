import Adafruit_CharLCD as LCD
import lcdbut
#import Queue
import threading
import time
from pydispatch import dispatcher

color=0
colorlist = [[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,1,1]]

def msgUpdate(msg):
	lcd.clear()
	lcd.message(msg)

def selectItem():
	msgUpdate("Select")

def goRight():
	msgUpdate("Right")
	lcd.show_cursor(True)
	
def goLeft():
	msgUpdate("Left")
	lcd.show_cursor(False)

def goUp():
	msgUpdate("Up")
	global color
	if color == (len(colorlist) - 1):
		color = 0
	else:
		color += 1
	updateColor()
def goDown():
	msgUpdate("Down")
	global color
	if color == 0:
		color = (len(colorlist) - 1)
	else:
		color -= 1
	updateColor()

def updateColor():
	lcd.set_color(colorlist[color][0], colorlist[color][1], colorlist[color][2])

dispatcher.connect( selectItem, signal='selectPressed', sender=dispatcher.Any)
dispatcher.connect( goRight, signal='rightPressed', sender=dispatcher.Any)
dispatcher.connect( goLeft, signal='leftPressed', sender=dispatcher.Any)
dispatcher.connect( goUp, signal='upPressed', sender=dispatcher.Any)
dispatcher.connect( goDown, signal='downPressed', sender=dispatcher.Any)

lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_backlight(False)

lcd.set_backlight(True)
updateColor()

x = lcdbut.lcdbut(lcd)

t = threading.Thread(target=x.startup)

t.start()

while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print "Stopping thread..."
		x.stop = True
		print "Waiting..."
		time.sleep(0.5)
		print "Exiting..."
		lcd.clear()
		lcd.set_backlight(False)
		exit()
