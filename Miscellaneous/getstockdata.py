import urllib.request

url="http://www.google.com/finance/getprices?i=(time)&p=(days)&f=d,o,h,l,c,v&df=cpct&q=(ticker)"

time="60"
days="1d"
ticker="AAPL"

url = url.replace("(time)",time)
url = url.replace("(days)",days)
url = url.replace("(ticker)",ticker)

print (url)

"""with urllib.request.urlopen(url) as link:
	print link.read()
"""

link = urllib.request.urlopen(url)
s=str(link.read())
app = s.replace('\\n','\r\n')
print(app)

target =  open("stockhist.txt","w")
target.write(s)

target.close()