# bs.py
Billig strøm <br>
Afvikler to gange om dagen (kl 8 og 20) og sender billigste tid i webhook "LowestPriceRestOfTheDay"


# ELOnOff

Get easy access to price on electicity in Denmark by colorcoding you Hue Light according to price and turn on charger (wemo switch) when low price and turn off when price is high



This Python program 
1) read the price for electricity in DK (DK1)
2) calls a webhook on IFTTT to set lights color correpsonding to the price 
3) calls a webhook on IFTTT the turn on and off a charger when price is low.

Thanks to <br>
#https://www.energidataservice.dk/tso-electricity/elspotprices <br>
#https://gist.github.com/tiede/66a160f8361e0821b904c6d47c6c7d71 <br>
#https://github.com/DrGFreeman/IFTTT-Webhook <br>
#https://ifttt.com/maker_webhooks <br>
#-----find webhook id here : https://ifttt.com/maker_webhooks/settings

