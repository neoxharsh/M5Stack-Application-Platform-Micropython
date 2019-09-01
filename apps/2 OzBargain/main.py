from helper import *
from flowlib.lib import urequests
import gc,time,_thread,hat
from ucollections import deque
import custbutton as btn

speaker = hat.get(hat.SPEAKER)

lcd.orient(1)
lcd.font(lcd.FONT_DefaultSmall)
lcd.clear(lcd.BLACK)
connectWiFi()

if machine.nvs_getstr('ozbargain')==None:
	machine.nvs_setstr('ozbargain','')

INTERVAL_TIME = 1
updateTimer = ""
ozBargainURL = "https://www.ozbargain.com.au/api/live?last={0}&disable=votes%2Cwiki&types=Ad%2CComp%2CForum"

epochOffset = 946648756

ledBit = False

ozData = []

currentTimeStamp = time.time()+epochOffset

def updateData(timeStamp=None):
	global currentTimeStamp,ozData,ozBargainURL,currentAlert,updateTimer
	alertList = getAllPara('ozbargain')
	gc.collect()
	if timeStamp==None:
		req = urequests.get(ozBargainURL.format(currentTimeStamp)).json()
		if len(req['records'])<1:
			return
		for x in req['records']:
			ozData.insert(0,x['title'][:26])
		ozData = ozData[:8]
		lcd.clear(lcd.BLACK)
		for x in range(len(ozData)):
			lcd.text(0,x*13,ozData[x])
	else:	
		req = urequests.get(ozBargainURL.format(timeStamp)).json()
	currentTimeStamp = req['timestamp']
	if alertList is not None:
		for x in alertList:
			for y in ozData:
				if x.lower() in y.lower()  and x is not '' and x is not ',':
					ledTimer = timEx.addTimer(1000,timEx.PERIODIC,alertLed)
					updateTimer.deinit()
					lcd.clear(lcd.BLACK)
					lcd.text(lcd.CENTER,lcd.CENTER,x)
					while True:
						_state = btn.getButtonsState()
						if _state==btn.BUTTON_A:
							ledTimer.deinit()
							alertList = getAllPara('ozbargain')
							alertList.remove(x)
							_temp = ''
							for x in alertList:
								_temp += ','+x
							setPara('ozbargain',_temp)
							M5Led.pin.value(1)
							updateTimer = timEx.addTimer(30000,timEx.PERIODIC,_updateData)
							_updateData()
							break			
	gc.collect()

def _updateData():
	_thread.start_new_thread(updateData,())


def alertLed():
	global ledBit
	M5Led.pin.value(ledBit)
	speaker.tone(600)
	ledBit = not ledBit
	

updateTimer = timEx.addTimer(30000,timEx.PERIODIC,_updateData)
_updateData()