__author__ = 'saurabh'
from flask import render_template, Flask, request
import urllib.request

app = Flask(__name__)

@app.route("/")
def home():
    stockData = getStockData(request['stockName'])
    return render_template("index.html")

def getStockData(stock):
    stockDateTimeList = []
    url="http://www.google.com/finance/getprices?i=(time)&p=(days)&f=d,o,h,l,c,v&df=cpct&q=(ticker)"
    time, days = "900", "5d"
    url = url.replace("(time)",time)
    url = url.replace("(days)",days)
    url = url.replace("(ticker)",stock)

    link = urllib.request.urlopen(url)
    stockData= str(link.read())
    stockDataList = stockData.split('\\n')
    for stockItem in stockDataList:
        stcklst = stockItem.split(",")
        if (stcklst[0]).isdigit == True:
            stockDateTimeList.append(stcklst[:2])
    print(stockDateTimeList)
    return stockDataList
    # print(stocks)

getStockData('AAPL')