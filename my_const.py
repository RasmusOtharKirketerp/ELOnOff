
colorLowest = 'BLUE'
colorLow = 'GREEN'
color = 'YELLOW'
colorHigh = 'RED'
colorHigest = 'PURPLE'
priceTohigh = 'price_to_high'
chargeOn = "chargeOn"
chargeOff = "chargeOff"
windowAhead = "48"


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
