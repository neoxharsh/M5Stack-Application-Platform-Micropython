from helper import *
from flowlib.lib import urequests
import gc,time,_thread
from ucollections import deque
import custbutton as btn
import menu as mnu

connectWiFi()

exchangeRateURL = ''

rates = urequests.get(exchangeRateURL).json()

inrRateRecRate = rates['currencies'][14]['bbImt']
usdRateRecRate = rates['currencies'][0]['bbImt']

inrRateSendRate = rates['currencies'][14]['bsImt']
usdRateSendRate = rates['currencies'][0]['bsImt']

def showRates(**kwargs):
	currency = kwargs['curr']
	tft.clear(tft.BLACK)
	forexMenu.updateButtonText('',"Back")
	tft.font(tft.FONT_DefaultSmall,transparent=True)

	if currency == "USD":
		tft.text(tft.CENTER,tft.CENTER,'USD: Receive: ' + str(usdRateRecRate) + ", Send: " + str(inrRateSendRate),tft.GREEN)
	elif currency == "INR":
		tft.text(tft.CENTER,tft.CENTER,'INR: Receive: ' + str(inrRateRecRate) + ", Send: " + str(inrRateSendRate),tft.GREEN)
	while True:
		if btn.getButtonsState()==btn.BUTTON_A:
			forexMenu.updateButtonText('Next',"Click")
			break



lcd.clear(lcd.BLACK)

forexMenu = mnu.Menu(tft,btn,header='APPS',landscape=True)

forexMenu.addMenuItem('USD',showRates,{'curr':'USD'})
forexMenu.addMenuItem('INR',showRates,{'curr':'INR'})

forexMenu.run()