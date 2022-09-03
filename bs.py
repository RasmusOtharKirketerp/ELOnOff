# thanks to :
# https://www.energidataservice.dk/tso-electricity/elspotprices
# https://gist.github.com/tiede/66a160f8361e0821b904c6d47c6c7d71
# https://github.com/DrGFreeman/IFTTT-Webhook
# https://ifttt.com/maker_webhooks
# find webhook id here : https://ifttt.com/maker_webhooks/settings


from datetime import datetime
import time
import schedule
import ifttt
from prices import Prices


def run():
    p = Prices()
    p.initPrices()
    nu_time = str(datetime.now().hour)
    nu_billigst = p.getBilligstIdagEfter(nu_time)
    print("Billigst efter nu ", nu_time, " :",  nu_billigst)
    wh.trigger("LowestPriceRestOfTheDay", nu_time, nu_billigst)


schedule.clear()
schedule.every().day.at("08:00").do(run)
schedule.every().day.at("20:00").do(run)
myWebHookID = 'mUM-Q5MRdcmv0qd8MzVnzXplGMPIhN-QB5b067or_nl'
wh = ifttt.IftttWebhook(myWebHookID)
run()
while True:
    schedule.run_pending()
    print("bs.py : looping....", datetime.now())
    for j in schedule.get_jobs():
        print("Jobs in queue :", j)
    time.sleep(5)
