import struct,usocket,ujson

class SmartDevice(object):

	def __init__(self,add):
		self.add = add
		self.INITIALIZATION_VECTOR = 171

	def encrypt(self,request):
  
	    key = self.INITIALIZATION_VECTOR

	    plainbytes = request.encode()
	    buffer = bytearray(struct.pack(">I", len(plainbytes)))

	    for plainbyte in plainbytes:
	        cipherbyte = key ^ plainbyte
	        key = cipherbyte
	        buffer.append(cipherbyte)

	    return bytes(buffer)


	def decrypt(self, ciphertext):
	    key = self.INITIALIZATION_VECTOR
	    buffer = []

	    for cipherbyte in ciphertext:
	        plainbyte = key ^ cipherbyte
	        key = cipherbyte
	        buffer.append(plainbyte)

	    plaintext = bytes(buffer)

	    return plaintext.decode()

	def send(self,query):
		sock = usocket.socket(2,1,0)
		buffer = bytes()
		try:
			sock.connect((self.add,9999))
			sock.send(self.encrypt(ujson.dumps(query)))
			length = -1
			while True:
				chunk = sock.recv(4096)
				if length == -1:
					length = struct.unpack(">I", chunk[0:4])[0]
				buffer += chunk
				if (length > 0 and len(buffer) >= length + 4) or not chunk:
					break
		except Exception:
			print('Exception occured')
			return None

		try:
			sock.close()
		except Exception as e:
			pass
		return ujson.loads(self.decrypt(buffer[4:]))
		

class SmartBulb:

	def __init__(self,add):
		self.LIGHT_SERVICE = "smartlife.iot.smartbulb.lightingservice"
		self.device = SmartDevice(add)
		self.deviceState = self.get_state()


	def turn_on(self):
		if not self.isOn():
			req = {self.LIGHT_SERVICE: {"transition_light_state": {"on_off": 1}}}
			res = self.device.send(req)

	def turn_off(self):
		if self.isOn():
			req = {self.LIGHT_SERVICE: {"transition_light_state": {"on_off": 0}}}
			res = self.device.send(req)

	def get_state(self):
		req = {self.LIGHT_SERVICE: {"get_light_state": None}}
		res = self.device.send(req)
		return res

	def isOn(self):
		try:
			_state = self.get_state()[self.LIGHT_SERVICE]['get_light_state']['on_off']
			if _state:
				return True
			else:
				return False
		except Exception as e:
			return None
		

	def toggle(self):
		try:
			_state = self.get_state()[self.LIGHT_SERVICE]['get_light_state']['on_off']
			if not _state:
				self.turn_on()
				return 1
			else:
				self.turn_off()
				return 0
		except Exception as e:
			return None
	


class SmartPlug:
	pass