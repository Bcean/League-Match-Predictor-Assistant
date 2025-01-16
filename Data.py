import requests
import time
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder
import csv

winRateList = []
nameList = []
roleList = []
url = "https://www.metasrc.com/lol/stats" #stats list that will get me all data

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
        
        
        winRateList.append(winRateTDText) #add to list
    print('success')
else:
    print(responseWinRate.status_code)
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

#encode every champion name and role for machine learning

nameEncoder = LabelEncoder()

encodedNames = nameEncoder.fit_transform(nameList)

roleEncoder = LabelEncoder()

encodedRoles = roleEncoder.fit_transform(roleList)

print(winRateList)
print(nameList)
print(encodedNames)
print(roleList)
print(encodedRoles)

#write to seperate csv files. one for regular data and one for ai data
#test for creating proper list
TotalRegData = [['ChampionName', 'ChampionRole', 'ChampionWinRate']]
MachineData = [['ChampionName', 'ChampionRole', 'ChampionWinRate']]

#251 items from previous calculation. put it in row format for table
for i in range(0, 251, 1):
    TotalRegData.append([nameList[i], roleList[i], winRateList[i]])
    MachineData.append([encodedNames[i], encodedRoles[i], winRateList[i]])

print(TotalRegData)

#write to regular csv file
with open('RegChampData.csv', 'w', newline='') as regCsvFile:
    writer = csv.writer(regCsvFile, delimiter=',') #give commas
    writer.writerows(TotalRegData)

#write to machine csv file

with open('MachineLearningData.csv', 'w', newline='') as MachineCsvFile:
    Mwriter = csv.writer(MachineCsvFile, delimiter=',') #give commas
    Mwriter.writerows(MachineData)

