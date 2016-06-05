import random

import requests
from django.shortcuts import render

from django.http import HttpResponse
from django.template import Context, loader
from django.template.loader import get_template
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib


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
    content = '<html>Processing</html>'

    response = HttpResponse(content, content_type='application/liquid')
    response['Content-Length'] = len(content)

    receivedContents = request.body

    receivedContentsCommaSplit = receivedContents.strip().split("&")
    smsContents = validateMessageBody(receivedContentsCommaSplit)
    if smsContents.success:
        smsToBeSend = generateSuccesMessage(smsContents)
    else:
        smsToBeSend = generateFailureMessage()
    sendSMS(smsContents.sender,smsToBeSend)
    return response


def validateMessageBody(receivedContentsCommaSplit):
    for attributes in receivedContentsCommaSplit:
        print attributes
        if(attributes.startswith('from')):
            sender = attributes.strip().split('=')
        if(attributes.startswith('message')):
            messagebody = attributes.strip().split('=')

    smsContents = SMSContents(sender, messagebody)
    return smsContents

def generateSuccesMessage(smsContents):
    return 'Hi '+smsContents.sender+' Your booking of is confirmed.'

def generateFailureMessage():
    return "Please send sms in correct format"

def sendSMS(sender,message_data):
    host = "http://192.168.1.8:9710"
    response = requests.post(host+ '/send_sms', data={'sender':sender,'msgdata':message_data})
    print (response.content)
    if response.content is "Message accepted for delivery":
        print "Message successfully sent"
    else:
        print "Message not sent! Please check your settings!"

    return

def generateRandom(request):
    return random.randint(1, 10);


class SMSContents:
    success = False
    def __init__(self, sender, messagebody):
        self.sender = sender
        self.messagebody = messagebody
        if (sender and messagebody):
            success = True
        else:
            success = False



