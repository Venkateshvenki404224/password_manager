
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC7b95626d9c0425256da8a60c0397b84f'
auth_token = '7fdde58b718521c01ea32c2c9f751317'
client = Client(account_sid, auth_token)

verification = client.verify \
                     .v2 \
                     .services('VAa91c04ee68751684496073318dfae4ab') \
                     .verifications \
                     .create(to='+918073088890', channel='sms')

print(verification.status)