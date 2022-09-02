import time
import requests


def createHeader():
    apiHeader = {
        "Content-Type": "application/json"
    }

    return [apiHeader]


def spotprices(windowAhead):
    headers = createHeader()
    url = "https://api.energidataservice.dk/datastore_search?resource_id=elspotprices&limit=" + \
        windowAhead + "&filters={\"PriceArea\":\"DK1\"}&sort=HourUTC desc"
    return requests.get(url, headers=headers[0]).json()


def filter_current_price(result):
    hour_dk = result["HourDK"]
    current_hour = time.strftime("%Y-%m-%dT%H:00:00")
    return hour_dk == current_hour


def getDKSportPrice():
    response = spotprices()
    prices = response["result"]["records"]
    current_hour_result = list(filter(filter_current_price, iter(prices)))
    print(prices)

    if len(current_hour_result) == 0:
        raise Exception("No current hour result")

    current_hour_price = current_hour_result[0]["SpotPriceEUR"]

    current_hour_price_kwh = (float(current_hour_price) * 7.46) / 1000.0

    # print(current_hour_result)
    #print (current_hour_price_kwh)

    return current_hour_price_kwh
