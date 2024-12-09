import json
import sys
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
import requests
from listeners.send_email import send_email

# We want to run thread in an infinite loop
running = True
conf = {'bootstrap.servers': "localhost:9092",
        'auto.offset.reset': 'smallest',
        'group.id': "user_group"}
# Topic
topic = 'topic_user_created'


def send_simple_message(to, subject, body):
    try:
        print("Sending email...")
        return requests.post(
            "https://api.mailgun.net/v3/sandbox0ab9a857d8164f0ca4359b66c44b4053.mailgun.org/messages",
            auth=("api", "17497a5bc65c802c53475f46c59a0423-f55d7446-afa86d61"),
            data={"from": "Excited User <mailgun@sandbox0ab9a857d8164f0ca4359b66c44b4053.mailgun.org>",
                  "to": ["amruthk99@gmail.com"],
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomeness!"})
    except requests.RequestException as e:
        print("Request Error: ", e)


class UserCreatedListener(threading.Thread):

    help = "Listen to user created events"

    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(conf)

    def run(self):

        print('Inside EmailService :  Created Listener ')

        try:
            # Subcribe to topic
            self.consumer.subscribe([topic])
            while running:
                try:
                    # Poll for message
                    msg = self.consumer.poll(timeout=1.0)

                    if msg is None:
                        continue

                    # Handle Error
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            # End of partition event
                            sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                             (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                    else:
                        # Handle Message
                        print('---------> Got message Sending email.....')
                        if msg.value() is None:
                            print('---------> Message: ', msg.value())
                        else:
                            print('---------> Message: ',
                                  msg.value().decode('utf-8'))
                            message = json.loads(msg.value().decode('utf-8'))
                            # In Real world, write email sending logic here
                            send_email("amruthk99@gmail.com", "Welcome to Unirides - Your goto ridesharing app for Students",
                                       "<!DOCTYPE html><html><head><style>body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; } .email-container { max-width: 600px; margin: 20px auto; background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; } .header { background-color: #4CAF50; color: #ffffff; padding: 20px; text-align: center; } .content { padding: 20px; color: #333333; } .button { display: inline-block; margin: 20px 0; padding: 10px 20px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 4px; } .footer { background-color: #f1f1f1; text-align: center; padding: 10px; font-size: 12px; color: #777; }</style></head><body><div class=\"email-container\"><div class=\"header\"><h1>Welcome to UniRides!</h1></div><div class=\"content\">Hi " +
                                       "Amruth"+", <p> We're excited to have you join UniRides, the go-to ridesharing app for university students. Connecting with fellow students for convenient and affordable rides has never been easier!</p><p>To get started, simply log in to the app, set up your profile, and start exploring rides in your area.</p><a href=\"" +
                                       "UniRides\""+" class=\"button\">Get Started</a><p>If you have any questions or need assistance, feel free to reach out to our support team at <a href=\"mailto:support@unirides.com\">support@unirides.com</a>.</p><p>Happy riding!<br>The UniRides Team</p></div><div class=\"footer\"><p>&copy; 2024 UniRides. All rights reserved.</p></div></div></body></html>"
                                       )
                            print(message)

                except Exception as e:
                    print("Exception: ", e)

        except KafkaException as e:
            print("Kafka Exception: ", e)

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()
