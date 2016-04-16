from flask import Flask
import rpy2.robjects as robjects

application = app = Flask(__name__)

@app.route("/")
def hello():

    return robjects.r('''

    # This functions installs the package if not present and loads it.
    usePackage <- function(p) {
            if (!is.element(p, installed.packages()[,1]))
                    install.packages(p, dep = TRUE)
            require(p, character.only = TRUE)
    }

    #library(shiny)                  # To build the shiny app
    usePackage("tm")                     # package for text analytics
    usePackage("ggplot2")                # makes visually aesthetic plots
    usePackage("twitteR")                # library to get tweets using the twitter API
    usePackage("stringr")                # package for string manipulation
    usePackage("RCurl")                  # Makes HTTP connection in the R interface
    usePackage("reshape")                # for using the plyr function
    usePackage("RJSONIO")                # for converting JavaScript to R objects
    usePackage("wordcloud")              # creates fancy word clou
    usePackage("gridExtra")              # Addon for ggplot
    usePackage("plyr")                   # for the plyr function
    #1library(shinyIncubator)


    # Company code
    company <- "AAPL"


    # First we need to make a developer account in twitter and create a app. Once the app is created, the keys are made available. We will use the key and secret to extract tweets from twitter. More information about the twitter APi can be found in https://dev.twitter.com/overview/api

    api_key <- "YvkutpGKLE5GF7tTgj6C6Rl2N"
    api_secret <- "S4X411AEQTkageVCDkkJ1gubLofTwOn8wf2ls9O78EpxKCorTZ"
    access_token <- "69119995-zW2hPiy02doO1MEF7FcOu16k8GTqyp49BhNACiYG1"
    access_token_secret <- "U8qdm7Z83W3mzIYPQ12RW2x9wKVuALYxEjzgb3xTpfRKD"

    #origop <- options("httr_oauth_cache")
    #options(httr_oauth_cache=TRUE)
    setup_twitter_oauth(api_key, api_secret, access_token, access_token_secret)
    #options(httr_oauth_cache=origop)


    # Once the connection is created, start extracting tweets.



    # The raw tweets from twitter are cleaned and all redundant inforamtion are removed.
    CleanTweets<-function(tweets){
            tweets <- str_replace_all(tweets," "," ")
            tweets <- str_replace_all(tweets, "http://t.co/[a-z,A-Z,0-9]{10}","")
            tweets <- str_replace_all(tweets, "https://t.co/[a-z,A-Z,0-9]{10}","")
            tweets <- str_replace(tweets,"RT @[a-z,A-Z]*: ","")
            tweets <- str_replace_all(tweets,"#[a-z,A-Z]*","")
            tweets <- str_replace_all(tweets,"@[a-z,A-Z]*","")
            return(tweets)
    }

    # This function extracts tweets from twitter
    TweetFrame<-function(searchTerm, maxTweets){
            twtList<-searchTwitter(searchTerm,n=maxTweets, since = as.character(Sys.Date()), lang="en")
            twtList1<- do.call("rbind",lapply(twtList,as.data.frame))
            twtList1$text<-iconv(twtList1$text, 'UTF-8', 'ASCII')
            return(twtList1)
    }


    # calls the score.sentiment function to calculate the sentiment
    sentimentalanalysis <- function(entity1text,entity1entry){
            positivewords <- readLines("./positive_words.txt")
            negativewords <- readLines("./negative_words.txt")
            entity1score <- score.sentiment(CleanTweets(entity1text),positivewords,negativewords)
            return(mean(entity1score$score != 0))
    }



    # Calculates the sentiment score for each tweet using the breen's alorithm.
    score.sentiment = function(sentences, pos.words, neg.words){

            scores = laply(sentences, function(sentence, pos.words, neg.words) {
                    sentence = gsub('[[:punct:]]', '', sentence)
                    sentence = gsub('[[:cntrl:]]', '', sentence)
                    sentence = gsub('\\d+', '', sentence)
                    sentence = tolower(sentence)


                    word.list = str_split(sentence, '\\s+')
                    words = unlist(word.list)
                    pos.matches = match(words, pos.words)
                    neg.matches = match(words, neg.words)
                    pos.matches = !is.na(pos.matches)
                    neg.matches = !is.na(neg.matches)
                    score = sum(pos.matches) - sum(neg.matches)

                    return(score)
            }, pos.words, neg.words)

            scores.df = data.frame(score=scores, text=sentences, size=seq(length(scores)))
            return(scores.df)
    }

    # Get tweets
    entity1 <- TweetFrame(company, 100)

    # Do sentiment analysis
    entityscores <- sentimentalanalysis(entity1$text, company)
            ''')

    #return "Hello World!"

if __name__ == "__main__":
    application.run()
