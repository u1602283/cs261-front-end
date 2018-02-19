import apiai
import json
import requests
from datetime import datetime, timedelta
from DatRet import *

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'
DR = DatRet()

def main(query):
    ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request=ai.text_request()
    request.lang='en'
    request.session_id="1"
    request.query=query
    res=request.getresponse()

    jsonres=json.loads(res.read())

    company=""
    try:
        company=jsonres['result']['parameters']['companies'].strip(".")
    except KeyError:
        pass

    date=""
    try:
        date=jsonres['result']['parameters']['date']
        print(date)
    except KeyError:
        pass
        
    if company=="":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return
    else:
        print("company:"+company)
            
    intent=jsonres['result']['metadata']['intentName']
    if intent=="Default Fallback Intent" or intent=="Default Welcome Intent":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return
    else:
        print("intent:"+intent)

    #If we've reached this point, we have a company and intent (and myb date)
    #Wrap all of this in a try catch and excuse ourselves for not having the data?
    #What do we do if they request the closing/opening on a weekend?
    #need to make sure date isn't in the future!
    if intent=="Spot Price":
        if date=="":
            print(DR.stock_price(company))
            return
        else:
            print(DR.stock_price(company, date))
            return
    elif intent=="Market Capitalisation":
        print(DR.current_marketcap(company))
        return
    elif intent=="retrieve-news-company":
        for article in DR.get_news(company):
            print("URL:"+article['u'])
            print("Snippit:"+article['sp'])
        return
    elif intent=="Open":
        print(DR.price_data(company, date)[0])
        return
    elif intent=="Close":
        print(DR.price_data(company, date)[1])
        return
    elif intent=="High":
        print(DR.price_data(company, date)[2])
        return
    elif intent=="Low":
        print(DR.price_data(company, date)[3])
        return
    elif intent=="Volume":
        if date!="":
            print(DR.price_data(company, date)[4])
        else:
            #Want the 24hr volume from yesterday
            #NEEDS WORK
            print(DR.price_data(company, (datetime.now()).strftime("%Y-%m-%d"))[4])
        return
        
while True:
    main(input("\n"))
