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
import matplotlib.pyplot as plt
load_dotenv()


########FUNCTIONS
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)  
    #https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

def add_commas(my_number):
    return "{:,}".format(my_number)

def to_usd(my_price):  
     return "${0:,.2f}".format(float(my_price))


########SCRIPT-WIDE VARIABLES
apikey = os.environ.get("ALPHAVANTAGE_API_KEY")
todaydate = datetime.now().strftime('%Y-%m-%d')
yesterday = date.today() - timedelta(days=1)
yesterdaydate = yesterday.strftime('%Y-%m-%d')


########USER INPUT 
entered_stock = input('Please type a stock symbol and press ENTER: ').lower()

while (len(entered_stock) > 5 or len(entered_stock) < 1 or hasNumbers(entered_stock)==True):
    entered_stock = input("Invalid entry. Please type a stock symbol and press ENTER: ").lower()
else: None


########REQUEST API AND CREATE VARIABLES
request_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={entered_stock}&apikey={apikey}'
response = requests.get(request_url)
parsed_response = json.loads(response.text)

#PREVENTING ERRORS AT RESPONSE
try:
    parsed_response['Time Series (Daily)']
except:
    print("Stock symbol not recognized. Please restart and try again.")
    exit()

parsed_timeseries = parsed_response['Time Series (Daily)']
all_dates = list(parsed_timeseries.keys()) 
#PREVENTING ERRORS AT RESPONSE
try:
    parsed_response['Time Series (Daily)'][todaydate]
except:
    todaydate = all_dates[0]
    yesterdaydate = all_dates[1]

today_parsed_timeseries = parsed_response['Time Series (Daily)'][todaydate]

# try:
#     parsed_response['Time Series (Daily)'][todaydate]
# except:
    

########VARIABLES TO BE USED
#Creating TODAY Variables
today_open = float(today_parsed_timeseries['1. open'])
today_close = float(today_parsed_timeseries['4. close'])
today_high = float(today_parsed_timeseries['2. high'])
today_low = float(today_parsed_timeseries['3. low'])
yesterday_close = float(parsed_response['Time Series (Daily)'][yesterdaydate]['4. close'])

#Creating TOTAL Variables
daily_highs = [float(parsed_timeseries[i]['2. high']) for i in parsed_timeseries]
daily_lows = [float(parsed_timeseries[i]['3. low']) for i in parsed_timeseries]

#Creating average/max/min
daily_high_average = np.average(daily_highs)
daily_lows_average = np.average(daily_lows)
daily_high_max = np.max(daily_highs)
daily_lows_max = np.max(daily_lows)
daily_high_min = np.min(daily_highs)
daily_lows_min = np.min(daily_lows)
daily_high_std = np.std(daily_highs)
daily_lows_std = np.std(daily_lows)

#Attempting to calculate slope - help from https://stackoverflow.com/questions/53100393/how-to-get-slope-from-timeseries-data-in-pandas
df_highs = pd.DataFrame([(i,float(parsed_timeseries[i]['2. high'])) for i in parsed_timeseries], columns=['date','high'])
df_highs['high'] = pd.to_numeric(df_highs['high'], errors='coerce')
df_highs['date']=pd.to_datetime(df_highs['date'])
df_highs['date_ordinal'] = pd.to_datetime(df_highs['date']).map(datetime.toordinal)
reg = linear_model.LinearRegression()
reg.fit(df_highs['date_ordinal'].values.reshape(-1, 1), df_highs['high'].values)
slope = float(reg.coef_)


########CREATING SUPER ADVANCED RECOMMENDATION ENGINE OF THE FUTURE
total_score = 0
reasons = []

#Is the slope positive and close to 1?
if slope > .5:
    total_score+=4
    reasons.append("(+) This stock has a positive and strong slope.")
elif slope < .5 and slope > 0:
    total_score+=2
    reasons.append("(+) This stock has a positive slope.")
else:
    total_score+=-2
    reasons.append("(-) This stock has a negative slope.")

#Is Recent low  > daily high average?
if (today_low/daily_high_average)-1 > .2:
    total_score+=4
    reasons.append("(++) Recent low is >20% vs. its average daily high!")
