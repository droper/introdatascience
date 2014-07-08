import sys
import json

def charge_afinn_dict(file_name):
    """Returns a dict with the afinn terms"""

    afinnfile = open(file_name)

    scores = {}  # empty dict

    for line in afinnfile:
        term, score = line.split("\t") # The file is tab-limited. "\t" means
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

    for line in tweetfile:
        tweet = json.loads(line)
        try:
            print rate_sentiment(tweet['text'], afinn_dict)
        except:
            pass

    tweetfile.close()

if __name__ == '__main__':
    main()
