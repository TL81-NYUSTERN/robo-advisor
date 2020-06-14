# app/robo_advisor.py

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


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
    sys.exit() # exit program if no data found

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
days_lookback = 100 # number of days of lookback for calculations

high_price_list = df_transpose['2. high'].tolist() # converting dataframe column to a list
high_price_list = high_price_list[:days_lookback] # changing list size to match number of days for lookback period
recent_high = max(high_price_list)


low_price_list = df_transpose['3. low'].tolist() # converting dataframe column to a list
low_price_list = low_price_list[:days_lookback] # changing list size to match number of days for lookback period
recent_low = min(low_price_list)


# RECOMMENDATION METHODOLOGY

import statistics

closing_price_list = df_transpose['4. close'].tolist()
closing_price_list = closing_price_list[:days_lookback]

standard_dev = statistics.stdev(closing_price_list)
average = statistics.mean(closing_price_list)
one_stdev_above = average + (standard_dev * 1)
one_stdev_below = average - (standard_dev * 1)

if (average < closing_price and closing_price < one_stdev_above):
    recommendation = "BUY!"
    reason = (f"LAST CLOSING PRICE ({to_usd(closing_price)}) IS BETWEEN THE AVERAGE ({to_usd(average)}) "
    f"AND ONE STANDARD DEVIATION ABOVE THE MEAN ({to_usd(one_stdev_above)}), WHICH INDICATES THERE IS UPWARD MOMENTUM.")
elif closing_price > one_stdev_above:
    recommendation = "SELL or DO NOT BUY"
    reason = (f"LAST CLOSING PRICE ({to_usd(closing_price)}) IS HIGHER THAN ONE STANDARD DEVIATION ABOVE THE MEAN ({to_usd(one_stdev_above)}), "
    f"WHICH MAY INDICATE THAT IT IS OVERVALUED.")
elif (closing_price < average and closing_price > one_stdev_below):
    recommendation = "BUY!"
    reason = (f"LAST CLOSING PRICE ({to_usd(closing_price)}) IS LOWER THAN THE AVERAGE ({to_usd(average)}) BUT "
    f"HIGHER THAN ONE STANDARD DEVIATION BELOW THE MEAN ({to_usd(one_stdev_below)}), WHICH INDICATES THERE IS AN OPPORTUNITY FOR THE PRICE TO REBOUND.")
elif closing_price < one_stdev_below:
    recommendation = "SELL or DO NOT BUY"
    reason = (f"LAST CLOSING PRICE ({to_usd(closing_price)}) IS LOWER THAN ONE STANDARD DEVIATION BELOW THE MEAN ({to_usd(one_stdev_below)}), "
    f"WHICH MAY INDICATE THAT THE PRICE HAS DROPPED TOO SIGNIFICANTLY AND IS ON A DOWNWARD TREND.")
elif closing_price = one_stdev_below:
    recommendation = "DO NOT BUY"
    reason = (f"LAST CLOSING PRICE EQUAL TO THE AVERAGE, THEREFORE NO INDICATION ON ANY MOVEMENT.")    


print("-------------------------")
print(f"SELECTED SYMBOL: {stock_symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {last_refresh}")
print("-------------------------")
print(f"LATEST DAY: {closing_date}")
print(f"LATEST CLOSE: {to_usd(closing_price)}")
print(f"RECENT HIGH: {to_usd(recent_high)}")
print(f"RECENT LOW: {to_usd(recent_low)}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {reason}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")