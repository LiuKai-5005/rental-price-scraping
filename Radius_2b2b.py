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
    url = 'https://www.essexapartmenthomes.com/EPT_Feature/PropertyManagement/Service/GetPropertyAvailabiltyByRange/513957/' + str(startDate)[:10] + '/' + str(endDate)[:10]
    response = requests.get(url)
    houseResponseStr = json.loads(response.content)
    houseResponse = json.loads(houseResponseStr)
    floorPlans = houseResponse["result"]["floorplans"]
    result = {}
    for i in range(len(floorPlans)):
        if floorPlans[i]["name"] == "Ratio":
            result["Ratio"] = float(floorPlans[i]["minimum_rent"])
        elif floorPlans[i]["name"] == "Locus":
            result["Locus"] = float(floorPlans[i]["minimum_rent"])
        elif floorPlans[i]["name"] == "Apex":
            result["Apex"] = float(floorPlans[i]["minimum_rent"])
        elif floorPlans[i]["name"] == "Chord":
            result["Chord"] = float(floorPlans[i]["minimum_rent"])
    return result

## check how many day you are interested
prices_Ratio = []
prices_Locus = []
prices_Apex = []
prices_Chord = []
dates = []

checkStartDate = date.today()           #start date to in the report    |   or you can manually specify the start date      e.g. checkStartDate = date(2022, 1, 1)    
numOfDay = 61                           #end date in the report         |   or you can manually specify the num of days     e.g. numOfDay = 61 
checkEndDate = checkStartDate + timedelta(days = numOfDay)

for i in range(0, numOfDay + 1):
    startDate = checkStartDate + timedelta(days = i)
    endDate = startDate + timedelta(days = 14)
    price_dict = housing(startDate, endDate)
    price_Ratio = price_dict.get("Ratio", None)
    price_Locus = price_dict.get("Locus", None)
    price_Apex = price_dict.get("Apex", None)
    price_Chord = price_dict.get("Chord", None)
    dates.append(startDate)
    prices_Ratio.append(price_Ratio)
    prices_Locus.append(price_Locus)
    prices_Apex.append(price_Apex)
    prices_Chord.append(price_Chord)

# Define output directory and file prefix
output_dir = os.path.join(os.path.dirname(__file__), 'Radius')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_prefix = os.path.join(output_dir, 'house_price')


import csv
# Output results as CSV with schema
csv_path = f'{output_prefix}_{checkStartDate}_{checkEndDate}.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'Ratio', 'Locus', 'Apex', 'Chord'])
    for i in range(len(dates)):
        writer.writerow([str(dates[i]), prices_Ratio[i], prices_Locus[i], prices_Apex[i], prices_Chord[i]])

# plot 

# Filter out zero prices for plotting
plot_dates = []
plot_Ratio = []
plot_Locus = []
plot_Apex = []
plot_Chord = []
for i in range(len(dates)):
    valid = False
    vals = []
    for val in [prices_Ratio[i], prices_Locus[i], prices_Apex[i], prices_Chord[i]]:
        if val is not None and val != 0:
            valid = True
        vals.append(val if val is not None and val != 0 else None)
    if valid:
        plot_dates.append(dates[i])
        plot_Ratio.append(vals[0])
        plot_Locus.append(vals[1])
        plot_Apex.append(vals[2])
        plot_Chord.append(vals[3])

plt.figure(figsize=(18, 6))
if any(plot_Ratio) or any(plot_Locus) or any(plot_Apex) or any(plot_Chord):
    if any(plot_Ratio):
        plt.plot(plot_dates, plot_Ratio, 'bo-', label='Ratio')
    if any(plot_Locus):
        plt.plot(plot_dates, plot_Locus, 'g+-', label='Locus')
    if any(plot_Apex):
        plt.plot(plot_dates, plot_Apex, 'rx-', label='Apex')
    if any(plot_Chord):
        plt.plot(plot_dates, plot_Chord, 'ms-', label='Chord')
    plt.xlabel('Dates (Time)')
    plt.ylabel('Prices ($)')
    plt.legend()
    plt.title("The rental Price of Radius -- Floor Plans: Ratio, Locus, Apex, Chord")
    plt.savefig(f'{output_prefix}_{checkStartDate}_{checkEndDate}.png')
