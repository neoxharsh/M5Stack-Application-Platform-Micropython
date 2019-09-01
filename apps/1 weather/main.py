from m5stack import *
import _thread,gc,utime
import helper as hp
import custbutton as btn
from flowlib.lib import urequests

from tpLinkWeb import TPLinkSmartBulb

SmartBulb = TPLinkSmartBulb({'deviceID':'','url':''})

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

import machine

_intindex=0
previousTime = ""
previousDate = ""

lcd.orient(1)

lcd.clear(lcd.BLACK)
lcd.setTextColor(lcd.WHITE, lcd.BLACK)
lcd.font(lcd.FONT_Default)

weatherPara = hp.getAllPara('weather')
if len(weatherPara)<2:
	hp.setPara('weather','')
	weatherPara = hp.getAllPara('weather')


weatherUrl =  'https://api.darksky.net/forecast//{0},{1}?exclude=minutely,hourly,daily,alerts,flags&units=si'
weatherUrl = weatherUrl.format(weatherPara[0],weatherPara[1])

def updateTime(_tim):
	global previousTime,previousDate
	now = utime.localtime()
	_h = now[3]
	if _h > 12:
		_h = _h - 12
	nowTime = "{0:02d}:{1:02d}:{2:02d}".format(_h,now[4],now[5])
	nowDate =  "{0:02d}-{1:02d}-{2}".format(now[2],now[1],now[0])
	lcd.text(lcd.RIGHT,0,previousTime,0x000000)
	if nowDate is not previousDate:
		lcd.text(0,0,previousDate,0x000000)
		lcd.text(0,0,nowDate)
	lcd.font(lcd.FONT_Default)	
	lcd.text(lcd.RIGHT,0,nowTime)
	previousTime = nowTime
	previousDate =  nowDate
	hp.drawBattery(130,14)

def _updateWeather():
	global _intindex
	gc.collect()
	try:
		weather = urequests.get(weatherUrl)
		weather = weather.json()
		print(str(_intindex))
		print(weather)
		_intindex += 1
		summary = weather['currently']['summary']
		temp = weather['currently']['temperature']
		humidity = str(float(weather['currently']['humidity'])*100) + "%"
		wind = weather['currently']['windSpeed'] * 3.6
		icon = weather['currently']['icon']
		lcd.rect(0,15,160,80,0x000000,0x000000)
		lcd.text(0,42,summary)
		lcd.font(lcd.FONT_DejaVu24)
		lcd.text(0,14,str(temp) + "C")
		lcd.font(lcd.FONT_Default)
		lcd.text(0,54,"Humid: "+ str(humidity))
		lcd.text(0,67,"Wind:  "+ str(wind))
		if icon+".jpg" in os.listdir('imgs'):
			lcd.image(120,40,'imgs/'+icon+".jpg")
		else:
			lcd.rect(0,15,160,80,0x000000,0x000000)
			lcd.font(lcd.FONT_DejaVu24)
			lcd.text(lcd.CENTER,lcd.CENTER,icon)
			lcd.font(lcd.FONT_Default)
	except Exception as e:
		pass
	

def updateWeather(time):
	_thread.start_new_thread(_updateWeather,())


def toggleLight():
	try:
		gc.collect()
		M5Led.on()
		SmartBulb.toggle()
		M5Led.off()
	except Exception as e:
		M5Led.on()
		utime.sleep(2)
		M5Led.off()


hp.updateTime(TIME_DIFF=[10,0])

timeUpdateTimer = machine.Timer(2)
timeUpdateTimer.init(period=999,mode=timeUpdateTimer.PERIODIC,callback=updateTime)

weatherUpdateTimer = machine.Timer(3)
weatherUpdateTimer.init(period=600000,mode=weatherUpdateTimer.PERIODIC,callback=updateWeather)


axp.setLDO2Vol(hp.currentBrightness)

hp.connectWiFi()

updateWeather(None)

while True:
	_buttonState = btn.getButtonsState()
	if _buttonState == btn.BUTTON_B:
		hp.changeBrightness()
	if _buttonState == btn.BUTTON_A:
		toggleLight()

