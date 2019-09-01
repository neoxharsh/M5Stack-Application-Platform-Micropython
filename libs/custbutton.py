import machine, time

BUTTON_A = 1
BUTTON_B = 2
BUTTON_AB = 4
BUTTON_AL = 7
BUTTON_BL = 8
BUTTON_AD = 10
BUTTON_BD = 11

class Button(object):
	"""docstring for Button"""
	def __init__(self,pin):
		super(Button, self).__init__()
		self.pin = machine.Pin(pin,machine.Pin.IN)
		self.activeHigh = 0
		self.btnState = not self.activeHigh
		self.lastState = self.btnState
		self.clickCount = 0
		self.clicks = 0
		self.depressed = False
		self.lastBounceTime = 0
		self.debounceTime = 30
		self.multiClickTime = 250
		self.longClickTime = 1300
		self.change = False
		self.longClicked= False

	def update(self):
		now = time.ticks_ms()
		self.btnState = self.pin.value()
		if not self.activeHigh:
			self.btnState =  not self.btnState

		if self.btnState is not self.lastState:
			self.lastBounceTime = now

		if now - self.lastBounceTime > self.debounceTime and self.btnState is not self.depressed:
			self.depressed = self.btnState
			if self.depressed:
				self.clickCount += 1

		if self.lastState == self.btnState:
			self.change = False

		self.lastState = self.btnState

		if not self.depressed and (now - self.lastBounceTime) > self.multiClickTime:
			self.clicks = self.clickCount
			self.clickCount = 0
			if self.clicks is not 0:
				self.change = True

		if self.depressed and (now - self.lastBounceTime > self.longClickTime):
			self.clicks = 0 - self.clickCount
			self.clickCount = 0
			if self.clicks is not 0:
				self.change = True
		return self.clicks

	def getValue(self):
		return  not self.pin.value()

buttonA = Button(37)
buttonB = Button(39)

def getButtonsState():
	if (buttonA.getValue() and buttonB.getValue()):
		time.sleep(0.2)
		return BUTTON_AB

	a = buttonA.update()
	b = buttonB.update()
	if (a==1):
		return BUTTON_A
	if (b==1):
		return BUTTON_B
	if (a==2):
		return BUTTON_AD
	if (b==2):
		return BUTTON_BD	
	if (a==-1):
		return BUTTON_AL
	if (b==-1):
		return BUTTON_BL
	return None
