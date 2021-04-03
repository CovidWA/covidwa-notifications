from dotenv import load_dotenv
import os
from twilio.rest import Client


def get_balance():
    client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])
    return float(client.balance.fetch().balance)


if __name__ == '__main__':
    load_dotenv()
    print(get_balance())
