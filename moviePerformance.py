#Primary goal: Make methods
#First: Append every animated and live action title to two different lists
#Second: Check for substrings between animated and live action titles to see if it's a live action remake. If so append to final list.
#Third: Go to the specific Wikipedia page of each title
#Fourth: Scrape the table and see if there is both a budget and box office performance
#Fifth: If both conditions are met ((len(ref) == 1), then the program will append them to an array for budgets

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

str = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'
source = 'https://en.wikipedia.org{}'

anTitle = [] #list to hold animated film titles
anUrls = [] #list to hold animated film title urls
laTitle = [] #list of live action film titles
laUrls = [] #list to hold animated film title urls
filmType = []
release = []
budget = []
box = []

r = requests.get(str)
soup = bs(r.text, 'html.parser')

soup = soup.find_all('table', {'class': 'wikitable sortable'})

tableID = list(range(0,1))

tables = []

for table in tableID:
    tables.append(soup[table])

    # print(tables)
    # print('')
    for tag in tables:
        count = 0
        for td in tag.find_all('td'):
            idx = tag.find_all('td').index(td)
            if(idx == 0):
                small = td.find('small').text
                filmType.append(small)
                for a in tag.find_all('a'):
                    if((small == 'A') & (count < 2)):
                        idx = tag.find_all('a').index(a)
                        anUrls.append(source.format(a['href']))
                    elif((small == 'L') & (count < 2)):
                        idx = tag.find_all('a').index(a)
                        laUrls.append(source.format(a['href']))
                    count = count + 1 #  counter to prevent server overload
            counter = 0
            if(idx == 2):
                if(counter<1):
                    date = td.text
                    date = date.replace('\n', '')
                    release.append(date)
                else:
                    break
                counter = counter + 1


count = 0
row = []
for titles in anUrls:
    r = requests.get(titles)
    soup = bs(r.text, 'html.parser')
    soup = soup.find_all('table', {'class': 'infobox vevent'})
    for tag in soup:
        for td in tag.find_all('td'):
            if(count == 1):
                row = [t.text for t in td.find_all('sup', {'class': 'reference'})]
            row = list(filter(None, row))
            print(row)
        # ref = td.find_all('sup', {'class': 'reference'})
        print('')
        # print(len(ref))


        # if((len(ref) == 1)):
        #     budget.append(td[0])
        #     box.append(td[1])
        # elif((len(ref) == 0)):
        #     box.append(td[0])
        # print(budget)
        # print(box)
    count = count + 1

    title = titles.replace('/', '').replace('wiki','').replace('_', ' ').replace('https:en.pedia.org', '')
    anTitle.append(title)


print(filmType)
print(anTitle)
print(release)
print(anUrls)
print(budget)
print(box)






