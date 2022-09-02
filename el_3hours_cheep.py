# thanks to :
# https://www.energidataservice.dk/tso-electricity/elspotprices
# https://gist.github.com/tiede/66a160f8361e0821b904c6d47c6c7d71
# https://github.com/DrGFreeman/IFTTT-Webhook
# https://ifttt.com/maker_webhooks
# find webhook id here : https://ifttt.com/maker_webhooks/settings


import datetime
import time
import time
import schedule
import ifttt
from prices import Prices


def run():
    p = Prices()
    #wh.trigger("3hoursLow", my_const.windowAhead, p.tid[p.min_idx])


schedule.every().day.at("08:00").do(run)
schedule.every().day.at("20:00").do(run)
myWebHookID = 'mUM-Q5MRdcmv0qd8MzVnzXplGMPIhN-QB5b067or_nl'
wh = ifttt.IftttWebhook(myWebHookID)
run()
while True:
    schedule.run_pending()
    print("el_3hours_cheep.py : looping....", datetime.datetime.now())
    time.sleep(60)
