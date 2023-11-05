import math


def price_conversion(price):
    price = price[4:]
    if "K" in price:
        price = price[: price.find("K")]
        price = int(price) * 1000
        usd_price = price * 0.27
        usd_price = int(math.ceil(usd_price / 5000.0)) * 5000
        usd_price = "USD " + str(int(usd_price / 1000)) + "K"
        return usd_price
    if "M" in price:
        price = price[: price.find("M")]
        price = int(price) * 1000000
        usd_price = price * 0.27
        usd_price = int(math.ceil(usd_price / 5000.0)) * 5000
        usd_price = "USD " + str(int(usd_price / 1000)) + "K"
        return usd_price


price_conversion("AED 460K")
