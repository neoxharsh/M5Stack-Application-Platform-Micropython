from helper import *
from microWebSrv import MicroWebSrv
import network,gc,machine,time

gc.collect()

WIFI_SSID= 'wifissid'
WIFI_PASSWORD = 'wifipassword'

wifiSta = ''

def setupWifi(threaded=False):
	global wifiSta
	sta = network.WLAN(network.STA_IF)
	sta.active(True)
	wifiSta = network.WLAN(network.AP_IF)
	wifiSta.active(True)
	wifiSta.config(essid='M5Stack WiFi Config')
	mws = MicroWebSrv(bindIP='192.168.4.1',webPath='/flash/apps') # TCP port 80 and files in /flash/www
	mws.Start(threaded)         # Starts server in a new thread
	lcd.orient(1)
	lcd.font(lcd.FONT_DefaultSmall)
	lcd.clear(lcd.BLACK)
	lcd.text(lcd.CENTER,lcd.CENTER,'192.168.4.1')



@MicroWebSrv.route('/submit',"GET")
def handlerFuncSubmit(httpClient, httpResponse) :
	content = '''
  <!DOCTYPE html>
<html>
<style>
body
{
  padding: 30px;
  background-color: #fcfcfc;
}
.center-div
{
text-align: center;
  margin: 0 auto;
  max-width: 400px;
  height: 210px;
  background-color: #ddd;
  border-radius: 3px;
}
</style>
<body>
<div class="center-div">
<h2 >Connecting</h2>
</div>
</body>
</html>
'''
	_wifiData = httpClient.GetRequestQueryParams()
	machine.nvs_setstr(WIFI_SSID,_wifiData['SSID'])
	machine.nvs_setstr(WIFI_PASSWORD,_wifiData['Password'])
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )
	time.sleep(2)
	machine.reset()

@MicroWebSrv.route('/','GET')
def handlerFuncRoot(httpClient, httpResponse) :
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = generatePage() )


@MicroWebSrv.route('/scan','GET')
def handlerFuncRoot(httpClient, httpResponse) :
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = generatePage() )


def generatePage():
	content = '''
<!DOCTYPE html>
<html>
<head>
	<title>M5Stack WiFi Config</title>
</head>
<style>
body
{
  padding: 30px;
  background-color: #fcfcfc;
}
.center-div
{
text-align: center;
  margin: 0 auto;
  max-width: 400px;
  height: 210px;
  background-color: #ddd;
  border-radius: 3px;
}
.center-div p
{

}
</style>
<body>
<div class="center-div">
<h2 >WiFi Config</h2>
<p >Select Access Point from Drop down list:</p>

<form action="/submit" method="GET" >
SSID<br>
  <select name="SSID" >
	'''


# <option value="volvo">Volvo</option>

	_ssid = wifiSta.scan()

	for x in _ssid:
		_x = x[0].decode('UTF-8')
		content += '<option value="'+ _x +'">' + _x + '</option>'

	content += '''

 </select>
  <br>Password<br>
  <input name="Password" type="password">
  <br><br>
  <input type="submit">
  <button action="/scan">Scan</button>
</form>

</div>
</body>
</html>


'''
	return content