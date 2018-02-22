import apiai
import json
import requests
from datetime import datetime, timedelta
from DatRet import *

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'
DR = DatRet()

#Need default return for if the date is in the future
def main(query):
    if query=='':
        return

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
        if datetime.strptime(date, "%Y-%m-%d")>datetime.now():
            print("At this point, I am unable to predict the future.")
            return
    except KeyError:
        pass
    except ValueError:
        pass

    time=""
    try:
        time=jsonres['result']['parameters']['time']
        print(time)
        if datetime.strptime(time, "%H:%M:%S")>datetime.now():
            print("At this point, I am unable to predict the future.")
            return
    except KeyError:
        pass
    except ValueError:
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
        if date=="" and time=="":
            print(DR.stock_price(company))
            return
        elif date=="":
            print(DR.stock_price(company, time=time))
            return
        elif time=="":
            print(DR.stock_price(company, date))
            return
        else:
            print(DR.stock_price(company, date, time))
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
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[0])
        else:
            print(DR.price_data_today(company)[0])
        return
    elif intent=="Close":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(date)
            print(DR.price_data(company, date)[1])
        else:
            print(DR.price_data_today(company)[1])
        return
    elif intent=="High":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[2])
        else:
            print(DR.price_data_today(company)[2])
        return
    elif intent=="Low":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[3])
        else:
            print(DR.price_data_today(company)[3])
        return
    elif intent=="Volume":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[4])
        else:
            print(DR.price_data_today(company)[4])
        return
    elif intent=="Percentage Change":
        #print(jsonres['result']['parameters']['date-time'])
        startdt=list(jsonres['result']['parameters']['date-time'])[0]
        print(startdt)
        try:
            enddt=list(jsonres['result']['parameters']['date-time'])[1]
        except IndexError:
            enddt=""
        print(enddt)
        #If we detect a "/", then we do the difference between the two values
        if "/" in startdt:
            #If its dates, just grab the difference between the dates
            print(DR.diff(company, start=startdt.split("/")[0], end=startdt.split("/")[1]))
            return
            #If its times, (hopefully we get dates too), and5 grab the differnces
            #Define a new value in the intent for time content(?)
        else:
            #If we don't detect a "/", and there's just one date(time), then get the difference between that date(time) and now
            if enddt=="":
                print(DR.diff(company, start=startdt))
            #If we don't detect a "/", and there are two date(times)s get the diffence between those two date(time)s 
            else:
                print(DR.diff(company, start=startdt, end=enddt))
            return
    
while True:
    main(input("\n"))
