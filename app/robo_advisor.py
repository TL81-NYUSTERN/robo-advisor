# app/robo_advisor.py

#print("-------------------------")
#print("SELECTED SYMBOL: XYZ")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT: 2018-02-20 02:00pm")
#print("-------------------------")
#print("LATEST DAY: 2018-02-20")
#print("LATEST CLOSE: $100,000.00")
#print("RECENT HIGH: $101,000.00")
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")

from dotenv import load_dotenv
import os

os.chdir('..') # go back one directory where the .env file is saved

load_dotenv() #> loads contents of the .env file into the script's environment

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


# USER INPUT CODE
while True:

    stock_symbol = input(f'Please enter one stock or cryptocurrency symbol: ').upper() 

    if len(stock_symbol) > 5:
        print("Sorry, that is too many characters.")
        continue

    elif stock_symbol.isdigit():
        print("Sorry, input cannot be all numbers.")
        continue

    else:
        break


# GET REQUEST FROM URL
import requests

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock_symbol + "&outputsize=compact&apikey=" + API_KEY
response = requests.get(request_url)

import json

response_data = json.loads(response.text) # convert JSON string into dictionary

import sys

if response.status_code != 200 or "ERROR MESSAGE" in str(response_data).upper():
    print("Sorry, couldn't find any trading data for that symbol.")
    sys.exit()

my_dict = response_data['Time Series (Daily)'] 


# PROCESSING DATA
import pandas as pd

df = pd.DataFrame(my_dict)
df_transpose = df.transpose()
df_transpose.reset_index(level=0, inplace=True)
df_transpose.rename(columns={'index': 'timestamp'}, inplace=True)

#print(df_transpose)

data_dir = os.path.join(os.getcwd(), "data")
csv_name = "prices_" + stock_symbol + ".csv"
csv_path = os.path.join(data_dir, csv_name)

df_transpose.to_csv(csv_path, index=False)