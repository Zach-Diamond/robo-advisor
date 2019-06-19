# app/robo_advisor.py
###PACKAGES
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import os
import requests
import json
import pandas as pd
from sklearn import linear_model
import csv
import numpy as np
load_dotenv()


###FUNCTIONS
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)  
    #https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

def add_commas(my_number):
    return "{:,}".format(my_number)

def to_usd(my_price):  
     return "${0:,.2f}".format(float(my_price))



###LATER-USED VARIABLES
apikey = os.environ.get("ALPHAVANTAGE_API_KEY")
todaydate = datetime.now().strftime('%Y-%m-%d')
yesterday = date.today() - timedelta(days=1)
yesterdaydate = yesterday.strftime('%Y-%m-%d')


###USER INPUT 
entered_stock = input('Please type a stock symbol and press ENTER: ').lower()

while (len(entered_stock) > 5 or len(entered_stock) < 1 or hasNumbers(entered_stock)==True):
    entered_stock = input("Invalid entry. Please type a stock symbol and press ENTER: ").lower()
else: None


###REQUEST API AND CREATE VARIABLES
request_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={entered_stock}&apikey={apikey}'
response = requests.get(request_url)
# if response:
#     response
# else:
#     print('no worko')
#     quit()
parsed_response = json.loads(response.text)
try:
    parsed_response['Time Series (Daily)']
except:
    print("Stock symbol not recognized. Please restart and try again.")
    exit()
parsed_timeseries = parsed_response['Time Series (Daily)']

try:
    parsed_response['Time Series (Daily)'][todaydate]
except:
    print("Stock symbol not recognized. Please restart and try again.")
    exit()

today_parsed_timeseries = parsed_response['Time Series (Daily)'][todaydate]


###Creating TODAY Variables
today_open = float(today_parsed_timeseries['1. open'])
today_close = float(today_parsed_timeseries['4. close'])
today_high = float(today_parsed_timeseries['2. high'])
today_low = float(today_parsed_timeseries['3. low'])
yesterday_close = float(parsed_response['Time Series (Daily)'][yesterdaydate]['4. close'])


###Creating TOTAL Variables
daily_highs = [float(parsed_timeseries[i]['2. high']) for i in parsed_timeseries]
daily_lows = [float(parsed_timeseries[i]['3. low']) for i in parsed_timeseries]

###Creating average/max/min
daily_high_average = np.average(daily_highs)
daily_lows_average = np.average(daily_lows)
daily_high_max = np.max(daily_highs)
daily_lows_max = np.max(daily_lows)
daily_high_min = np.min(daily_highs)
daily_lows_min = np.min(daily_lows)
daily_high_std = np.std(daily_highs)
daily_lows_std = np.std(daily_lows)
df = pd.DataFrame([(i,float(parsed_timeseries[i]['2. high'])) for i in parsed_timeseries], columns=['date','high'])
df['date_ordinal'] = pd.to_datetime(df['date']).map(datetime.datetime.toordinal)
reg = linear_model.LinearRegression()
reg.fit(df['date_ordinal'].values.reshape(-1, 1), df['high'].values)

reg.coef_

array([0.80959405])



###CREATING SUPER ADVANCED RECOMMENDATION ENGINE OF THE FUTURE
total_score = 0
reasons = []

#Is today's low  > daily high average?
if (today_low/daily_high_average)-1 > .2:
    total_score+=3
    reasons.append("Today's low is >20% vs. average daily high!")
elif (today_low/daily_high_average)-1 > .1:
    total_score+=2
    reasons.append("Today's low is >10% vs. average daily high.")
else:
    total_score+=0
    reasons.append("Today's low is not very strong vs. daily high.")

#Is today's low more than 1.5 St.D. over average daily high?
if today_low > daily_high_average+(daily_high_std*2):
    total_score+=2
    reasons.append("Today's low is more than 2 deviations over the average daily high!")
if today_low > daily_high_average+(daily_high_std):
    total_score+=1
    reasons.append("Today's low is more than 1 deviation over the average daily high!")
else:
    total_score+=0
    reasons.append("Today's low is not remarkable vs. the average daily high's standard deviation.")

#Is the opening price > yesterday's close?
if today_open>yesterday_close:
    total_score+=1
    reasons.append("Today's open is higher than yesterday's close!")
else:
    total_score+=0
    reasons.append("Today's open is below yesterday's close.")

#Is the opening price > daily high average?
if (today_open/daily_high_average)-1 > .2:
    total_score+=2
    reasons.append("Today's open is >20% vs. average daily high!")
elif (today_open/daily_high_average)-1 > .1:
    total_score+=1
    reasons.append("Today's open is >10% vs. average daily high.")
else:
    total_score+=0
    reasons.append("Today's open is not very strong vs. daily high.")



#Max = 8

print(total_score)
print(reasons)

###PRINT RESULTS
print('--------------------------------------')
print(f"SELECTED SYMBOL: {entered_stock.upper()}")
print('--------------------------------------')
print('REQUESTING STOCK MARKET DATA...')
print(f"RUN AT: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
print(f'DATA THROUGH: {next(iter(parsed_timeseries))}')
print('--------------------------------------')
print(f"  ### {entered_stock.upper()} ###")
print(f"OPENING PRICE: {to_usd(today_open)}")
print(f"CLOSING PRICE: {to_usd(today_close)}")
print(f"DAILY HIGH: {to_usd(today_high)}")
print(f"DAILY LOW: {to_usd(today_low)}")
print(f"TOTAL VOLUME: {add_commas(int(today_parsed_timeseries['5. volume']))}")









    #  T E M P O R A R I L Y   D I S A B L E D 
# #Export to file based on stock name (and append if already exists)
# with open(f'../data/prices_{entered_stock}.csv', 'a') as csvFile:
#     fieldnames = ['1. open', '2. high', '3. low', '4. close', '5. volume']
#     writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow (today_parsed_timeseries)
# csvFile.close()


# print("RECOMMENDATION: BUY!")
# print("RECOMMENDATION REASON: TODO")
# print("-------------------------")
# print("HAPPY INVESTING!")
# print("-------------------------")


#Call API key via .env file (dotenv)

#{'1. open': '247.5400', '2. high': '251.3050', '3. low': '243.9000', '4. close':
# '250.1200', '5. volume': '580627'}
