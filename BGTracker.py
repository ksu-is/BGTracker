from lxml import html
import requests
from os import listdir
from datetime import datetime
import time


# Class to hold the Board Game Info
class BGI:
    def __init__(self, BGID = ''):
        self.name = ''
        self.BGID = BGID
        self.rPrice = ''
        self.sPrice = ''
        self.stock = ''
        

#this function does the actual scraping
def scrapeData(BGID):
    # sPrice is initialized no matter what, in case there is no special price
    sPrice = ''

    url = "https://www.miniaturemarket.com/" + BGID + ".html"
    url = url.lower()
    r = requests.get(url)
    tree = html.fromstring(r.content)

    name = tree.find_class('product-name')[0].text_content()
    prices = tree.find_class('price')

    # Both regular and special prices are stored together. Regular price is stored in the first element. 
    # If there is a special price, it is stored in the second element
    if len(prices) == 2:
        rPrice = prices[0].text_content()
        sPrice = prices[1].text_content()
    else:
        rPrice = prices[0].text_content()
    
    # Multiple different availability classes across the site, but a product can only have 1 at a time
    # the different classes are: availablility out-of-stock, availablility in-stock, availability preorder
    stock = tree.find_class('availability')[0].text_content()
    
    BGData = BGI(BGID)
    BGData.name = name
    BGData.sPrice = sPrice
    BGData.rPrice = rPrice
    BGData.stock = stock
    return BGData


BGlist = []
filePath = 'BGTracker/'
filesExisting = listdir(filePath)

#This for loop adds the tracked games from previous sessions
for i in range(len(filesExisting)):
    if '.txt' in filesExisting[i]:
        BGlist.append(BGI(filesExisting[i][:-4])) # [:-4 to remove the .txt]


menuInput = 0
while menuInput != 'q':
    print("\n1: Track new game")
    print("2: Show currently tracked product IDs")
    print("Q to begin tracking\n")
    
    menuInput = input("Select a menu item: ").lower()
    if menuInput == '1':
        print("Here is a list of currently tracked board games: ")
        if len(BGlist) < 1:
            print("No board games currently being tracked\n")
        else:
            for games in BGlist:
                print (games.BGID)

        while True:
            usrInput = input("Enter the product # located below the name, or press q to return to menu: ")
            if usrInput[0] == '#':
                usrInput = usrInput[1:]
            elif usrInput == 'q':
                break
            
            BGlist.append(BGI(usrInput))
    elif menuInput == '2':
        if len(BGlist) < 1:
                print('No board games currently being tracked\n')
        for IDs in BGlist:
            print(IDs.BGID)
        input("Press any button to continue")
    elif menuInput == 'q':
        break

    
# creates files and enters data from previous sessions
fileList = []
for i in range(len(BGlist)):
    file = open(filePath + BGlist[i].BGID + '.txt', 'a+')
    fileList.append(file)

    lineNum = file.readlines()
    if len(lineNum) >= 5:
        BGlist[i].name = lineNum[-6]
        BGlist[i].rPrice = lineNum[-4]
        BGlist[i].sPrice = lineNum[-3]
        BGlist[i].stock = lineNum[-2]



while True:
    # Scrapes the data then checks to see if anything has changed. If so, the changes are written to the corresponding file. 
    for i in range(len(BGlist)):
        currentData = BGlist[i]
        newData = scrapeData(BGlist[i].BGID)

        if currentData != newData:
            fileList[i].write(newData.name.strip() + '\n' + newData.BGID.strip() + '\n' + newData.rPrice.strip() + '\n' + newData.sPrice.strip() + '\n' + newData.stock.strip() + '\n' + str(datetime.now()))

            BGlist[i] = newData
    
    time.sleep(900) # Wait for 900 seconds (15 minutes)
    


