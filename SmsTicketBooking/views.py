import urllib

from django.shortcuts import render

from django.http import HttpResponse
from django.template import Context, loader
from django.template.loader import get_template


def index(request):
    t = get_template('home.html')
    html = t.render(Context())
    return HttpResponse(html)

def parseIncomingMessage(request):
    sender = request.GET['sender']
    message_body = request.GET['msgdata']
    smsToBeSend = 'Processing'
    if validateMessageBody(message_body):
        smsToBeSend = generateSuccesMessage(message_body)
    else:
        smsToBeSend = generateFailureMessage()

    sendSMS(sender,smsToBeSend)
    return


def validateMessageBody(messagebody):
    return True;

def generateSuccesMessage(message):
    parts = message.split(" ")
    return 'Hi '+parts[0] +' Your booking of is confirmed.'

def generateFailureMessage():
    return "Please sms in correct format"

def sendSMS(sender,message_data):
    host = "http://127.0.0.1"
    user_name = "admin"
    user_password = "abc123"
    recipient = sender
    message_body = message_data

    http_req = host
    http_req += ":9501/api?action=sendmessage&username="
    http_req += urllib.quote(user_name)
    http_req += "&password="
    http_req += urllib.quote(user_password)
    http_req += "&recipient="
    http_req += urllib.quote(recipient)
    http_req += "&messagetype=SMS:TEXT&messagedata="
    http_req += urllib.quote(message_body)

    get = urllib.urlopen(http_req)
    req = get.read()
    get.close()

    if req.find("Message accepted for delivery") > 1:
        print "Message successfully sent"
    else:
        print "Message not sent! Please check your settings!"

    return

def generateRandom(request):
    return 123456;

