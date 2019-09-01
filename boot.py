import machine,os,ujson,sys,time


print('Booting..')

sys.path.append('/flash/libs')
sys.path.append('flowlib/lib')

from m5stack import *
import menu as mnu
import helper as hp
import custbutton as btn
config = {}
with open('config.cfg','r') as configFile:
    config = ujson.load(configFile)

buttonA = machine.Pin(37, machine.Pin.IN)
buttonB = machine.Pin(39, machine.Pin.IN)

M5Led.on()
time.sleep(2)
M5Led.off()


def configWiFi():
	lcd.clear(lcd.BLACK)
	lcd.text(lcd.CENTER,30,'192.168.4.1')
	import wifiConfig
	wifiConfig.setupWifi()
	
	return 1
def configUSB():
	lcd.clear(lcd.BLACK)
	lcd.text(lcd.CENTER,lcd.CENTER,'Enter config using serial\nport.\nhp.setPara(key,value)')
	return 1

def configKeyCard():
	pass

def debugMenu():
	return 1


if buttonA.value() == 0:
    import main_menu
elif buttonB.value()==0:
	settingMenu = mnu.Menu(hp.tft,btn,header='Settings',landscape=True)
	settingMenu.addMenuItem('Setup WiFi',configWiFi)
	settingMenu.addMenuItem('Configure Using USB',configUSB)
	settingMenu.addMenuItem('Configure Using Key Card',configKeyCard)
	settingMenu.addMenuItem('Debug Menu',debugMenu)
	settingMenu.run()
else:
    os.chdir('apps/'+config['apps']['defaultApp'])
    import main