elif (today_low/daily_high_average)-1 > .1:
    total_score+=2
    reasons.append("(+) Recent low is >10% vs. its average daily high.")
else:
    total_score+=0
    reasons.append("(-) Recent low is not very strong vs. its average daily high.")

#Is Recent low more than 1.5 St.D. over average daily high?
if today_low > daily_high_average+(daily_high_std*2):
    total_score+=3
    reasons.append("(++) Recent low is more than 2 deviations over the average daily high!")
if today_low > daily_high_average+(daily_high_std):
    total_score+=1
    reasons.append("(+) Recent low is more than 1 deviation over the average daily high!")
else:
    total_score+=0
    reasons.append("(-) Recent low is not remarkable vs. the average daily high's standard deviation.")

#Is the opening price > yesterday's close?
if today_open>yesterday_close:
    total_score+=1
    reasons.append("(+) Recent open is higher than yesterday's close!")
else:
    total_score+=0
    reasons.append("(-) Recent open is below yesterday's close.")

#Is the opening price > daily high average?
if (today_open/daily_high_average)-1 > .2:
    total_score+=2
    reasons.append("(+) Recent open is >20% vs. average daily high!")
elif (today_open/daily_high_average)-1 > .1:
    total_score+=1
    reasons.append("(+) Recent open is >10% vs. average daily high.")
else:
    total_score+=0
    reasons.append("(-) Recent open is not very strong vs. daily high.")

reasons_clean = [i for i in reasons]

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
print('--------------------------------------')
if total_score >= 9:
    print("RECOMMENDATION: STRONG BUY!")
elif total_score >= 6:
    print("RECOMMENDATION: BUY")
elif total_score >=4:
    print("RECOMMENDATION: CONSIDER")
elif total_score <3 and total_score >0:
    print("RECOMMENDATION: AVOID")
elif total_score <= 0:
    print("RECOMMENDATION: STRONG AVOID!")
else:
    print("RECOMMENDATION: STRONG AVOID!")
print(f'RECOMMENDATION DETAILS: ')

for c, value in enumerate(reasons_clean, 1): # https://www.geeksforgeeks.org/enumerate-in-python/
    print(c, value)
print(f"Total score: {total_score} of possible 14 points.")

csv_headers = {"timestamp", "open", "high", "low", "close", "volume"}

#Export to file based on stock name (and append if already exists)
with open(f'../data/prices_{entered_stock}.csv', 'a') as csvFile:
    fieldnames = ['1. open', '2. high', '3. low', '4. close', '5. volume']
    writer = csv.DictWriter(csvFile, fieldnames=csv_headers)
    writer.writeheader()
    for date in all_dates:
        price_per_day = parsed_timeseries[date]
        writer.writerow ({
            "timestamp":date,
            "open":price_per_day["1. open"],
            "high":price_per_day["2. high"],
            "low":price_per_day["3. low"],
            "close":price_per_day["4. close"],
            "volume":price_per_day["5. volume"]
        })
csvFile.close()

print('--------------------------------------')
print('GOOD LUCK INVESTING!')
print('--------------------------------------')
print('DISCLAIMER:')
print('I am not liable for any money lost')
print('due to the questionable nature of')
print('this "algorithm." That is all on you!')
print('--------------------------------------')

#Creating chart
df_highs.drop(['date_ordinal'],axis=1)
repivot = df_highs.groupby(['date'])[['high']].sum() #Forced to repivot because of a datetime issue (-0) that I couldn't figure out
fig, ax = plt.subplots()
repivot.plot(kind='line', 
                  ax=ax, 
                  figsize=(15,8), 
                  color=['mediumblue'],
                  #alpha=.8                         
                 )
ax.set_title(f'Daily High for Stock: {entered_stock.upper()}',
             size=20)

ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_position(('outward', 10))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.set_ylabel('Daily High',size=10)
ax.set_xlabel('Recorded Date',size=10)
plt.xticks(rotation=90)
plt.savefig('../data/chart_'+entered_stock+'.png')
exit()