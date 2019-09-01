import ujson,machine,gc,uuid
import custreq as requests

tokenKey = 'tplinktokenkey'

class TpLinkCloud(object):
	"""docstring for TpLinkCloud"""
	def __init__(self,username,password):
		super(TpLinkCloud, self).__init__()
		self.username = username
		self.password = password
		self.isTokenPresent = False
		self.token = ''
		self.tokenKey = 'tplinktokenkey'
		self.getToken()
	
	def sendData(self,url,payload):
		try:
			payload = ujson.dumps(payload).encode('utf-8')
			gc.collect()
			return requests.post(url+'?token={}'.format(self.token),data=payload)
		except Exception as e:
			gc.collect()
			return None
		

	def getToken(self,newToken=False):
		try:
			if machine.nvs_getstr(self.tokenKey) is None or newToken:
				print("Getting a New Token")
				payload = {
				"method": "login",
				"params":
				{
				"appType": "Kasa_Android",
				"cloudUserName":self.username,
				"cloudPassword":self.password,
				"terminalUUID": str(uuid.uuid4())
				}
				}
				_token = requests.post('https://wap.tplinkcloud.com/',json=payload).json()['result']['token']
				machine.nvs_setstr(self.tokenKey,_token)
				self.isTokenPresent = True
				self.token = _token
				return _token
			else:
				print("Using Stored Token")
				_token =  machine.nvs_getstr(self.tokenKey)
				self.isTokenPresent = True
				self.token = _token
				return machine.nvs_setstr(self.tokenKey,_token)
		except Exception as e:
			print(e)
		
	def getDeviceList(self):
		if self.token is not None:
			data = {"method":"getDeviceList"}
			return self.sendData('https://wap.tplinkcloud.com/',data).json()['result']['deviceList']

class TPLinkSmartBulb(TpLinkCloud):
	"""docstring for TPLinkSmartBulb"""
	def __init__(self,device:dict, username='',password=''):
		super(TPLinkSmartBulb, self).__init__(username,password)
		self.deviceId = device['deviceID']
		self.appURL = device['url']
		self.state = True
		
	def generatePayload(self,payload):
		return {"method":"passthrough",
		"params":{
		"deviceId":self.deviceId,
		"requestData":ujson.dumps(payload)
		}}
	def turnOn(self):
		bulb_command = {
		"smartlife.iot.smartbulb.lightingservice":
		{
		"transition_light_state":
		{
		"on_off": 1
		}
		}
		}
		self.sendData(self.appURL,self.generatePayload(bulb_command))

	def turnOff(self):
		bulb_command = {
		"smartlife.iot.smartbulb.lightingservice":
		{
		"transition_light_state":
		{
		"on_off": 0
		}
		}
		}
		self.sendData(self.appURL,self.generatePayload(bulb_command))

	def getState(self):
		bulb_command = {
		"smartlife.iot.smartbulb.lightingservice":
		{
		"get_light_state":""
		}
		}
		return self.sendData(self.appURL,self.generatePayload(bulb_command)).json()

	def toggle(self):
		if self.state:
			self.turnOff()
			self.state = not self.state
		else:
			self.turnOn()
			self.state = not self.state

