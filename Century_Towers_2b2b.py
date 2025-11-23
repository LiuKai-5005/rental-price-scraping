# save this as app.py
from flask import Flask
import json
import requests
import datetime  
import os
from datetime import date, timedelta
import matplotlib.pyplot as plt

app = Flask(__name__)
@app.route('/housing', methods=['GET'])
def housing(startDate, endDate):
    url = 'https://www.essexapartmenthomes.com/EPT_Feature/PropertyManagement/Service/GetPropertyAvailabiltyByRange/543205/' + str(startDate)[:10] + '/' + str(endDate)[:10]
    response = requests.get(url)
    houseResponseStr = json.loads(response.content)
    # print(houseResponseStr)
    houseResponse = json.loads(houseResponseStr)
    floorPlans = houseResponse["result"]["floorplans"]
    dict = {}
    for i in range(len(floorPlans)):
        if floorPlans[i]["name"] == "C3":
            dict["C3"] = float(floorPlans[i]["minimum_rent"])
            # return float(floorPlans[i]["minimum_rent"])
        elif floorPlans[i]["name"] == "C2":
            dict["C2"] = float(floorPlans[i]["minimum_rent"])
        elif floorPlans[i]["name"] == "C1":
            dict["C1"] = float(floorPlans[i]["minimum_rent"])
    return dict

dates = []

# Collect price data for each day of interest
prices_C1 = []
prices_C2 = []
prices_C3 = []             
dates = []
# dates_C1 = []


# Output directory: relative Century_Towers folder under project
temp_dir = os.path.join(os.path.dirname(__file__), 'Century_Towers')
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)


# Start date for report; can be manually specified, e.g. checkStartDate = date(2022, 1, 1)
checkStartDate = date.today()
# Number of days to check; can be manually specified, e.g. numOfDay = 61
numOfDay = 61
checkEndDate = checkStartDate + timedelta(days = numOfDay)


for i in range(0, numOfDay + 1):
    startDate = checkStartDate + timedelta(days = i)
    endDate = startDate + timedelta(days = 14)
    # Get prices for each floor plan
    price_C1_C2_C3 = housing(startDate, endDate)

    price_C1 = price_C1_C2_C3["C1"]
    price_C2 = price_C1_C2_C3["C2"]
    price_C3 = price_C1_C2_C3["C3"]

    dates.append(startDate)             # date
    prices_C1.append(price_C1)          # price for C1
    prices_C2.append(price_C2)          # price for C2
    prices_C3.append(price_C3)          # price for C3


# Write results to CSV file with schema header
import csv
csv_path = os.path.join(temp_dir, 'house_price_%s_%s.csv' % (checkStartDate, checkEndDate))
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'C3', 'C2', 'C1'])
    for i in range(len(dates)):
        pip install tqdm        writer.writerow([str(dates[i]), prices_C3[i], prices_C2[i], prices_C1[i]])


# Filter out zero prices for plotting
plot_dates = []
plot_C1 = []
plot_C2 = []
plot_C3 = []
for i in range(len(dates)):
    valid = False
    vals = []
    for val in [prices_C1[i], prices_C2[i], prices_C3[i]]:
        if val is not None and val != 0:
            valid = True
        vals.append(val if val is not None and val != 0 else None)
    if valid:
        plot_dates.append(dates[i])
        plot_C1.append(vals[0])
        plot_C2.append(vals[1])
        plot_C3.append(vals[2])

# Make the plot
plt.figure(figsize=(18, 6))
if any(plot_C1) or any(plot_C2) or any(plot_C3):
    if any(plot_C3):
        plt.plot(plot_dates, plot_C3, 'bo-', label='C3')
    if any(plot_C2):
        plt.plot(plot_dates, plot_C2, 'g+-', label='C2')
    if any(plot_C1):
        plt.plot(plot_dates, plot_C1, 'rx-', label='C1')
    plt.xlabel('Dates (Time)')
    plt.ylabel('Prices ($)')
    plt.legend()
    plt.title("The rental Price of Century Towers -- Floor Plans: C1, C2, C3")
    plt.savefig(os.path.join(temp_dir, 'house_price_%s_%s.png' % (checkStartDate, checkEndDate)))

# Output CSV file with metadata schema
import csv
csv_path = os.path.join(temp_dir, 'house_price_%s_%s.csv' % (checkStartDate, checkEndDate))
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'C3', 'C2', 'C1'])
    for i in range(len(dates)):
        writer.writerow([str(dates[i]), prices_C3[i], prices_C2[i], prices_C1[i]])

