#File has been updated through OTA updates

import _thread as th
import socket
from umqtt.simple import MQTTClient
from machine import Pin,Timer

import ubinascii
import time
import network
import json
from machine import Timer
dictn={}
global led1
led0 = Pin(23, Pin.OUT)
led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(19, Pin.OUT)
led4 = Pin(5, Pin.OUT)
led5 = Pin(4, Pin.OUT)
led6 = Pin(18, Pin.OUT)
led7 = Pin(2, Pin.OUT)

'''
#wifi crendentials
ssid = "Pranay"
password = "Pranay21"

#connects to the wifi network
sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect(ssid,password)
    while not sta.isconnected():
        pass

print('network config:', sta.ifconfig())
'''

#Mac Address of the chip
macaddress= ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(macaddress)
#configuration to connect to the mqtt broker
CONFIG = {
     "MQTT_BROKER": "14.97.22.54",
     "USER": "admin",
     "PASSWORD": "password",
     "PORT": 1883, 
     "PUBTOPIC": b"ESPPUB",
     "SUBTOPIC": b"ESPSUB",   
}

def deep_sleep(msecs):
    rtc = machine.RTC()  # configure RTC.ALARM0 to be able to wake the device
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs) # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    machine.deepsleep()
    
def task1():
    try:
        if led1.value()==1:
            print("Thread started")
            print("LED 3 ON")
            led3.on()
            time.sleep(5)
            led3.off()
            print("LED 3 OFF")
            dictn[lst[3]]='0'
            print("Thread closed")
    except:
        print("error in multitask")
        
def task2():
    try:
        if led7.value()==1:
            print("Thread started")
            print("LED 5 ON")
            led5.on()
            time.sleep(5)
            print("LED 5 OFF")
            led5.off()
            dictn[lst[5]]='0'
            time.sleep(5)
            print("LED 7 OFF")
            led7.off()
            dictn[lst[3]]='0'
            print("Thread closed")
    except:
        print("error in multitask")
        

#Act based on received command & publish status of respective LED
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
   
    #take the json message and convert into dictionary
    print(type(msg))
    
    while True:
        try:
            msgjsn=json.loads(msg)
            print(msgjsn)
            
           
            for i in msgjsn.items():
                for j in range(len(lst)):
                    if '1' in i and lst[j] in i:
                        gpiolist[j].on()
                        dictn[lst[j]]='1'
                        th.start_new_thread(task1,())
                        th.start_new_thread(task2,())   
                        #if led 1 is on then after 5s led 2 will be off
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
            
          
def connect_and_subscribe():
    #instance of MQTTClient
    
    client = MQTTClient(macaddress, CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
    client.connect()
    PUB_MSG="ESP8266 is Connected and it's mac address is: %s"%macaddress
    client.publish(CONFIG["SUBTOPIC"], PUB_MSG)
    client.set_callback(onMessage)
    client.subscribe(CONFIG["PUBTOPIC"])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG["PUBTOPIC"]))
    return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(2)
  machine.reset()
  
def listen(client):
    try:
        while True:
            #msg = client.wait_msg()
            msg = (client.check_msg())
    except OSError as e:
        restart_and_reconnect()
              
                    
    finally:
            client.disconnect()
          
def web_page():
  if led1.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html =  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button {
background-color: #4CAF50;
border: 2px solid #4CAF50;;
color: white;
padding: 15px 32px;
text-align: center;
text-decoration: none;
display: inline-block;
font-size: 16px;
margin: 4px 2px;
cursor: pointer;
}</style></head><body> <h1>ESP32 Web Server</h1> 
 <center>
<a href="/?led0=on"><button class="button">LED0 ON</button></a> 
<a href="/?led0=off"><button class="button button2">LED0 OFF</button></a> <br><br>
<a href="/?led1=on"><button class="button">LED1 ON</button></a> 
<a href="/?led1=off"><button class="button button2">LED1 OFF</button></a> <br><br> 

</center></body></html>"""
  return html
def webserver():
    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led0_on = request.find('/?led0=on')
        led0_off = request.find('/?led0=off')
        led1_on = request.find('/?led1=on')
        led1_off = request.find('/?led1=off')
        if led0_on == 6:
            print('LED ON')
            led0.value(1)
            
        elif led0_off == 6:
            print('LED OFF')
            led0.value(0)
            
        elif led1_on == 6:
            print('LED ON')
            led1.value(1)
            
        elif led1_off == 6:
            print('LED OFF')
            led1.value(0)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

#Connecting to the mqtt broker

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
        

try:
    client = connect_and_subscribe()
            
except OSError as e:
    print('Failed to connect to MQTT broker. Reconnecting...')
            
            

#Lists
lst=['L0','L1','L2','L3','L4','L5','L6','L7', 'L8']
gpiolist =[led0, led1, led2, led3, led4, led5, led6, led7]


#publish initial state data
for j in range(0,8):
    if gpiolist[j].value() == 1:
        dictn[lst[j]]='1'
    if gpiolist[j].value() == 0:
        dictn[lst[j]]='0'
#after completing the loop the initial data is stored in dictionary and it is converted to json data to publish
print(dictn)
message=json.dumps(dictn)
client.publish(CONFIG["SUBTOPIC"], message)
th.start_new_thread(webserver,())
th.start_new_thread(listen(client))
