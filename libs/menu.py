import time
import custbutton as btn

class Menu(object):
	def __init__(self, tft,btn,header='',items=None,landscape=False,isReset=False,isExit=False,isBold=False,font=None):
		super(Menu, self).__init__()
		self.tft = tft
		self.btn = btn
		if landscape:
			self.tft.orient(1)
			self.width,self.height = self.tft.screensize()
			self.headerBar = [0                 ,0                    ,self.width  ,int(0.2 * self.height)   ,self.tft.BLUE    ,self.tft.WHITE]
			self.menuBody =  [self.headerBar[0] ,self.headerBar[3]+5  ,self.width  ,int(self.headerBar[3] + .6 * self.height)                ,self.tft.BLACK  ,self.tft.GREEN]
			self.buttonBar = [self.menuBody[0]  ,self.menuBody[3]     ,self.width  ,int(self.menuBody[3] + 0.2 * self.height),self.tft.BLUE    ,self.tft.WHITE]
		else:
			self.tft.orient(0)
			self.width,self.height = self.tft.screensize()
			self.headerBar = [0                 ,0                    ,self.width  ,int(0.1 * self.height)   ,self.tft.BLUE    ,self.tft.WHITE]
			self.menuBody =  [self.headerBar[0] ,self.headerBar[3]+5  ,self.width  ,int(self.headerBar[3] + .8 * self.height)                ,self.tft.BLACK  ,self.tft.GREEN]
			self.buttonBar = [self.menuBody[0]  ,self.menuBody[3]     ,self.width  ,int(self.menuBody[3] + 0.1 * self.height),self.tft.BLUE    ,self.tft.WHITE]
		

		if items is not None:
			self.items = items
		else:
			self.items= {}
		self.totalItems = len(self.items)
		self.itemNames = [self.items[str(x)]['itemName'] for x in range(0,self.totalItems)]
		self.itemGroupSize = 2
		self.itemGroup = [self.itemNames[x:x+self.itemGroupSize] for x in range (0,len(self.itemNames),self.itemGroupSize)]
		self.currentCursor = 0
		self.previousCursor = 0
		self.currentItemPage = None
		self.isReset = isReset
		self.isExit = isExit
		self.buttonAText = 'Next'
		self.buttonBText = 'Click'
		self.headerText = header
		self.tft.font(self.tft.FONT_DefaultSmall,transparent=True)
		if isBold:
			self.menuItemBold = True
			self.buttonTextBold = True
			self.headerTextBold = True
		else:
			self.menuItemBold = False
			self.buttonTextBold = False
			self.headerTextBold = False
		self.updateHeader(self.headerText)
		self.updateButtonText(self.buttonAText,self.buttonBText)

	def addMenuItem(self,itemName,methodName,args=()):
		self.items.update({str(self.totalItems):{'itemName':itemName,'methodName':methodName,'args':args}})
		self.totalItems += 1
		self.itemNames = [self.items[str(x)]['itemName'] for x in range(0,self.totalItems)]
		self.itemGroup = [self.itemNames[x:x+self.itemGroupSize] for x in range (0,len(self.itemNames),self.itemGroupSize)]
	
	def updateMenuItemByID(self,id,itemName=None,methodName=None,args=None):
		if itemName is not None:
			self.items[str(id)]['itemName'] = itemName
		if methodName is not None:
			self.items[str(id)]['methodName'] = methodName
		if args is not None:
			self.items[str(id)]['args'] = args
		self.itemNames = [self.items[str(x)]['itemName'] for x in range(0,self.totalItems)]
		self.itemGroup = [self.itemNames[x:x+self.itemGroupSize] for x in range (0,len(self.itemNames),self.itemGroupSize)]

	def updateMenuItemByName(self,name,itemName=None,methodName=None,args=None):
		_itemNametoID = {y['itemName']:x for x,y in self.items.items()}
		if itemName is not None:
			self.items[str(_itemNametoID[name])]['itemName'] = itemName
		if methodName is not None:
			self.items[str(_itemNametoID[name])]['methodName'] = methodName
		if args is not None:
			self.items[str(_itemNametoID[name])]['args'] = args
		self.itemNames = [self.items[str(x)]['itemName'] for x in range(0,self.totalItems)]
		self.itemGroup = [self.itemNames[x:x+self.itemGroupSize] for x in range (0,len(self.itemNames),self.itemGroupSize)]

	def updateHeader(self,text=None,bgColor=None,txtColor=None,isBold=False):
		if text is not None:
			self.headerText = str(text)
		self.tft.setwin(self.headerBar[0],self.headerBar[1],self.headerBar[2],self.headerBar[3])
		if isBold or self.headerTextBold:
			self.tft.font(self.tft.FONT_Default,transparent=True)
			self.headerTextBold = True
		else:
			self.tft.font(self.tft.FONT_DefaultSmall,transparent=True)
			self.headerTextBold = False
		if bgColor is not None:
			self.headerBar[4] = bgColor
		if txtColor is not None:
			self.headerBar[5] = txtColor
		self.tft.clearwin(self.headerBar[4])
		self.tft.text(5,4,self.headerText,self.headerBar[5])
		self.tft.resetwin()

	def updateButtonText(self,A=None,B=None,bgColor=None,txtColor=None,isBold=False):
		if isBold or self.buttonTextBold:
			self.tft.font(self.tft.FONT_Default,transparent=True)
			self.buttonTextBold = True
		else:
			self.tft.font(self.tft.FONT_DefaultSmall,transparent=True)
			self.buttonTextBold = False
		if A is not None:
			self.buttonAText = A
		if B is not None:
			self.buttonBText = B
		self.tft.setwin(self.buttonBar[0],self.buttonBar[1],self.buttonBar[2],self.buttonBar[3])
		if bgColor is not None:
			self.buttonBar[4] = bgColor
		if txtColor is not None:
			self.buttonBar[5] = txtColor
		self.tft.clearwin(self.buttonBar[4])
		self.tft.text(5,4,self.buttonAText,self.buttonBar[5])
		self.tft.text(self.tft.RIGHT,4,self.buttonBText,self.buttonBar[5])
		self.tft.resetwin()

	def updateBodyColor(self,bgColor=None,txtColor=None):
		if bgColor is not None:
			self.menuBody[4] = bgColor
		if txtColor is not None:
			self.menuBody[5] = txtColor

	def drawMenuItems(self,items,isBold=False):
		if isBold or self.menuItemBold:
			self.tft.font(self.tft.FONT_Default,transparent=True)
			self.menuItemBold = True
		else:
			self.tft.font(self.tft.FONT_DefaultSmall,transparent=True)
			self.menuItemBold = False
		self.tft.setwin(self.menuBody[0],self.menuBody[1],self.menuBody[2],self.menuBody[3])
		self.tft.clearwin(self.menuBody[4])
		index = 0
		for item in items:
			self.tft.text(5,index*20,item[:19],self.menuBody[5])
			index+=1
		self.tft.resetwin()

	def selectItem(self,id):
		if self.totalItems > 0:
			itemPage = int(id/self.itemGroupSize)
			if itemPage is not self.currentItemPage:
				self.drawMenuItems(self.itemGroup[itemPage])
				self.currentItemPage = itemPage
				self.tft.setwin(self.menuBody[0],self.menuBody[1],self.menuBody[2],self.menuBody[3])
				_internItemId = id - itemPage * self.itemGroupSize
				selectedApp = self.itemGroup[itemPage][_internItemId]
				print(str(id))
				self.tft.text(5, _internItemId * 20,selectedApp[:19] + " <--",self.menuBody[5])
				self.previousCursor = id
				self.tft.resetwin()
			else:
				self.tft.setwin(self.menuBody[0],self.menuBody[1],self.menuBody[2],self.menuBody[3])
				if self.previousCursor is not id:
					_internItemId = self.previousCursor - itemPage * self.itemGroupSize
					selectedApp = self.itemGroup[itemPage][_internItemId]
					self.tft.text(5, _internItemId * 20 ,selectedApp[:19] + " <--",self.tft.BLACK)
					self.tft.text(5, _internItemId * 20,selectedApp[:19],self.menuBody[5])
					self.previousCursor = id
				_internItemId = id - itemPage * self.itemGroupSize
				selectedApp = self.itemGroup[itemPage][_internItemId]
				self.tft.text(5, _internItemId * 20,selectedApp[:19] + " <--",self.menuBody[5])
				self.tft.resetwin()

	def getMenuBodyDimension(self):
		return self.menuBody

	def getHeaderBarDimension(self):
		return self.headerBar

	def getButtonBarDimension(self):
		return self.buttonBar

	def run(self):
		self.selectItem(0)
		time.sleep(1)
		while True:
			_buttonCurrentState = self.btn.getButtonsState()
			if _buttonCurrentState==self.btn.BUTTON_BD:
				if (self.currentCursor >0):
					self.currentCursor -= 1
					self.selectItem(self.currentCursor)
				time.sleep(.3)
			if _buttonCurrentState==self.btn.BUTTON_B:
				if (self.currentCursor<len(self.items)-1):
					self.currentCursor += 1
					self.selectItem(self.currentCursor)
				time.sleep(.3)
			elif _buttonCurrentState==self.btn.BUTTON_A:
				if not callable(self.items[str(self.currentCursor)]['methodName']):
					self.tft.setwin(self.menuBody[0],self.menuBody[1],self.menuBody[2],self.menuBody[3])
					self.tft.clearwin(self.tft.BLACK)
					self.tft.text(self.tft.CENTER,self.tft.CENTER,'Nothing to Run',self.tft.RED)
					self.tft.resetwin()
					time.sleep(1)
				else:
					if len(self.items[str(self.currentCursor)]['args'])==0:
						res = self.items[str(self.currentCursor)]['methodName']()
						if res:
							break
						self.tft.resetwin()
						self.currentItemPage = None
						self.selectItem(self.currentCursor)
						self.updateHeader()
						self.updateButtonText()
					else:
						self.items[str(self.currentCursor)]['methodName'](**self.items[str(self.currentCursor)]['args'])
						self.tft.resetwin()
						self.currentItemPage = None
						self.selectItem(self.currentCursor)
						self.updateHeader()
						self.updateButtonText()
				time.sleep(.5)
				self.selectItem(self.currentCursor)