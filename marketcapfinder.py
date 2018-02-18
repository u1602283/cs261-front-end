from bs4 import BeautifulSoup
import requests
import json
import re

def get_market_cap(symbol, exch):
    url="https://finance.google.com/finance?q="+exch+":"+symbol
    content=requests.get(url)
    soup=BeautifulSoup(content.text, "html.parser")

    tds=soup.select('td')
    trigger=False
    data=''
    for item in tds:
        if trigger:
            data=item
            break
        if 'data-snapfield="market_cap"' in str(item):
            trigger=True
    #print(data)
    #print(str(data)[str(data).find('>')+1:str(data)[1:].find('<')+1])
    return (str(data)[str(data).find('>')+1:str(data)[1:].find('<')+1])

