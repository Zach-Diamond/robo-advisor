# app/robo_advisor.py

from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)  
    #https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

apikey = os.environ.get("ALPHAVANTAGE_API_KEY")


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

entered_stock = input('Please type a stock symbol and press ENTER: ').lower()

while (
len(entered_stock) > 5 
or len(entered_stock) < 1 
or hasNumbers(entered_stock)==True
):
    entered_stock = input("Invalid entry. Please type a stock symbol and press ENTER: ").lower()
else: print(f"Selected Stock: {entered_stock.upper()}")


request_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={entered_stock}&apikey={apikey}'
response = requests.get(request_url)
parsed_response = json.loads(response.text)

print(response.text)

#Call API key via .env file (dotenv)

