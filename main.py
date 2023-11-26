import conf  # imports conf.py fle stored in the same directory
import time
import json
import requests
from boltiot import Bolt, Sms, Email

bolt = Bolt(conf.BOLT_API, conf.DEVICE_ID)  # we have configured our module connections
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)  # our twillio account is connected to our code
mail = Email(conf.MAIL_API, conf.SANDBOX_URL, conf.SENDER_MAIL,
             conf.RECEIVER_MAIL)  # our mailgun account is also connected to our code now

  # now we input our desired selling price.


# following is the function definition which will be called later
def price_check():
    url = ("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms={}".format(
        currency.upper()))  # currency.upper converts string into uppercase letters.
    response = requests.request("GET", url)
    response = json.loads(response.text)
    current_price = response[currency.upper()]
    return current_price


print("Select any one of the following currency input\nINR\nUSD\nJPY\nEUR")
currency = input(
    "Enter the above Currency from which you have to invest in:")  # we chose the currency which we want to invest in
market_price = price_check()
print("Market price of Bitcoin is:",market_price)
sell_price = float(input("Enter Your Selling Price:"))


while True:
    # this prints current market price of Bitcoin in the specified country currency.
    print("Selling Price is:", sell_price)  # this gives the Selling price we have entered.
    try:
        if market_price < sell_price:  # this checks for current market price bitcoin is less than of selling price or not.
            bolt.digitalWrite("0", "HIGH")  # LED gets "ON
            response1 = sms.send_sms(
                "The Bitcoins are at price ={} You can Invest now if you want".format(market_price))
            print("Status of Sms at Twilo:" + str(
                response1.status))  # Prints status of twilio account whether message reached or not.
            response = mail.send_email("Alert", "The Bitcoins are at price ={} You can Invest now if you want".format(
                market_price))

        elif market_price > sell_price:
            bolt.digitalWrite("1", "HIGH")  # BUZZER gets "ON
            response1 = sms.send_sms(
                "The Bitcoins are at price ={} You need to be cautious".format(market_price))
            print("Status of Sms at Twilo:" + str(
                response1.status))  # Prints status of twilio account whether message reached or not.
            response = mail.send_email("CAUTION", "The Bitcoins are at price ={} You need to be cautious".format(
                market_price))
    except Exception as e:
        print("An error occurred\n")
        print(e)
    time.sleep(5)
    bolt.digitalWrite("0", "LOW")  # led gets off
    bolt.digitalWrite("1", "LOW")  # buzzer gets off
    time.sleep(30)