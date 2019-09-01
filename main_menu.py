import helper as hp
import menu as mnu
from m5stack import *
import custbutton as btn
import os,re,time,ujson,machine

config = {}
with open('config.cfg','r') as configFile:
	config = ujson.load(configFile)

regex = r'(\D+[^\s][a-z]\w+)'


def runProgram(**kwarg):
	global config
	if len(kwarg) is not 0:
		folderName = kwarg['folderName']
	if 'main.py' in os.listdir('apps/'+folderName):
		config['apps']['defaultApp'] = folderName
		with open('config.cfg','w') as configFile:
			ujson.dump(config,configFile)
		hp.tft.clear(hp.tft.BLACK)
		hp.tft.text(hp.tft.CENTER,hp.tft.CENTER,"Launching..",hp.tft.GREEN)
		time.sleep(1)
		hp.tft.clear(hp.tft.BLACK)
		machine.reset()
	else:
		hp.tft.setwin(menuBody[0],menuBody[1],menuBody[2],menuBody[3])
		hp.tft.clearwin(hp.tft.BLACK)
		hp.tft.text(hp.tft.CENTER,hp.tft.CENTER,'main.py not found',hp.tft.GREEN)
		time.sleep(1)
		hp.tft.resetwin()
		return 1




allAppsName = {str(id):{'itemName':re.search(regex,x).group(0).lstrip(' '),'methodName':runProgram,'args':{'folderName':x}} for id,x in enumerate(os.listdir('apps'))}

appMenu = mnu.Menu(hp.tft,btn,header='APPS',items=allAppsName,landscape=True)

menuBody = appMenu.getMenuBodyDimension()
appMenu.run()