import apiai
import json
import requests
from datetime import datetime, timedelta
from DatRet import *
from NewsSentiment import *
from AI import *
from Dict import code_cat

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'
DR = DatRet()
NS = NewsSentiment()
a = AI()

##TO DO##
#Correct line breaks in news return
#Perhaps allow high/low/close/open be over a period? (ie. Was was the high price of BP last week?)
#Change since market opened (ALSO MAKE SURE NO REQUESTED DATES ARE BEFORE THESE ONES)

"""
Generates response to user based on given query

Args:
	query: The query obtained from the user

Returns:
	A string to be displayed to the user in the form of HTML
"""
def main(query):

		ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
		request=ai.text_request()
		request.lang='en'
		request.session_id="1"
		request.query=query
		res=request.getresponse()
		
		#Attempt to identify components of query
		jsonres=json.loads(res.read().decode())

		#Identify company within query
		company=""
		try:
				company=jsonres['result']['parameters']['companies'].strip(".")
				if company != "":
						a.addQuery(company)
		except KeyError:
				pass

		#Identify sector within query
		sector=""
		try:
				sector=jsonres['result']['parameters']['sectors']
		except KeyError:
				pass
				
		#Identify date within query
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

		#Identify time within query
		time=""
		try:
				time=jsonres['result']['parameters']['time']
				print(time)
				#Handler for queries about the future
				if datetime.strptime(time, "%H:%M:%S")>datetime.now():
						print("At this point, I am unable to predict the future.")
						return ("At this point, I am unable to predict the future.")
		except KeyError:
				pass
		except ValueError:
				pass

		#No specified company and sector
		if company=="" and sector=="":
				default=jsonres['result']['fulfillment']['speech']
				print(default)
				return default
		else:
				if sector=="":
						print("company:"+company)
				else:
						print("sector:"+sector)

		#Identify intent of query
		intent=jsonres['result']['metadata']['intentName']
		if intent=="Default Fallback Intent" or intent=="Default Welcome Intent":
				default=jsonres['result']['fulfillment']['speech']
				print(default)
				return default
		else:
				print("intent:"+intent)

		#If we've reached this point, we have a company and intent (and possibly date)
		#Wrap all of this in a try catch and excuse ourselves for not having the data?
		
		#Retrieving spot price
		if intent=="Spot Price":
				if date=="" and time=="": #No specified data and time
						#print(DR.stock_price(company))
						return "The current spot price of "+company+" is "+str(DR.stock_price(company))+"GBX"
				elif date=="": #Specified time
						#print(DR.stock_price(company, time=time))
						return "The spot price of "+company+" at "+time+" was "+str(DR.stock_price(company, time=time))+"GBX"
				elif time=="": #Specified date
						#print(DR.stock_price(company, date))
						return "The spot price of "+company+" on "+date+" was "+str(DR.stock_price(company, date))+"GBX"
				else: #Specified date and time
						#print(DR.stock_price(company, date, time))
						return "The spot price of "+company+" on "+date+" at "+time+" was "+str(DR.stock_price(company, date, time))+"GBX"
						
		#Retrieving market capitalisation
		elif intent=="Market Capitalisation":
				#print(DR.current_marketcap(company))
				return "The current Market Capitalisation of "+company+" is £"+str(DR.current_marketcap(company))
				
		#Retrieving news on given company
		elif intent=="retrieve-news-company":
				returnstring="Here's some news on "+company+"<br />"
				for article in DR.get_news(company): #For each obtained article
						print("URL:"+article['u'])
						print("Snippit:"+article['sp'])
						score=NS.getScore(article['u'])
						print("Score: "+str(score))

						returnstring+=" <a href = '"+article['u']+"' target='_blank'>"+article['t']+"</a>:<br />"+article['sp']+" - "+article['s']+"<br />This article seems to be "+str(round(score*100, 1))+"% "
						if score < 0:
								returnstring+="negative"
						else:
								returnstring+="positive"
						returnstring+="<br />"
				return returnstring
				
		#Retrieving news on sector
		elif intent=="retrieve-news-sector":
				returnstring="Here's some news on "+sector+"<br />"
				for article in DR.get_news_cat(sector):
						print("URL:"+article['u'])
						print("Snippit:"+article['sp'])
						symbol=NS.getSymbol(article['u'])
						print(symbol)
						returnstring+=symbol
						returnstring+=" <a href = '"
						returnstring+=article['u']
						returnstring+="' target='_blank'>"
						returnstring+=article['company']+"</a> - "+article['s']+" | "
						returnstring+=article['d']
						returnstring+="<br />"
						print(article)
				return returnstring
				
		#Retrieving open price
		elif intent=="Open":
				if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"): #Not today
						#print(DR.price_data(company, date)[0])
						return "The open price of "+company+" on "+date+" was "+str(DR.price_data(company, date)[0])+"GBX"
				else: #Today
						#print(DR.price_data_today(company)[0])
						return "The opening price of "+company+" today was "+str(DR.price_data_today(company)[0])+"GBX"
						
		#Retrieving close price
		elif intent=="Close":
				if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"): #Not today
						print(date)
						#print(DR.price_data(company, date)[1])
						return "The close price of "+company+" on "+date+" was "+str(DR.price_data(company, date)[1])+"GBX"
				else: #Today
						#print(DR.price_data_today(company)[1])
						return "The close price of "+company+" today was "+str(DR.price_data_today(company)[1])+"GBX"
						
		#Retrieving high price
		elif intent=="High":
				if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"): #Not today
						#print(DR.price_data(company, date)[2])
						return "The high price of "+company+" on "+date+" was "+str(DR.price_data(company, date)[2])+"GBX"
				else: #Today
						#print(DR.price_data_today(company)[2])
						return "The high price of "+company+" today was "+str(DR.price_data_today(company)[2])+"GBX"
						
		#Retrieving low price
		elif intent=="Low":
				if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"): #Not today
						#print(DR.price_data(company, date)[3])
						return "The low price of "+company+" on "+date+" was "+str(DR.price_data(company, date)[3])+"GBX"
				else: #Today
						#print(DR.price_data_today(company)[3])
						return "The low price of "+company+" today was "+str(DR.price_data_today(company)[3])+"GBX"
						
		#Retrieving volume
		elif intent=="Volume":
				if date!="" and date!=(datetime.now()).strftime("%Y-%m-%d"): #Not today
						#print(DR.price_data(company, date)[4])
						return "The volume traded of "+company+" on "+date+" was "+str(DR.price_data(company, date)[4])
				else: #Today
						#print(DR.price_data_today(company)[4])
						return "The volume traded of "+company+" today is "+str(DR.price_data_today(company)[4])
						
		#Retrieving percentage change
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

				if startdt==(datetime.now()).strftime("%Y-%m-%d"): #Start date is specified to be now
						startdt=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d") #Set start to yesterday

				if enddt=="": #No specified end date
						#print(DR.diff(company, start=startdt))
						data = DR.diff(company, start=startdt)
						if data[0] > 0:
								return "Since "+startdt+", "+company+" has changed by +"+str(data[0])+"GBX, +" + str(data[1]) + "%"
						else:
								return "Since "+startdt+", "+company+" has changed by " + str(data[0]) + "GBX, " + str(data[1]) + "%"
				else: #Specified start and end date
						#print(DR.diff(company, start=startdt, end=enddt))
						data = DR.diff(company, start=startdt, end=enddt)
						#return "Between "+startdt+" and "+enddt+", "+company+" has had a "+str(DR.diff(company, start=startdt, end=enddt)[0])+"GBX price change, and a "+str(DR.diff(company, start=startdt, end=enddt)[1])+"% change"
						if data[0] > 0: #Positive change
								return "Since "+startdt+", "+company+" has changed by +" + str(data[0]) + "GBX, +" + str(data[1]) + "%"
						else: #Negative change
								return "Since "+startdt+", "+company+" has changed by " + str(data[0]) + "GBX, " + str(data[1]) + "%"
								
		#Retrieve general company information
		elif intent=="General Query Companies":
				returnstring=""
				
				#Current price
				returnstring+="The current spot price of "+company+" is "+str(DR.stock_price(company))+"GBX <br /><br />"
				
				#Percent change since yesterday
				startdt=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
				diffData = DR.diff(company, start=startdt)
				if diffData[0] > 0: #Positive change
						returnstring += "Since "+startdt+", "+company+" has changed by +" + str(diffData[0]) + "GBX, +" + str(diffData[1]) + "%  <br /><br />"
				else: #Negative change
						returnstring += "Since "+startdt+", "+company+" has changed by " + str(diffData[0]) + "GBX, " + str(diffData[1]) + "%  <br /><br />"
				
				#News
				returnstring+="Here's some news on "+company+"<br />"
				for article in DR.get_news(company):
						print("URL:"+article['u'])
						print("Snippit:"+article['sp'])
						score=NS.getScore(article['u'])
						print("Score: "+str(score))
						
						returnstring+=" <a href = '"+article['u']+"' target='_blank'>"+article['t']+"</a>:<br />"+article['sp']+" - "+article['s']+"<br />This article seems to be "+str(round(score*100, 1))+"% "
						if score < 0:
								returnstring+="negative"
						else:
								returnstring+="positive"
						returnstring+="<br />"
				
				return returnstring
				
		#General sector quert
		elif intent=="General Query Sectors":
				returnstring="Constituent prices: <br />"
				#price of each member
				for item in code_cat.items():
						if item[1]==sector:
								company=item[0]
								returnstring+=company+" - "+str(DR.stock_price(company))+"GBX <br />"
				#News stories
				returnstring+="<br />Here's some news on "+sector+"<br />"
				for article in DR.get_news_cat(sector):
						print("URL:"+article['u'])
						print("Snippit:"+article['sp'])
						symbol=NS.getSymbol(article['u'])
						print(symbol)
						returnstring+=symbol
						returnstring+=" <a href = '"
						returnstring+=article['u']
						returnstring+="' target='_blank'>"
						returnstring+=article['company']+"</a> - "+article['s']+" | "
						returnstring+=article['d']
						returnstring+="<br />"			   

				return returnstring
				
		#Unable to parse query
		return ("Sorry, I didn't understand that query.")

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

#Obtain categories from AI
def suggestCategories():
		return a.suggestCategories(3)

#Obtain anobalies from AI
def detectAnomalies():
		anomalies = a.detectAnomalies()
		return anomalies

#Write to AI file
def writeToFile():
		a.writeToFile()
		return
