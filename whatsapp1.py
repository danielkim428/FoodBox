import os
from twilio.rest import Client

os.environ['TWILIO_ACCOUNT_SID'] = 'ACcd99094db783d1141bf1de6a0f4c1e5a'
os.environ['TWILIO_AUTH_TOKEN'] = 'e7b1fad4a5bff4685a0444bb77aba376'

client = Client()

from_whatsapp_number="whatsapp:+14155238886"
to_whatsapp_number="whatsapp:+821063539202"

otp = 'asdfas'

try:
    client.messages.create(body='Verify your phone number by submitting the OTP: ' + otp,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
except:
    print('no')
