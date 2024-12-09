import requests


def send_email(to, subject, body):
    try:
        print("Sending email...")
        response = requests.post(
            "https://api.mailgun.net/v3/sandbox0ab9a857d8164f0ca4359b66c44b4053.mailgun.org/messages",
            auth=("api", "17497a5bc65c802c53475f46c59a0423-f55d7446-afa86d61"),
            data={"from": "Excited User <mailgun@sandbox0ab9a857d8164f0ca4359b66c44b4053.mailgun.org>",
                  "to": [to],
                  "subject": subject,
                  "html": body})
        print("Email Sent Response: ", response)
        return response
    except requests.RequestException as e:
        print("Request Error: ", e)
