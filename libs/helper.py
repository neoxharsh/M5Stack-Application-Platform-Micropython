try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

import machine,utime,ujson,network
from m5stack import *
from flowlib.hw.bm8563 import Bm8563
tft = lcd

rtc = Bm8563()

BATTERY_LANDSCAPE =  0
BATTERY_POTRAIT = 1


def connectWiFi(ssid=None,password=None,showProgress=False):
    if showProgress:
        tft.font(tft.FONT_DefaultSmall,transparent=True)
        tft.clear(tft.BLACK)
        tft.text(tft.CENTER,tft.CENTER,"Connecting to WiFi: " + WIFI['ssid'],tft.GREEN)
    wifiSta = network.WLAN(network.STA_IF)
    wifiSta.active(True)
    print("\n=== Activate STA ===\n")
    if ssid is not None:
        wifiSta.connect(ssid,password)
        if showProgress:
            tft.clear(tft.BLACK)
            tft.text(tft.CENTER,tft.CENTER,"Connected to WiFi: " + WIFI['ssid'],tft.GREEN)
        return wifiSta
    else:
        if machine.nvs_getstr('wifissid') is None:
            from wifiConfig import setupWifi
            setupWifi()
        else:
            wifiSta.connect(machine.nvs_getstr('wifissid'),machine.nvs_getstr('wifipassword'))
            while not wifiSta.isconnected():
                utime.sleep_ms(100)
            print(wifiSta.ifconfig())
            if showProgress:
                tft.clear(tft.BLACK)
                tft.text(tft.CENTER,tft.CENTER,"Connected to WiFi: " + WIFI['ssid'],tft.GREEN)
            return wifiSta

currentBrightness = 2.5

def readConfig(file):
    with open('config.cfg','r') as configFile:
        config = ujson.load(configFile)
    return config

def dumpConfig(config,file):
    _cfg = open('config.cfg','w')
    ujson.dump(config,_cfg)
    _cfg.flush()
    _cfg.close()

def setPara(key,value):
    params = machine.nvs_getstr('params')
    if params == None:
        machine.nvs_setstr('params','')
        params = machine.nvs_getstr('params')
    if str(key) not in params:
        params += ","+str(key)
        machine.nvs_setstr('params',params)
    machine.nvs_setstr(str(key),str(value))

def getAllPara(par=None):
    params = machine.nvs_getstr('params')
    if params == None:
        machine.nvs_setstr('params','')
    if par == None:
        return machine.nvs_getstr('params')
    else:
        if machine.nvs_getstr(par) is not None:
            return machine.nvs_getstr(par).split(',')
        else:
            return ''.split(',')

def erasePara():
    machine.nvs_erase_all()

def updateTime(sync=False,host = "pool.ntp.org",TIME_DIFF=[0,0]):
    tDiff = (TIME_DIFF[0] * 3600) + (TIME_DIFF[1]*60)
    if sync:
        NTP_DELTA = 3155673600
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        t = val - NTP_DELTA
        print(t)
        tm = utime.localtime(t)
        rtc.setTime(tm[0],tm[1],tm[2],tm[3],tm[4],tm[5])
        tm = utime.localtime(t + tDiff)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)
    else:
        now = rtc.now()
        _t = utime.mktime((now[0],now[1],now[2],now[3],now[4],now[5],0,0))
        tm = utime.localtime( _t + tDiff)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)



def map(x, in_min,in_max,out_min,out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def drawBattery(x,y,orient=0):
    lcd.rect(x,y,22,7,0x000000,0x000000)
    if orient is 0:
        lcd.rect(x,y,20,7,0xFF0000)
        lcd.rect(x+20,y+1,4,5,0xFF0000,0xFF0000)
        if not axp.isCharge():
            pass
        currentBat = int(map(axp.getBatVol(),2500,3760,2,19))
        lcd.rect(x+1,y+1,currentBat,5,0x00FF00,0x00FF00)

def removeDir(dir):
    import os
    for x in os.listdir(dir):
        os.remove(dir+'/'+x)
    os.rmdir(dir)

def modifyBit( n,  p,  b): 
    mask = 1 << p 
    return (n & ~mask) | ((b << p) & mask)

def drawHeader(text,headerBar,bgColor=None,txtColor=None,isBold=False):
    tft.setwin(headerBar[0],headerBar[1],headerBar[2],headerBar[3])
    tft.font(tft.FONT_DefaultSmall,transparent=True)
    if isBold:
        tft.font(tft.FONT_DejaVu18,transparent=True)
    if bgColor is not None:
        tft.clearwin(bgColor)
    else:
        tft.clearwin(tft.RED)
    if txtColor is not None:
        tft.text(5,4,str(text),txtColor)
    else:
        tft.text(5,4,str(text),tft.BLACK)
    tft.resetwin()

def drawButton(A,B,buttonBar,bgColor=None,txtColor=None,isBold=False):
    tft.setwin(buttonBar[0],buttonBar[1],buttonBar[2],buttonBar[3])
    if isBold:
        tft.font(tft.FONT_Ubuntu,transparent=True)
    if bgColor is not None:
        tft.clearwin(bgColor)
    else:
        tft.clearwin(tft.RED)
    if txtColor is not None:
        tft.text(5,4,A,txtColor)
        tft.text(tft.RIGHT,4,B,txtColor)
    else:
        tft.text(5,4,A,tft.BLACK)
        tft.text(tft.RIGHT,4,B,tft.BLACK)
    tft.resetwin()

def rgbToInt(r, g, b):
  return int(r << 16 | g << 8 | b)


def changeBrightness():
    global currentBrightness
    if currentBrightness > 3.3:
        currentBrightness = 2.5
        axp.setLDO2Vol(currentBrightness)
    else:
        currentBrightness += .1
        axp.setLDO2Vol(currentBrightness)
