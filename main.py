import network, ntptime, time # type: ignore
from machine import Pin # type: ignore


def blinker(amount):
    count = 0
    while amount > count:
        count += 1
        ledRunner(.1, 16)
        for _ in range(count):
            ledRunner(.1, 2)


def ledRunner(t, pin):
    led = Pin(pin, Pin.OUT)
    led.value(0)
    time.sleep(t)
    led.value(1)
    time.sleep(t)


def connectWifi(ssid, password):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
        ntptime.settime()
        return True
    except Exception as e:
        print(e)
        return False

def createAP(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
        pass
    blinker(4)
    ledRunner(2, 16)

