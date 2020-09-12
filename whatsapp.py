import os
from twilio.rest import Client

os.environ['TWILIO_ACCOUNT_SID'] = 'ACcd99094db783d1141bf1de6a0f4c1e5a'
os.environ['TWILIO_AUTH_TOKEN'] = 'ad848429edfbe548faaaafc94f7f86ad'

client = Client()

from_whatsapp_number="whatsapp:+14155238886"
to_whatsapp_number="whatsapp:+821090292356"

otp = 'asdfas'
request.user.profile.otp = otp
user.profile.save()

client.messages.create(body='Verify your phone number by submitting the OTP: ' + otp,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
