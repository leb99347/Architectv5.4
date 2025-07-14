import os
import oandapyV20
from oandapyV20.endpoints.pricing import PricingInfo

def get_price_data(instruments=["GBP_JPY"]):
    print("Account ID:", os.getenv("OANDA_ACCOUNT_ID"))
    print("API Key:", os.getenv("OANDA_API_KEY")[:6], "...")  # partial for security
    client = oandapyV20.API(access_token=os.getenv("OANDA_API_KEY"))
    params = {"instruments": ",".join(instruments)}
    r = PricingInfo(accountID=os.getenv("OANDA_ACCOUNT_ID"), params=params)
    client.request(r)
    return r.response
