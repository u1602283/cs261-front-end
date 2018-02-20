from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from pinance import Pinance
from datetime import datetime
from marketcapfinder import get_market_cap
import pandas
import time

#NOTES
#non trading days (saturdays and sundays) have no data and hence throw an error - perhaps catch errors when returned df is empty as "Data is not availible for selected timeframe"
#start date must be before end date
#should stock_price function add functionality to tighter time frames (ie, per-minute requests)
#should diff function add functionality for start/end times?
#the time_frame function can cause measurements to be very wasteful in the data we are retriving
#should price_data have time parameter?
#round price values using decimal?


class DatRet:
    param = {
        'q': "", # Stock symbol (ex: "AAPL")
        'i': "", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "" # Period (Ex: "1Y" = 1 year)
    }

    #stock_price(object, string, string, string)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #The date should be in %Y-%m-%d format
    #The time should be in a %H:%M:%S format, though accuracy up the hour is only needed
    #If no date or time is given, then the current spot price is received accurate up to the minute. 
    def stock_price(self, symbol, date=None, time=None):
        currprice=0
        self.param['q']=symbol
        if date is None:
            #If we don't have a selected date, then select minute by minute data for the last day, and get the close price of the most recent result.
            self.param['i']='60'
            self.param['x']='LON'
            if symbol=="UKX":
                self.param['x']='INDEXFTSE'
            self.param['p']='1d'
            data=get_price_data(self.param)
            currprice=data.iloc[-1]['Close']
        else:
            #If we do have a selected date, the find the time frame most suitable for this date
            timeamt=self.time_frame(date)
            #We only need per-day data
            self.param['i']='86400'
            #But if we have a time, then we need per-hour
            if time is not None:
                self.param['i']='3600'
            #Our exchange
            self.param['x']='LON'
            if symbol=="UKX":
                self.param['x']='INDEXFTSE'
            
            #The period of time we want to look over is equal to our calculated time frame
            self.param['p']=timeamt

            #Request data using set parameters
            data=get_price_data(self.param)
            if time is not None:
                #Pandas requires us to use .loc when request hour-sensitive time series data
                #This only returns one row which can be indexed for it's close value
                daydata=data.loc[date+" "+time]['Close']
                currprice=daydata
            else:
                #If we only require per-day data then we can simply index by our given date
                daydata=data[date]
                #And index our dataframe using .iloc, selecting the close value of the first row
                currprice=daydata.iloc[0]['Close']
            
        return currprice
        #date=False => current stock price
        #date!=False => closing price on date

    #diff(object, string, string, string)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #The start should be the period of time from which the difference is required
    #The end should be the end date of the period from which the difference is required, namely after the start date
    #This function retrieves the difference in price, and percentage difference on a stock between two dates. If no end date is given, then the current date is assumed.
    def diff(self, symbol, start, end=None):
        if end is None:
            #Find the current price of the stock
            currprice=self.stock_price(symbol)
            #Find the price of the stock on our given start date
            histprice=self.stock_price(symbol, start)
            #Calculate the price difference
            pricediff=currprice-histprice
            #Calculate the percent change
            percentdiff=pricediff/histprice
        else:
            #Find the price of the stock on our start date
            startprice=self.stock_price(symbol, start)
            #Find the price of the stock on the end date
            endprice=self.stock_price(symbol, end)
            #Calculate the price difference of these two values
            pricediff=endprice-startprice
            #Calculate percentage change
            percentdiff=pricediff/startprice
        return (pricediff, percentdiff)
        #end=False => difference in (price, percentage) between start and current
        #end!=False => difference in (price, percentage) between start and end dates

    #price_data(object, sting, string)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #The date should be in %Y-%m-%d format (SHOULD NOT BE THE CURRENT DAY!)
    #This function returns a (opening, closing, high, low, vol) for a given day
    def price_data(self, symbol, date):
        #Find our required time frame for data for this date to be requested
        timeamt=self.time_frame(date)
        #Update params of our request
        self.param['q']=symbol
        self.param['i']='86400'
        self.param['x']='LON'
        if symbol=="INDEXFTSE":
            self.param['x']='UKX'
        
        self.param['p']=timeamt

        #Make request to API
        data=get_price_data(self.param)
        #Extract data just for this day
        data=data[date]
        #Construct tuple with required data from indices
        pricetuple=(data.iloc[0]['Open'],data.iloc[0]['Close'],data.iloc[0]['High'],data.iloc[0]['Low'], data.iloc[0]['Volume'])
        return pricetuple
        #Tuple with (opening, closing, high, low, vol) for given day

    #price_data_today(object, sting)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #This function will return the price data for the current day. This function is useful if the current trading hours are still in progress,
    #since the price_data function requires a day to be complete to retrieve the current data.
    def price_data_today(self, symbol):
        self.param['q']=symbol
        self.param['i']='60'
        self.param['x']='LON'
        if symbol=="INDEXFTSE":
            self.param['x']='UKX'
        self.param['p']='1d'

        data=get_price_data(self.param)
        #Extract data just for this day
        #We want the data for the current day only
        data=data[(datetime.now()).strftime("%Y-%m-%d")]

        #The day open is the open of the first data piece we're given
        dayopen=data.iloc[0]['Open']
        #The day close is simply the current stock price
        dayclose=self.stock_price(symbol)
        dayhigh=0
        daylow=0
        dayvol=0

        #We iterate through the rows of the day
        for index,row in data.iterrows():
            #The volume is cumulative
            dayvol+=int(row['Volume'])
            #For high and low we must make comparisons against our current guess and update accordingly
            if row['Low']<daylow or daylow==0:
                daylow=row['Low']
            if row['High']>dayhigh:
                dayhigh=row['High']

        return (dayopen, dayclose, dayhigh, daylow, dayvol)
    
    def current_marketcap(self, symbol):
        mktcap = get_market_cap(symbol, 'LON')
        return mktcap
        #Current market capitalisation for stock

    #get_news(object, string)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #This function returns a list of all recent news stories on a given stock
    def get_news(self, symbol):
        #Set our pinance variable
        stock=Pinance("LON:"+symbol)
        #If we're looking for general news on the FTSE we need a different exchange
        if symbol=="UKX":
            stock=Pinance("INDEXFTSE:"+symbol)
        #Request the news
        stock.get_news()
        #Set the news array to the requested data
        newsarray=stock.news_data
        return newsarray
        #array of dictionary entries, each with a news story, and metadata

    def get_news_cat(self, category):
        return
        
    def time_frame(self, d1):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        now=datetime.now()
        #d2 = str(now.strftime("%Y-%m-%d"))
        daynum=abs((now - d1).days)
        if daynum==0:
            return "1d"
        if daynum>265:
            return str(int(float(daynum/265)+1))+"Y"
        elif daynum>30:
            return str(int(float(daynum/30)+1))+"M"
        else:
            return str(daynum)+"d"

#dr=DatRet()
#print(dr.price_data_today("III"))
##now = time.time()
##print('dr.stock_price(symbol="III")')
##print(dr.stock_price(symbol="III"))
##print('dr.stock_price(symbol="III",date="2018-02-02")')
##print(dr.stock_price(symbol="III",date="2018-02-02"))
##print('dr.stock_price(symbol="BP",date="2018-02-06", time="12:00")')
##print(dr.stock_price(symbol="BP",date="2018-02-06", time="12:00"))
##print('dr.diff(symbol="III", start="2018-02-02")')
##print(dr.diff(symbol="III", start="2018-02-02"))
##print('dr.diff(symbol="III", start="2018-02-02", end="2018-02-09")')
##print(dr.diff(symbol="III", start="2018-02-02", end="2018-02-09"))
##print('dr.price_data(symbol="HSBA", date="2015-04-10")')
##print(dr.price_data(symbol="HSBA", date="2015-04-10"))
##print('dr.get_news("INDEXFTSE")')
##print(dr.get_news("INDEXFTSE"))
##print('dr.current_marketcap("BP")')
##print(dr.current_marketcap("BP"))
##print(time.time()-now)
