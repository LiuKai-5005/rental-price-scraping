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

## check how many day you are interested
prices_C1 = []
prices_C2 = []
prices_C3 = []             
dates = []
# dates_C1 = []

# Ensure C:\\temp directory exists
temp_dir = 'C:\\temp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

checkStartDate = date.today()           #start date to in the report    |   or you can manually specify the start date      e.g. checkStartDate = date(2022, 1, 1)    
numOfDay = 61                           #end date in the report         |   or you can manually specify the num of days     e.g. numOfDay = 61 
checkEndDate = checkStartDate + timedelta(days = numOfDay)

for i in range(0, numOfDay + 1):
    startDate = checkStartDate + timedelta(days = i)
    endDate = startDate + timedelta(days = 14)
    
    # price = housing(startDate, endDate)
    price_C1_C2_C3 = housing(startDate, endDate)

    price_C1 = price_C1_C2_C3["C1"]
    price_C2 = price_C1_C2_C3["C2"]
    price_C3 = price_C1_C2_C3["C3"]

    dates.append(startDate)             #date time
    prices_C1.append(price_C1)            #string
    prices_C2.append(price_C2)            #string
    prices_C3.append(price_C3)            #string
    
with open('C:\\temp\\house_price_%s_%s.txt'%(checkStartDate, checkEndDate), 'a') as f:
    for i in range(len(dates)):
        f.write(str(dates[i]) + '\t' + str(prices_C3[i]) + '\t' + str(prices_C2[i]) + '\t' + str(prices_C1[i]) + '\n')
f.close()

# plot 
plt.figure(figsize=(9, 6))
# plt.plot(dates, prices_C3,'bo-', dates, prices_C2, 'g+-', dates, price_C1, 'rx-')
plt.plot(dates, prices_C3,'bo-')
plt.xlabel('Dates (Time))')
plt.ylabel('Prices ($)')
# plt.legend("C3", "C2", "C1")
plt.legend(["C3"])
plt.title("The rental Price of Century Towers -- Floor Plan : C3")
# plt.show()
plt.savefig('C:\\temp\\house_price_%s_%s.png' % (checkStartDate, checkEndDate))

# print(dates,prices)
# print(dict)

## check 60 days in the future
# ans = []
# for i in range(1, 61):
#     startDate = startDate + timedelta(days = i)
#     ans.append(housing(startDate, endDate))
# print(ans)
