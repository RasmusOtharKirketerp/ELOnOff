# thanks to :
#https://www.energidataservice.dk/tso-electricity/elspotprices
#https://gist.github.com/tiede/66a160f8361e0821b904c6d47c6c7d71
#https://github.com/DrGFreeman/IFTTT-Webhook
#https://ifttt.com/maker_webhooks
# find webhook id here : https://ifttt.com/maker_webhooks/settings


import requests
import time
from pathlib import Path

default_url = 'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'

myWebHookID  = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

colorLowest = 'BLUE'
colorLow = 'GREEN'
color = 'YELLOW'
colorHigh = 'RED'
colorHigest = 'PURPLE'

def createHeader():
    apiHeader = {
        "Content-Type": "application/json"
    }

    return [apiHeader]

def filter_current_price(result):
    hour_dk = result["HourDK"]
    current_hour = time.strftime("%Y-%m-%dT%H:00:00")
    return hour_dk == current_hour

def spotprices():
    headers = createHeader()
    url = "https://api.energidataservice.dk/datastore_search?resource_id=elspotprices&limit=48&filters={\"PriceArea\":\"DK1\"}&sort=HourUTC desc"
    return requests.get(url, headers=headers[0]).json()

def getDKSportPrice():
    response = spotprices()
    prices = response["result"]["records"]
    current_hour_result = list(filter(filter_current_price, iter(prices)))

    if len(current_hour_result) == 0:
        raise Exception("No current hour result")

    current_hour_price = current_hour_result[0]["SpotPriceEUR"]

    current_hour_price_kwh = (float(current_hour_price) * 7.46) / 1000.0

    #print(current_hour_result)
    #print (current_hour_price_kwh)

    return current_hour_price_kwh

#webhooks IFTTT
# 
class IftttWebhook():
    """A class to trigger IFTTT webhook events."""

    def __init__(self, key, url=default_url):
        """A class to trigger IFTTT webhook events.
        Parameters
        ----------
        key : str
            The user's IFTTT Webhook key. This key can be found under
            "Documentation" at https://ifttt.com/maker_webhooks/. The key can
            be passed directly to the key parameter or stored in a text file.
            If the value passed to the key parameter is a valid path to a file,
            then the constructor will look for the key on the first line of
            this file.
        url : str, default: 'https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'
            The string corresponding to the url of the webhook event. The
            '{event_name}' and '{key}' fileds will be automatically filled with
            the proper values upon calling one of the trigger methods.
        """
        if Path(key).is_file():
            with open(Path(key), 'r') as f:
                self._key = f.readlines()[0].strip('\n').strip('\r')
        else:
            self._key = key
        self._url = url
        # Trigger a test event to check if key is valid
        self.trigger('key_test_event')
    
    def trigger(self, event_name, value1=None, value2=None, value3=None):
        """Triggers the IFTTT event defined by event_name with the JSON content
        defined by the value1, value2 and value3 parameters.
        
        Parameters
        ----------
        event_name : str
            The name of the IFTTT webhook event to trigger (set in the
            "Event Name" field of the IFTTT Webhook).
        value1, value2 and value3 : str or number
            The optional values passed to the JSON body of the webhook. These
            will be passed as "ingredients" to the Action of the IFTTT Recipe.
        """
        body = {}
        if value1 is not None:
            body['value1'] = value1
        if value2 is not None:
            body['value2'] = value2
        if value3 is not None:
            body['value3'] = value3
        url = self._url.format(event_name=event_name, key=self._key)
        response = requests.post(url, json=body)
        print(url)
        if response.status_code != 200:
            raise IftttException(response.status_code, response.text.strip('\n'))
        else:
            print(response.status_code , " - " , response.text.strip('\n'))


    def gmail(self, to, subject=None, body=None):
        """Triggers an IFTTT event named 'send_gmail' that send an email using
        the user's Gmail account, with the value1, value2 and value3
        "ingredients" mapped to the To, Subject and Body fields respectively.
        
        For this method to work, the event must be created in the user's IFTTT
        account.
        """
        self.trigger('send_gmail', to, subject, body)

    def notification(self, title=None, message=None, url=None):
        """Triggers an IFTTT event named 'notification' that sends a
        notification to the user via the IFTTT mobile application. The value1,
        value2 and value3 "ingredients" are mapped to the Title, Content and
        URL fields of the notification respectively.
        For this method to work, the event must be created in the user's IFTTT
        account.
        """
        self.trigger('notification', title, message, url)

class IftttException(Exception):
    def __init__(self, status_code, content):
        self.content = content
        self.status_code = status_code

    def __str__(self):
        return repr(f"Status code: {self.status_code}, message: {self.content}")
current_hour_price_kwh = getDKSportPrice()

print(current_hour_price_kwh)

wh = IftttWebhook(myWebHookID)
#priceTohigh = 'qeiTcPnb-if-maker-event-price_to_high-then-turn-off-all'
priceTohigh = 'price_to_high'
chargeOn = "chargeOn"
chargeOff = "chargeOff"
#if current_hour_price_kwh > 4:


def setColor(inValue):
    


    retVal = colorLowest
    if inValue > 2: 
        retVal = colorLow
    
    if inValue > 4: 
        retVal = color

    if inValue > 6:         
        retVal = colorHigh

    if inValue > 8:
        retVal = colorHigest

    print("Color :" + retVal)
    return retVal


state = setColor(current_hour_price_kwh)
wh.trigger(priceTohigh, state, current_hour_price_kwh)

if state == colorLow or state == colorLowest:
    wh.trigger(chargeOn)
else :
    wh.trigger(chargeOff)



