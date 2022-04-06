#File updated through OTA updates

from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
import time
from time import sleep
import network
import json
import usocket as socket
import urequests
import _thread as th

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
ssid = "Wokwi-GUEST"
password = ""

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect(ssid,password)
    while not sta.isconnected():
        pass
print('Connected to WiFi')
print('network config:', sta.ifconfig())

#Connecting to the mqtt broker
client = MQTTClient(mac_address, CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
client.connect()
PUB_MSG="ESP8266 is Connected and it's mac address is: %s"%mac_address
client.publish(CONFIG["SUBTOPIC"], PUB_MSG)

html='''<!DOCTYPE html>
<html>
<center><h2> Webserver </h2></center>
<form>
<center>
<h3> LED 0 </h3>
<button name="LED0" value='ON' type='submit'>  ON </button>
<button name="LED0" value='OFF' type='submit'> OFF </button>
<h3> LED 1 </h3>
<button name="LED1" value='ON' type='submit'>  ON </button>
<button name="LED1" value='OFF' type='submit'> OFF </button>
<h3> LED 2 </h3>
<button name="LED2" value='ON' type='submit'>  ON </button>
<button name="LED2" value='OFF' type='submit'> OFF </button>
<h3> LED 3 </h3>
<button name="LED3" value='ON' type='submit'>  ON </button>
<button name="LED3" value='OFF' type='submit'> OFF </button>
<h3> LED 4 </h3>
<button name="LED4" value='ON' type='submit'>  ON </button>
<button name="LED4" value='OFF' type='submit'> OFF </button>
<h3> LED 5 </h3>
<button name="LED5" value='ON' type='submit'>  ON </button>
<button name="LED5" value='OFF' type='submit'> OFF </button>
<h3> LED 6 </h3>
<button name="LED6" value='ON' type='submit'>  ON </button>
<button name="LED6" value='OFF' type='submit'> OFF </button>
<h3> LED 7 </h3>
<button name="LED7" value='ON' type='submit'>  ON </button>
<button name="LED7" value='OFF' type='submit'> OFF </button>
<h3>  Restart Device </h3>
<button name="Restart" value='restart' type='submit'> Restart </button>
</center>
'''

def local():
    print('Webserver has been Activated over WLAN')
    print('...........................................')
    # Initialising Socket
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # AF_INET - Internet Socket, SOCK_STREAM - TCP protocol

    Host = '' # Empty means, it will allow all IP address to connect
    Port = 80 # HTTP port
    s.bind((Host,Port)) # Host,Port

    s.listen(5) # It will handle maximum 5 clients at a time
    while True:
      connection_socket,address=s.accept() # Storing Conn_socket & address of new client connected
      print("Got a connection from ", address)
      request=connection_socket.recv(1024) # Storing Response coming from client
      #print("Content ", request) # Printing Response 
      request=str(request) # Coverting Bytes to String
      # Comparing & Finding Postion of word in String 
      LED0_ON =request.find('/?LED0=ON')
      LED0_OFF =request.find('/?LED0=OFF')
      LED1_ON =request.find('/?LED1=ON')
      LED1_OFF =request.find('/?LED1=OFF')
      LED2_ON =request.find('/?LED2=ON')
      LED2_OFF =request.find('/?LED2=OFF')
      LED3_ON =request.find('/?LED3=ON')
      LED3_OFF =request.find('/?LED3=OFF')
      LED4_ON =request.find('/?LED4=ON')
      LED4_OFF =request.find('/?LED4=OFF')
      LED5_ON =request.find('/?LED5=ON')
      LED5_OFF =request.find('/?LED5=OFF')
      LED6_ON =request.find('/?LED6=ON')
      LED6_OFF =request.find('/?LED6=OFF')
      LED7_ON =request.find('/?LED7=ON')
      LED7_OFF =request.find('/?LED7=OFF')
      restart =request.find('/?Restart=restart')

      if(LED0_ON==6):
        led0.value(1)
        
      if(LED0_OFF==6):
        led0.value(0)

      if(LED1_ON==6):
        led1.value(1)
        
      if(LED1_OFF==6):
        led1.value(0)
      
      if(LED2_ON==6):
        led2.value(1)
        
      if(LED2_OFF==6):
        led2.value(0)

      if(LED3_ON==6):
        led3.value(1)
        
      if(LED3_OFF==6):
        led3.value(0)

      if(LED4_ON==6):
        led4.value(1)
        
      if(LED5_OFF==6):
        led5.value(0)
      
      if(LED6_ON==6):
        led6.value(1)
        
      if(LED6_OFF==6):
        led6.value(0)

      if(LED7_ON==6):
        led7.value(1)
        
      if(LED7_OFF==6):
        led7.value(0)
        
      if(restart==6):
          deep_sleep(2000)            
        
      # Sending HTML document in response everytime to all connected clients  
      response=html 
      connection_socket.send(response)
      
      #Closing the socket
      connection_socket.close()
  

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
                        client.publish(CONFIG["SUBTOPIC"],"Rebooting Device...")
                        sleep(2)
                        deep_sleep(2000)
                        
                        
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
    print("Device is Connected to %s and subscribed to %s topic over MQTT protocol" % (CONFIG['MQTT_BROKER'], CONFIG["PUBTOPIC"]))   

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

th.start_new_thread(local, ())
th.start_new_thread(Listen, ())
