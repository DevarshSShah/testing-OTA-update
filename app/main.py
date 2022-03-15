#Updated Code for rebooting device using MQTT
#testing if code has been updated or not
#Test1234

from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
import time
from time import sleep
import network
import json

dictn={}
led0 = Pin(15, Pin.OUT)
led1 = Pin(5, Pin.OUT)
led2 = Pin(4, Pin.OUT)
led3 = Pin(0, Pin.OUT)
led4 = Pin(14, Pin.OUT)
led5 = Pin(12, Pin.OUT)
led6 = Pin(13, Pin.OUT)
led7 = Pin(2, Pin.OUT)

#mac address of the chip
mac_address= ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

#configuration to connect to the mqtt broker
CONFIG = {
     "MQTT_BROKER": "14.97.22.54",
     "USER": "admin",
     "PASSWORD": "password",
     "PORT": 1883, 
     "PUBTOPIC": b"esppub",
     "SUBTOPIC": b"espsub",   
}

#wifi
ssid = "Devarsh"
password = "Shital@9825569091"

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect(ssid,password)
    while not sta.isconnected():
        pass
print('Connected to WiFi')
print('network config:', sta.ifconfig())
print('Your code has been updated succesfully')

#Connecting to the mqtt broker
client = MQTTClient(mac_address, CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
client.connect()
PUB_MSG="ESP8266 is Connected and it's mac address is: %s"%mac_address
client.publish(CONFIG["SUBTOPIC"], PUB_MSG)

#reboot
def deep_sleep(msecs):
    rtc = machine.RTC()  # configure RTC.ALARM0 to be able to wake the device
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs) # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    machine.deepsleep()
    

#Act based on received command & publish status of respective LED
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
    #take the json message and convert into dictionary
    print(type(msg))
    while True:
        try:
            msgjsn=json.loads(msg)
            for i in msgjsn.items():
                for j in range(len(lst)):
                    if '1' in i and lst[j] in i:
                        gpiolist[j].on()
                        dictn[lst[j]]='1'
                    elif '0' in i and lst[j] in i:
                        gpiolist[j].off()
                        dictn[lst[j]]='0'
                    elif "2" in i and lst[j] in i:
                        print("Rebooting device...")
                        client.publish(CONFIG["SUBTOPIC"],"Rebooting Device")
                        sleep(2)
                        deep_sleep(5000)
                        
                        
#dictionary is converted to json data             
            message=json.dumps(dictn)
            client.publish(CONFIG["SUBTOPIC"],message)
            break
#If there is invalid json syntax is entered then exception raised and take another input of valid json syntax           
        except :
            print("Error Raised Invalid Json...")
            print("Please enter valid json format")
            break
            
def Listen():
    #instance of MQTTClient
    
    client.set_callback(onMessage)
    client.subscribe(CONFIG["PUBTOPIC"])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG["PUBTOPIC"]))
   

    try:
        while True:
            #msg = client.wait_msg()
            msg = (client.check_msg())          
    finally:
            client.disconnect()

#Lists
lst=['L0','L1','L2','L3','L4','L5','L6','L7','L8']
gpiolist =[led0, led1, led2, led3, led4, led5, led6, led7]

#publish initial state data
for j in range(0,8):
    if gpiolist[j].value() == 1:
        dictn[lst[j]]='1'
    if gpiolist[j].value() == 0:
        dictn[lst[j]]='0'
#after completing the loop the initial data is stored in dictionary and it is converted to json data to publish       
message=json.dumps(dictn)
client.publish(CONFIG["SUBTOPIC"], message)

Listen()
