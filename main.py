import apiai
import json
import requests
from datetime import datetime, timedelta
from DatRet import *
from NewsSentiment import *
from AI import *

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'
DR = DatRet()
NS = NewsSentiment()
a = AI()

##TO DO##
#Correct line breaks in news return
#Perhaps allow high/low/close/open be over a period? (ie. Was was the high price of BP last week?)
#Change since market opened (ALSO MAKE SURE NO REQUESTED DATES ARE BEFORE THESE ONES)


def main(query):
    if query=='':
        return

    ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request=ai.text_request()
    request.lang='en'
    request.session_id="1"
    request.query=query
    res=request.getresponse()

    jsonres=json.loads(res.read().decode())

    company=""
    try:
        company=jsonres['result']['parameters']['companies'].strip(".")
        if company != "":
            a.addQuery(company)
    except KeyError:
        pass

    sector=""
    try:
        sector=jsonres['result']['parameters']['sectors']
    except KeyError:
        pass

    date=""
    try:
        date=jsonres['result']['parameters']['date']
        print(date)
        if datetime.strptime(date, "%Y-%m-%d")>datetime.now():
            print("At this point, I am unable to predict the future.")
            return ("At this point, I am unable to predict the future.")
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
            return ("At this point, I am unable to predict the future.")
    except KeyError:
        pass
    except ValueError:
        pass

    if company=="" and sector=="":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return default
    else:
        if sector=="":
            print("company:"+company)
        else:
            print("sector:"+sector)

    intent=jsonres['result']['metadata']['intentName']
    if intent=="Default Fallback Intent" or intent=="Default Welcome Intent":
        default=jsonres['result']['fulfillment']['speech']
        print(default)
        return default
    else:
        print("intent:"+intent)

    #If we've reached this point, we have a company and intent (and myb date)
    #Wrap all of this in a try catch and excuse ourselves for not having the data?
    if intent=="Spot Price":
        if date=="" and time=="":
            print(DR.stock_price(company))
            return "The current spot price of "+company+" is £"+str(DR.stock_price(company))
        elif date=="":
            print(DR.stock_price(company, time=time))
            return "The spot price of "+company+" at "+time+" was £"+str(DR.stock_price(company, time=time))
        elif time=="":
            print(DR.stock_price(company, date))
            return "The spot price of "+company+" on "+date+" was £"+str(DR.stock_price(company, date))
        else:
            print(DR.stock_price(company, date, time))
            return "The spot price of "+company+" on "+date+" at "+time+" was £"+str(DR.stock_price(company, date, time))
    elif intent=="Market Capitalisation":
        print(DR.current_marketcap(company))
        return "The current Market Capitalisation of "+company+" is £"+str(DR.current_marketcap(company))
    elif intent=="retrieve-news-company":
        returnstring="Here's the news on "+company+": \n"
        for article in DR.get_news(company):
            print("URL:"+article['u'])
            print("Snippit:"+article['sp'])
            polarity=NS.getPolarity(article['u'])
            print(polarity)

            returnstring+=article['u']+" \n"
            returnstring+=article['sp']+" \n"
            returnstring+=polarity+" \n"
        return returnstring
    elif intent=="retrieve-news-sector":
        returnstring="Here's the news on "+sector+": \n"
        for article in DR.get_news_cat(sector):
            print("URL:"+article['u'])
            print("Snippit:"+article['sp'])
            polarity=NS.getPolarity(article['u'])
            print(polarity)
            returnstring+=article['company']+"\n"
            returnstring+=article['u']+" \n"
            returnstring+=article['sp']+" \n"
            returnstring+=polarity+" \n"
        return returnstring
    elif intent=="Open":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[0])
            return "The open price of "+company+" on "+date+" was £"+str(DR.price_data(company, date)[0])
        else:
            print(DR.price_data_today(company)[0])
            return "The opening price of "+company+" today was £"+str(DR.price_data_today(company)[0])
    elif intent=="Close":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(date)
            print(DR.price_data(company, date)[1])
            return "The close price of "+company+" on "+date+" was £"+str(DR.price_data(company, date)[1])
        else:
            print(DR.price_data_today(company)[1])
            return "The close price of "+company+" today was £"+str(DR.price_data_today(company)[1])
    elif intent=="High":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[2])
            return "The high price of "+company+" on "+date+" was £"+str(DR.price_data(company, date)[2])
        else:
            print(DR.price_data_today(company)[2])
            return "The high price of "+company+" today was £"+str(DR.price_data_today(company)[2])
        return
    elif intent=="Low":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[3])
            return "The low price of "+company+" on "+date+" was £"+str(DR.price_data(company, date)[3])
        else:
            print(DR.price_data_today(company)[3])
            return "The low price of "+company+" today was £"+str(DR.price_data_today(company)[3])
    elif intent=="Volume":
        if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"):
            print(DR.price_data(company, date)[4])
            return "The volume traded of "+company+" on "+date+" was "+str(DR.price_data(company, date)[4])
        else:
            print(DR.price_data_today(company)[4])
            return "The volume traded of "+company+" today is "+str(DR.price_data_today(company)[4])
    elif intent=="Percentage Change":
        listinput=list(jsonres['result']['parameters']['date-time'])
        if listinput==[]:
            default=jsonres['result']['fulfillment']['speech']
            print(default)
            return default
        startenddates=extract_diff_dates(listinput)
        print(startenddates)
        startdt=startenddates[0]
        enddt=startenddates[1]

        if startdt==(datetime.now()).strftime("%Y-%m-%d"):
            startdt=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

        if enddt=="":
            print(DR.diff(company, start=startdt))
            return "Since "+startdt+", "+company+" has had a £"+str(DR.diff(company, start=startdt)[0])+" price change, and a "+str(DR.diff(company, start=startdt)[1])+"% change"
        else:
            print(DR.diff(company, start=startdt, end=enddt))
            return "Between "+startdt+" and "+enddt+", "+company+" has had a £"+str(DR.diff(company, start=startdt, end=enddt)[0])+" price change, and a "+str(DR.diff(company, start=startdt, end=enddt)[1])+"% change"
    return ("This is the catch-all return at the end of the main function")

#Function for determining start/end dates of difference function
def extract_diff_dates(listinput):
    startdt=listinput[0]
    try:
        enddt=listinput[1]
    except IndexError:
        enddt=""
    if "/" in startdt:
        enddt=startdt.split("/")[1]
        startdt=startdt.split("/")[0]
    return (startdt, enddt)

def suggestCategories():
    return a.suggestCategories(3)

def detectAnomalies():
    anomalies = a.detectAnomalies()
    return anomalies

def writeToFile():
    a.writeToFile()
    return
#while True:
#    main(input("\n"))
