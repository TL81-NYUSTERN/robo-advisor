# app/robo_advisor.py

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY: 2018-02-20")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

from dotenv import load_dotenv
import os

os.chdir('..') # go back one directory where the .env file is saved

load_dotenv() #> loads contents of the .env file into the script's environment

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


import requests

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact&apikey=" + API_KEY
response = requests.get(request_url)
print(response.text)