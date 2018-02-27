from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from pinance import Pinance
from datetime import datetime, timedelta
from marketcapfinder import get_market_cap
import pandas
import time

###NOTES###
#SECTOR NEWS
#CHANGE SINCE OPENING
#ANY DATES REQUESTED ON A STOCK MUST BE AFTER THEY OPENED

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
            if time is None:
                #If time is None too then we just want the current stock price
                currprice=data.iloc[-1]['Close']
            else:
                #If we have a time, then we want the stock price at that time today
                date=datetime.now().strftime("%Y-%m-%d")
                #Just make a call to this function with today as the date
                currprice=self.stock_price(symbol, date, time)
                
        else:
            #If we have a date on the weekend, just change it to the preceding friday
            if datetime.strptime(date, "%Y-%m-%d").strftime("%A")=="Saturday":
                date=(datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d")
            elif datetime.strptime(date, "%Y-%m-%d").strftime("%A")=="Sunday":
                date=(datetime.strptime(date, "%Y-%m-%d")-timedelta(days=2)).strftime("%Y-%m-%d")
            #If we do have a selected date, the find the time frame most suitable for this date
            timeamt=self.time_frame(date)
            #We only need per-day data
            self.param['i']='86400'
            #But if we have a time, then we need per-hour
            if time is not None:
                self.param['i']='60'
            #Our exchange
            self.param['x']='LON'
            if symbol=="UKX":
                self.param['x']='INDEXFTSE'
            
            #The period of time we want to look over is equal to our calculated time frame
            self.param['p']=timeamt

            #Request data using set parameters
            data=get_price_data(self.param)
            if time is not None:
                if datetime.now().strftime("%Y-%m-%d %H:%M:%S")==date+" "+time:
                    return self.stock_price(symbol)
                #If we're BEFORE trading hours
                if datetime.strptime(time, "%H:%M:%S")<datetime.strptime("08:00:00", "%H:%M:%S"):
                    print("Before trading hours")
                    return self.price_data(symbol, (datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d"))[1] #Return closing price of the day before
                #If it's AFTER trading hours
                elif datetime.strptime(time, "%H:%M:%S")>datetime.strptime("16:30:00", "%H:%M:%S"):
                    print("After trading hours")
                    return self.price_data(symbol, (datetime.strptime(date, "%Y-%m-%d")).strftime("%Y-%m-%d"))[1] #Closing price of the current day
                #Pandas requires us to use .loc when request hour-sensitive time series data
                #This only returns one row which can be indexed for it's close value
                daydata=data.loc[date+" "+time]['Close']
                currprice=daydata
            else:
                if datetime.now().strftime("%Y-%m-%d")==date:
                    return self.stock_price(symbol)
                try:
                    #If we only require per-day data then we can simply index by our given date
                    daydata=data[date]
                    #And index our dataframe using .iloc, selecting the close value of the first row
                    currprice=daydata.iloc[0]['Close']
                except KeyError:
                    currprice=self.stock_price(symbol, (datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d"))
                except IndexError:
                    currprice=self.stock_price(symbol, (datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d"))
            
        return currprice
        #date=False => current stock price
        #date!=False => closing price on date

    #diff(object, string, string, string)
    #The symbol should be a valid stock symbol with the FTSE100 index
    #The start should be the period of time from which the difference is required
    #The end should be the end date of the period from which the difference is required, namely after the start date
    #This function retrieves the difference in price, and percentage difference on a stock between two dates. If no end date is given, then the current date is assumed.
    def diff(self, symbol, start, starttime=None, end=None, endtime=None):
        if end is None:
            #Find the current price of the stock
            currprice=self.stock_price(symbol)
            #Find the price of the stock on our given start date
            if starttime is None:
                histprice=self.stock_price(symbol, start)
            else:
                histprice=self.stock_price(symbol, start, starttime)
            #Calculate the price difference
            pricediff=currprice-histprice
            #Calculate the percent change
            percentdiff=pricediff/histprice
        else:
            #Find the price of the stock on our start date
            if starttime is None:
                startprice=self.stock_price(symbol, start)
            else:
                startprice=self.stock_price(symbol, start, starttime)
            #Find the price of the stock on the end date

            if endtime is None:
                endprice=self.stock_price(symbol, end)
            else:
                endprice=self.stock_price(symbol, end, endtime)
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
        #If the date given to us is a weekend
        weekend=False;
        if datetime.strptime(date, "%Y-%m-%d").strftime("%A")=="Saturday":
            date=(datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d")
            weekend=True;
        elif datetime.strptime(date, "%Y-%m-%d").strftime("%A")=="Sunday":
            date=(datetime.strptime(date, "%Y-%m-%d")-timedelta(days=2)).strftime("%Y-%m-%d")
            weekend=True;

        
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
        try:
            data=data[date]
            #Construct tuple with required data from indices
            pricetuple=(data.iloc[0]['Open'],data.iloc[0]['Close'],data.iloc[0]['High'],data.iloc[0]['Low'], data.iloc[0]['Volume'])
            if weekend:
                #If its the weekend, then open, close high and low is going to be the close price from friday, and the volume traded is going to be 0
                pricetuple=(data.iloc[0]['Close'],data.iloc[0]['Close'],data.iloc[0]['Close'],data.iloc[0]['Close'], 0)
            return pricetuple
        except KeyError:
            return self.price_data(symbol, (datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d"))
        except IndexError:
            return self.price_data(symbol, (datetime.strptime(date, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d"))
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
        if daynum<2:
            return "2d"
        if daynum>365:
            return str(int(float(daynum/265)+1))+"Y"
        elif daynum>30:
            return str(int(float(daynum/30)+1))+"M"
        else:
            return str(daynum)+"d"

    def roundTime(self, dt=None, roundTo=60):
       if dt == None : dt = datetime.datetime.now()
       seconds = (dt.replace(tzinfo=None) - dt.min).seconds
       rounding = (seconds+roundTo/2) // roundTo * roundTo
       return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

##dr=DatRet()
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
