# app/robo_advisor.py


# LOOKING UP API CODE FROM ENV FILE
from dotenv import load_dotenv
import os

os.chdir('..') # go back one directory where the .env file is saved

load_dotenv() #> loads contents of the .env file into the script's environment

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

os.chdir('app') # go back to app directory


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
    print("Sorry, trading data could not be found for that symbol.")
    sys.exit()

my_dict = response_data['Time Series (Daily)'] # isolating price data


# GET LAST REFRESH DATE
last_refresh = response_data['Meta Data']['3. Last Refreshed']


# PROCESSING DATA AND CONVERTING TO DATAFRAME
import pandas as pd

df = pd.DataFrame(my_dict)
df_transpose = df.transpose()
df_transpose.index.name = 'timestamp'


# CREATING CSV FILE
data_dir = os.path.join(os.getcwd(), "..", "data")
csv_name = "prices_" + stock_symbol + ".csv"
csv_path = os.path.join(data_dir, csv_name)

df_transpose.to_csv(csv_path)
df_transpose["2. high"] = df_transpose["2. high"].astype(float) # converting string values to float
df_transpose["3. low"] = df_transpose["3. low"].astype(float) # converting string values to float
df_transpose["4. close"] = df_transpose["4. close"].astype(float) # converting string values to float


# GET LAST CLOSING DATE AND PRICE
closing_date = df_transpose.index[0] # assumes latest date is the first row in the data (index =0)
closing_price = df_transpose['4. close'].iloc[0] 


# GET RECENT HIGH AND LOW
high_price_list = df_transpose['2. high'].tolist() # converting dataframe column to a list
recent_high = max(high_price_list)

low_price_list = df_transpose['3. low'].tolist() # converting dataframe column to a list
recent_low = min(high_price_list)


print("-------------------------")
print(f"SELECTED SYMBOL: {stock_symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {last_refresh}")
print("-------------------------")
print(f"LATEST DAY: {closing_date}")
print(f"LATEST CLOSE: {closing_price}")
print(f"RECENT HIGH: {recent_high}")
print(f"RECENT LOW: {recent_low}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")