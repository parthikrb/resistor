import urllib.request
import json
import base64

from django.conf import settings

def send_invitation_email(to, subject, body):
    api_key = settings.MAILJET_KEY
    api_secret = settings.MAILJET_SECRET

    url = 'https://api.mailjet.com/v3/send'
    auth = api_key + ':' + api_secret
    data = {
        'FromEmail': 'parthi.krb@gmail.com',
        'FromName': 'Parthiban Baskar',
        'Subject': subject,
        'Text-part': body,
        'Recipients': [{'Email': to}]
    }
    data = json.dumps(data).encode('utf8')
    req = urllib.request.Request(url, data, {'Content-Type': 'application/json'}, method='POST')
    base64string = base64.b64encode(auth.encode())
    req.add_header("Authorization", "Basic %s" % base64string.decode())
    response = urllib.request.urlopen(req)
    if response.status == 200:
        print('Email sent successfully')
    else:
        print(f'An error occurred: {response.reason}')

def invite_user(to, organization, invitation_code):
    subject = f'Invitation to join {organization.name}'
    body = f'You have been invited to join {organization.name}! To accept the invitation, click the link below:\n'
    body += f'http://localhost:4200/join?token={invitation_code}'
    send_invitation_email(to, subject, body)
