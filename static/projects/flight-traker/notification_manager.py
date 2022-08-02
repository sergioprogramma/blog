account_sid = "AC25aad92a99c628e1cc28a5e23947de08"
auth_token = "8df484fd134e78df6d373eb8dd06ae19"

from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import smtplib
import os

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_text(self, dep_city, dep_airport, ar_city, ar_airport, price, first_day, last_day):
        proxy_client = TwilioHttpClient()
        # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"Important message! The flight from {dep_city}-{dep_airport} to {ar_city}-{ar_airport} has a new lowest price of ${price}. From {first_day} to {last_day}",
            from_="+16812525644",
            to="+16473940639"
        )
        print(message.status)

    def send_email(self, dest_email, my_email, password, dep_city, dep_airport, ar_city, ar_airport, price, first_day, last_day):
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=dest_email,
            msg=f"Subject: Get ready to fly!\n\nGOOD NEWS! The flight from {dep_city}-{dep_airport} to {ar_city}-{ar_airport} has a new lowest price of ${price}. From {first_day} to {last_day}"
        )
