import random

import requests
from django.shortcuts import render

from django.http import HttpResponse
from django.template import Context, loader
from django.template.loader import get_template
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
from twisted.internet import task
from twisted.internet import reactor

def index(request):
    t = get_template('home.html')
    html = t.render(Context())
    return HttpResponse(html)

'''
source=GSM+Modem+Gateway
&action=message_in
&user_id=
&from=%2b919840490729
&to=
&sms_central=%2b919840011016
&message=Test4
&message_type=sms.text
&message_part=1
&message_parts_received=1
&message_parts_total=1
&send_time=2016-06-05T10%3a11%3a02.0000000
&receive_time=2016-06-05T10%3a11%3a04.4458022%2b05%3a30
&pdu=0791198904100161240C9119890494709200006160500111202205D4F29C4E03

'''

@csrf_exempt
def parseIncomingMessage(request):
    content = 'Kindly wait till we process your request'

    response = HttpResponse(content, content_type='application/text')
    response['Content-Length'] = len(content)

    receivedContents = request.body

    print '#####'
    print '#####'
    print 'Inside parse incoming message'
    print 'Body'
    print request.body
    print '#####'
    print '#####'

    receivedContentsCommaSplit = receivedContents.strip().split("&")
    smsContents = validateMessageBody(receivedContentsCommaSplit)

    print '#####'
    print '#####'
    print 'Inside generateSuccesMessage - Part TWO'
    print smsContents.success
    print '#####'
    print '#####'

    if smsContents.success:
        smsToBeSend = generateSuccesMessage(smsContents)
    else:
        smsToBeSend = generateFailureMessage()
    sendSMS(smsContents,smsToBeSend)
    return response


def validateMessageBody(receivedContentsCommaSplit):
    for attributes in receivedContentsCommaSplit:
        if(attributes.startswith('from')):
            sender = attributes.strip().split('=')[1]
        if(attributes.startswith('message')):
            messagebody = attributes.strip().split('=')[1]

    print '#####'
    print '#####'
    print 'Inside validateMessageBody'
    print 'sender + messagebody'
    print  sender+' sneds ' + messagebody
    print '#####'
    print '#####'

    smsContents = SMSContents(sender, messagebody)
    return smsContents

def generateSuccesMessage(smsContents):
    print '#####'
    print '#####'
    print 'Inside generateSuccesMessage'
    print '#####'
    print '#####'
    return 'Hi '+smsContents.sender+' Your booking of is confirmed.'

def generateFailureMessage():
    print '#####'
    print '#####'
    print 'Inside generateFailureMessage'
    print '#####'
    print '#####'
    return "Please send sms in correct format"

def sendSMS(smsContents,smsToBeSend):
    host = "http://192.168.1.8"
    user_name = "admin"
    user_password = "admin"
    recipient = smsContents.sender
    message_body = smsToBeSend

    http_req = host
    http_req += ":9710/http/send-message?username="
    http_req += user_name
    http_req += "&password="
    http_req += user_password
    http_req += "&message-type=sms.text&message="
    http_req += message_body
    http_req += "&to="
    http_req += recipient

    get = urllib.urlopen(http_req)
    req = get.read()
    get.close()

    print '#####'
    print '#####'
    print 'Inside sendSMS'
    print 'Request'
    print  req
    print '#####'
    print '#####'

    if req.startswith("OK:"):
        print "Message successfully sent"
    else:
        print "Message not sent! Please check your settings!"

def generateRandom():
    securitycode = str(random.randint(1000, 9999))
    print 'value is'+ securitycode

def getcode(request):
    content = "{code:"+securitycode+"}"
    response = HttpResponse(content, content_type='application/text')
    response['Content-Length'] = len(content)
    return response;

class SMSContents:
    success = False
    def __init__(self, sender, messagebody):
        self.sender = sender
        self.messagebody = messagebody
        if (sender and messagebody and messagebody.startswith("ALBT")):
            self.success = True
        else:
            self.success = False
        print '#####'
        print '#####'
        print 'Inside SMSContents'
        print 'sender + messagebody'
        print  sender + ' sneds ' + messagebody +"Scuess? "
        print self.success
        print '#####'
        print '#####'



import time

def executeSomething():
    generateRandom()
    time.sleep(60)

while True:
    executeSomething()