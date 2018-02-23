from aylienapiclient import textapi
import json

client = textapi.Client("af398876", "a965f860dbd17f6c5958ed7ca395c737")

class NewsSentiment:

    def getPolarity(self, url):

        sentiment = client.Sentiment({'mode': 'document', 'url': url})

        if (sentiment['polarity'] == 'positive'):
            return 1
        elif (sentiment['polarity'] == 'negative'):
            return -1
        else:
            return 0