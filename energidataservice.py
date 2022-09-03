from datetime import datetime
import time
import requests
import my_const


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


def filter_today_price(result):
    res_timestamp = result["HourDK"]
    #current_timestamp = time.strftime("%Y-%m-%dT%H:00:00")
    current_day = time.strftime("%Y-%m-%dT%H:00:00")
    #print("Current day : ", current_day)
    date_object = datetime.strptime(res_timestamp, "%Y-%m-%dT%H:00:00")

    #print("data day", date_object.day, "today day", datetime.now().day)

    if (date_object.day == datetime.now().day):
        return res_timestamp


def getDKSportPrice():
    response = spotprices(my_const.windowAhead)
    prices = response["result"]["records"]
    current_hour_result = list(filter(filter_current_price, iter(prices)))
    # print(prices)

    if len(current_hour_result) == 0:
        raise Exception("No current hour result")

    current_hour_price = current_hour_result[0]["SpotPriceEUR"]

    current_hour_price_kwh = (float(current_hour_price) * 7.46) / 1000.0

    # print(current_hour_result)
    # print(current_hour_price_kwh)

    return current_hour_price_kwh


def getDKPriceToday():
    response = spotprices(my_const.windowAhead)
    prices = response["result"]["records"]
    today_result = list(filter(filter_today_price, iter(prices)))
    # print(prices)

    if len(today_result) == 0:
        raise Exception("No today result")

    #current_hour_price = today_result[0]["SpotPriceEUR"]

    #current_hour_price_kwh = (float(current_hour_price) * 7.46) / 1000.0

    # print(current_hour_result)
    # print(today_result)

    return today_result
