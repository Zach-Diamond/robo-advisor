# shopping_cart.py

import os
from datetime import datetime
from pprint import pprint

import numpy as np
from pandas import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def to_usd(my_price):  
    return "${0:,.2f}".format(my_price)

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
 ] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

#####ESTABLISHING BASLINES#####

#Initializing empty list for user inputs
user_list = []

#Creating "viable" options and converting to string
viable = [p["id"] for p in products]
viable.append("done")
viable = str(viable)


#####USER INPUT SECTION#####

#First user input
user_input = input("Please input a Product ID or type DONE: ").lower()

#If you immediately type DONE, cancel and quit.
if user_input.lower() == "done":
    print("TRANSCATION CANCELLED.")
    quit()

#Check users input against viable options, otherwise append
if user_input not in viable or len(user_input)==0:
    print("ID not recognized. Please try again.")
else:
    user_list.append(user_input)

#Second input. If not viable, get to viable, otherwise append.
while user_input != "done":
    user_input = input("Please input another Product ID or type DONE: ").lower()
    if user_input not in viable or len(user_input)==0:
        print ('ID not recognized. Please try again.')
    else: user_list.append(user_input)
else:
    print("")

#Remove "Done" from list, reduce id by 1 to fix error in iterable.
user_list.remove('done')
user_list = [(int(i)-1) for i in user_list]

#####RECEIPT PRINTING SECTION#####

print("------------------------------------------")
print("PROBABLY FRESH GROCERS")
print('"Guaranteed To Be Somewhat Fresh!"')
print("WWW.PROBABLY-FRESH.EDU")
print("------------------------------------------")
print(f"CHECKOUT AT: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}") #24 hour time:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S ')}")
print("------------------------------------------")
print("SELECTED PRODUCTS:")

#Creating receipt output (... Name  ($123))

for i in user_list:
    price_usd = to_usd(products[int(i)]['price'])
    print(f" ... {products[int(i)]['name']}  ({price_usd})")

#Adding a total price list
chosen_prices = []
[chosen_prices.append(products[int(i)]['price']) for i in user_list]

#Setting Tax Rate (8.75%)
taxrate = .0875
taxincrease = 1.0875

#Simple Tax (8.875%)
tax = []
[tax.append(i*taxrate) for i in chosen_prices]

#Increasing by Tax Rate (8.875%)
tax_plus_price = []
[tax_plus_price.append(i*taxincrease) for i in chosen_prices]

#Sum and print total price and tax 
total_price = to_usd(np.sum(chosen_prices))
total_tax = to_usd(np.sum(tax))
total_price_tax = to_usd(np.sum(tax_plus_price))

#Printing totals
print("------------------------------------------")

print("SUBTOTAL: "+total_price)
print("TAX: "+total_tax)
print("TOTAL: "+total_price_tax)

print("------------------------------------------")
print("THANKS, SEE YOU AGAIN SOON! NO RETURNS!")
print("------------------------------------------")

# exporttime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
# # filename = "exporttime+.txt"
# # with open(filename, "w") as file:
# #     file.write("Hello World")



# #input('Would you like an e-mail copy of this receipt? Type YES or NO: ').lower()

# MY_ADDRESS = '@gmail.com'
# CUSTOMER_ADDRESS = '@gmail.com'
# SENDGRID_API_KEY = '' 
# SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
# client = SendGridAPIClient(SENDGRID_API_KEY) 
# print("CLIENT:", type(client))


# from_email=MY_ADDRESS,
# to_emails=CUSTOMER_ADDRESS,
# subject='Your Receipt from Probably Fresh Grocers'
# html_list_items = "<li>You ordered: Product 1</li>"
# html_list_items += "<li>You ordered: Product 2</li>"
# html_list_items += "<li>You ordered: Product 3</li>"
# html_content = f"""
# <h3>Here is your Receipt</h3>
# <p>Date of Transaction: {exporttime}</p>
# <ol>
# {html_list_items}
# </ol>
# """
# print("HTML:", html_content)

# message = Mail(from_email=MY_ADDRESS, to_emails=CUSTOMER_ADDRESS, subject=subject, html_content=html_content)

# try:
#     response = client.send(message)

#     print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
#     print(response.status_code) #> 202 indicates SUCCESS
#     print(response.body)
#     print(response.headers)

# except Exception as e:
#     print("OOPS", e.message)