var express = require('express');
var request = require("request");
var forecast = require('nostradamus');

var router = express.Router();
var app = express();
var stockQuotes = []; var nostroData = []; var predictions = [];
var alpha = 0.5; var beta = 0.4; var gamma = 0.6; var period = 5; var m = 2; 

var url = "http://www.google.com/finance/getprices?i=900&p=5d&f=d,o,h,l,c,v&df=cpct&q=(ticker)";
url = url.replace('(ticker)', 'AAPL');
request({
    url: url,
	json: true
}, function (error, response, body) {
    if (!error && response.statusCode === 200) {
		var quotes = body.split("\n");
		var quoteItems = [];
		quotes.forEach(function(quote){
			quoteItems = quote.split(",");
			if (isNaN(quoteItems[0]) == false && isNaN(quoteItems[0]) == false) {
				stockQuotes.push({'date': quoteItems[0], 'quote': quoteItems[1]});
				// console.log({'date': quoteItems[0], 'quote': quoteItems[1]});
				nostroData.push(parseFloat(quoteItems[1]));
			}
		});
	console.log(nostroData.length);
	console.log(forecast(nostroData, alpha, beta, gamma, period, m));
    }
})

// app.listen(3000);
// console.log("Running at Port 3000");