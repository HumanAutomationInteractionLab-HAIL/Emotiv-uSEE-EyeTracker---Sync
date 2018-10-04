#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 21:05:05 2018

A demo for getting Emotiv eeg raw data in real time.
Using Python websocket
Real time eeg data will be printed in the terminal and written into a txt file.
The returned time here of each data =  "the time that data being received" - "the time cortex was started". However, the tricky is 
we can't get "the time cortex was started". This is a bug and the Emotiv technical support has reported this issue to the Emotiv development
team. Hope they will fix this as soon as possible.

Emotiv Cortex need to be installed first. https://www.emotiv.com/developer/

@author: zhangbo
"""
# dependent pkgs install
# pip install websocket-client, ssl

import websocket
import ssl
import time
import json

# user information for login
username = "bit"
password = "Bit123456"
client_id = "I2OZ3iYEn9gMLJfNDjXf3AlJzPVihaeSrNw5ceth"
client_secret ="BBGcB3wkcTRTwiDupWxT0Yr6ucNeb4DeAi6WOxZSoDjPN7qMYuHZ44EoWkpWknBTNZns1DZw0ipR2j64lAT1TRAnSPFVK1Vd7cv8XCJyCuBaQYDk8iXcKg4iVdx3UWlA"

# establish websocket connect
ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://emotivcortex.com:54321")

# logout the existing users
with open("logout.json") as f:
    logout = f.read()
    logout = json.loads(logout)
    logout['params']['username'] = username
    logout = json.dumps(logout)
    ws.send(logout)
    print(ws.recv())

# login 
with open("login.json") as f:
    login = f.read()
    login = json.loads(login)
    login['params']['username'] = username
    login['params']['password'] = password
    login['params']['client_id'] = client_id
    login['params']['client_secret'] = client_secret    
    login = json.dumps(login)
    ws.send(login)
    print(ws.recv())

# wait for the request finished. In my testing, not need time.sleep(3)
    # you may delete this line to see whether it can still run
time.sleep(3)
# Authenticates a user
with open("authorize.json") as f:
    authorize = f.read()
    authorize = json.loads(authorize)
    authorize['params']['client_id'] = client_id
    authorize['params']['client_secret'] = client_secret
    authorize = json.dumps(authorize)
    ws.send(authorize)
    result = ws.recv()

# get Auth Token
_auth = json.loads(result)
_auth = _auth['result']['_auth']

# wait for the request finished. In my testing, not need time.sleep(3)
    # you may delete this line to see whether it can still run
time.sleep(3)
# accept license
with open("acceptLicense.json") as f:
    acceptLicense = f.read()
    acceptLicense = json.loads(acceptLicense)
    acceptLicense['params']['_auth'] = _auth
    acceptLicense = json.dumps(acceptLicense)
    ws.send(acceptLicense)
    print(ws.recv())

# wait for the request finished. In my testing, not need time.sleep(3)
    # you may delete this line to see whether it can still run
time.sleep(3)
# create session with activate status
with open("createSession.json") as f:
    createSession = f.read()
    createSession = json.loads(createSession)
    createSession['params']['_auth'] = _auth
    createSession = json.dumps(createSession)
    ws.send(createSession)
    result = (ws.recv())
sess = json.loads(result)
start_time = sess['result']['started']

# wait for the request finished. In my testing, not need time.sleep(3)
    # you may delete this line to see whether it can still run
time.sleep(3)
# subscribe
with open("subscribe.json") as f:
    subscribe = f.read()
    subscribe = json.loads(subscribe)
    subscribe['params']['_auth'] = _auth
    subscribe = json.dumps(subscribe)
    ws.send(subscribe)

# record 1000 lines of eeg data, default sampling rate is 125Hz
out = open('out8.txt','w')
n=0
while n<1000:
    result=ws.recv()
    out.write(result+'\n')
    n=n+1
    print(result)
out.close()

# unsubscribe
with open("unsubscribe.json") as f:
    unsubscribe = f.read()
    unsubscribe = json.loads(unsubscribe)
    unsubscribe['params']['_auth'] = _auth
    unsubscribe = json.dumps(unsubscribe)
    ws.send(unsubscribe)
    
# close session
with open("closeSession.json") as f:
    closeSession = f.read()
    closeSession = json.loads(closeSession)
    closeSession['params']['_auth'] = _auth
    closeSession = json.dumps(closeSession)
    ws.send(closeSession)

# close websocket
ws.close()
