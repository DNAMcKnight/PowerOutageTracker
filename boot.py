# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine # type: ignore
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()
import main
import powerOutage as po
from time import sleep, localtime
import network, json # type: ignore

main.ledRunner(1, 16)
with open("settings.json", "r") as f:
    settings = json.load(f)
    ssid = settings['wifi'][0]['ssid']
    password = settings['wifi'][0]['password']
    
wifi = main.connectWifi(ssid, password)

#createAP("ESP8266","123456789")
while not wifi:
    print(".")
    
po.timeSaver()

