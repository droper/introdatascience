# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import json

non_sentiment_words = {}

def charge_afinn_dict(file_name):
    """Returns a dict with the afinn terms"""

    afinnfile = open(file_name)

    scores = {}  # empty dict

    for line in afinnfile:
        term, score = line.decode('utf-8').split("\t") # The file is tab-limited. "\t" means
                                       # tabs character"
        scores[term] = int(score)      # Converts the score to an integer 

    afinnfile.close()

    return scores



def rate_sentiment(tweet, affin_dict):
    """Score the sentiment in a tweet"""

    words = tweet.split()

    score = 0

    # Iterate over the words of the tweet and 
    # add the sentiment score of each word if exists
    for word in words:
        if word in affin_dict.keys():
            score = score + affin_dict[word]

    return score


def main():
    afinn_dict = charge_afinn_dict(sys.argv[1])

    # Iterate over all the tweets
    tweetfile = open(sys.argv[2])

    # The counters
    positives = 1
    negatives = 1

    # Iterate over the tweets
    for line in tweetfile:
        tweet = json.loads(line)

        # if word is in the text then we rate it, if the rate is greater
        # that cero is a positive tweet, if less then is negative.
        try:
                rate = rate_sentiment(tweet['text'], afinn_dict)

                # If a word is a non sentiment one we add it to
                # non_sentiment_words and create a list with three items
                # first item: total number of tweets, second: positive tweets
                # third: negative tweets
                for word in tweet['text'].split():
                    if word not in afinn_dict.keys():
                        if word not in non_sentiment_words.keys():
                            if rate > 0:      # Si es un tweet positivo
                                non_sentiment_words[word] = [1,2,1]
                            elif rate < 0:      # Si es un tweet negativo
                                non_sentiment_words[word] = [1,1,2]
                        else:
                            if rate > 0:    # Si es un tweet positivo
                                non_sentiment_words[word][0] += 1
                                non_sentiment_words[word][1] += 1
                            elif rate < 0:      # Si es un tweet negativo
                                non_sentiment_words[word][0] += 1
                                non_sentiment_words[word][2] += 1

        except:
            pass

    # Use the formula of the paper and print it
    for word in non_sentiment_words.keys():
        a = non_sentiment_words[word][1]/float(non_sentiment_words[word][0])
        b = non_sentiment_words[word][2]/float(non_sentiment_words[word][0])
        print word, a/b

    tweetfile.close()


if __name__ == '__main__':
    main()
