import requests
import time
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder
import csv

winRateList = []
pickRateList = []
banRateList = []
nameList = []
roleList = []
url = "https://www.metasrc.com/lol/stats?ranks=silver" #stats list that will get me all data in silver

responseWinRate = requests.get(url) #make a get request
#for getting winrates
if responseWinRate.status_code == 200:
    data = responseWinRate.text
    parsedData = BeautifulSoup(data, 'html.parser')#convert to python object
    tableBody = parsedData.find('tbody')
    tableRows = tableBody.find_all('tr')#find all rows in the table body
    for row in tableRows:
        #find all table data
        tableData = row.find_all('td')
        #select 5th td
        winRateTD = tableData[5] #zero based indexing would tell you win rate is 5 withtin the list
        winRateTDText = winRateTD.get_text()
        winRateNoPer = winRateTDText.replace("%", "")
        winRateFloat = float(winRateNoPer) / 100
        
        winRateList.append(winRateFloat) #add to list
    print('success')
else:
    print(responseWinRate.status_code)
    print('something went wrong')
#wait before another request
time.sleep(60)

responsePickRates = requests.get(url) #make a get request
#for getting pickRates
if responseWinRate.status_code == 200:
    data = responseWinRate.text
    parsedData = BeautifulSoup(data, 'html.parser')#convert to python object
    tableBody = parsedData.find('tbody')
    tableRows = tableBody.find_all('tr')#find all rows in the table body
    for row in tableRows:
        #find all table data
        tableData = row.find_all('td')
        #select 7th td
        pickRateTD = tableData[7] #zero based indexing would tell you pick rate is 7 withtin the list
        pickRateTDText = pickRateTD.get_text()
        pickRateNoPer = pickRateTDText.replace("%", '')
        pickRateFloat = float(pickRateNoPer) / 100
        
        pickRateList.append(pickRateFloat) #add to list
    print('success')
else:
    print(responseWinRate.status_code)
    print('something went wrong')
#wait before another request
time.sleep(60)

responseBanRates = requests.get(url) #make a get request
#for getting pickRates
if responseBanRates.status_code == 200:
    data = responseWinRate.text
    parsedData = BeautifulSoup(data, 'html.parser')#convert to python object
    tableBody = parsedData.find('tbody')
    tableRows = tableBody.find_all('tr')#find all rows in the table body
    for row in tableRows:
        #find all table data
        tableData = row.find_all('td')
        #select 8th td
        banRateTD = tableData[8] #zero based indexing would tell you ban rate is 8 withtin the list
        banRateTDText = banRateTD.get_text()
        banRateNoPer = banRateTDText.replace("%", '')
        banRateFloat = float(banRateNoPer) / 100
        banRateList.append(banRateFloat) #add to list
    print('success')
else:
    print(responseBanRates.status_code)
    print('something went wrong')
#wait before another request
time.sleep(60)

responseNames = requests.get(url)
#for getting names
if responseNames.status_code == 200:
    data = responseNames.text
    parsedData = BeautifulSoup(data, 'html.parser')#convert to python object
    names = parsedData.find_all('td', class_='_byr3u7 _fs7qiw champ')#find anything table data wise with this class
    for name in names:#loop through each 
        nameLink = name.find('a')
        nameLinkText = nameLink.get_text()
        nameList.append(nameLinkText)
      
    print("success")
else:
    print(responseNames.status_code)
    print('something went wrong')
#sleep
time.sleep(60)

responseRoles = requests.get(url)
#for getting roles
if responseRoles.status_code == 200:
    data = responseRoles.text
    parsedData = BeautifulSoup(data, 'html.parser')#convert to python object
    roles = parsedData.find_all('td', class_='_byr3u7')#find anything table data wise with this class
    for role in roles:#loop through each 
        roleDiv = role.find('div')
        
        if roleDiv: #if there is a div
            divText = roleDiv.get_text()
            roles = ["TOP", "MID", "ADC", "JUNGLE", "SUPPORT"]
            if divText in roles:
                roleList.append(divText)#append to list
    print("success")
else:
    print(responseRoles.status_code)
    print('something went wrong')
time.sleep(60)



winRateListAmount = 0

#check to see if number of items in each list matches
for winRate in winRateList:
    winRateListAmount += 1
print(f"There are {winRateListAmount} items in the winRate List")

nameListAmount = 0
for item in nameList:
    nameListAmount += 1
print(f"There are {nameListAmount} items in the names List")

roleListAmount = 0
for roleItem in roleList:
    roleListAmount += 1
print(f"There are {roleListAmount} items in the role List")

pickListAmount = 0
for pickItem in pickRateList:
    pickListAmount += 1
print(f"There are {pickListAmount} items in the pick rate List")

banListAmount = 0
for banItem in banRateList:
    banListAmount += 1
print(f"There are {banListAmount} items in the ban rate List")


#write to seperate csv files. one for regular data and one for ai data
#test for creating proper list
TotalRegData = [['ChampionName', 'ChampionRole', 'ChampionWinRate', 'ChampionPickRate', 'ChampionBanRate']]


#238 items from previous calculation. put it in row format for table
for i in range(0, 238, 1):
    TotalRegData.append([nameList[i], roleList[i], winRateList[i], pickRateList[i], banRateList[i]])
    

print(TotalRegData)

#write to regular csv file
with open('MachineLearningData.csv', 'w', newline='') as regCsvFile:
    writer = csv.writer(regCsvFile, delimiter=',') #give commas
    writer.writerows(TotalRegData)



