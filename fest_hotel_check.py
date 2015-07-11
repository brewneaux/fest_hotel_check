#!/usr/bin/python

import os
import re
import requests
from bs4 import BeautifulSoup
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import datetime

url = 'http://thefestfl.limitedrun.com/products/549782-holiday-inn-gainesville'
# In textEmails, put your text-message email address, something like phonenumber@vtext.net for verizon
textEmails = '' 
emails = ['putyour', 'emails', 'here']
sender = 'who_the-Hell_isSending-this_shit'
smtp = 'putyoursmtpserverhere'

html = requests.get(url).text
soup = BeautifulSoup(html)

def sendSMS():

    mailer = smtplib.SMTP(smtp, 587);
    mailer.sendmail(sender, textEmails, 'A Fest room might be available!')

def sendEmail():
    mailer = smtplib.SMTP(smtp, 587);
    
    for email in emails:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = 'A Fest hotel room might be available'
        now = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
        body = "\nAt %s, a hotel room seemed to be available. Go get it!" % now
        msg.attach(MIMEText(body, 'plain'))
        mailer.ehlo()
        mailer.starttls()
        mailer.ehlo()
        txt = msg.as_string()
        mailer.sendmail(sender, email, txt)
        
logNoResults = 0
for option in soup.findAll('option'):
    matchFound = re.search(r'Double Room 3 Night.*', option.getText())

    if matchFound and not option.has_attr('disabled'):
        logNoResults = 1
        sendSMS()
        sendEmail()
        
if not logNoResults:
    cwd = os.path.dirname(__file__)
    logfile = open(cwd + '/fest_hotel.log', 'a');
    now = datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
    logfile.write(str(now) + " - Room not available - no messages sent\n")
