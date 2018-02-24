# from aylienapiclient import textapi
# import json

# client = textapi.Client("af398876", "a965f860dbd17f6c5958ed7ca395c737")

# class NewsSentiment:

#     def getPolarity(self, url):
        
#         extract = client.Summarize({'url': url, 'sentences_number': 5})

#         text = extract['sentences']
        
#         sentiment = client.Sentiment({'mode': 'document', 'text': text})

#         if (sentiment['polarity'] == 'positive'):
#             return 1
#         elif (sentiment['polarity'] == 'negative'):
#             return -1
#         else:
#             return 0

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='ad32de0b-12b9-4596-aadb-bcf62691a5d6',
  password='0Lrz7bWmjFYp',
  version='2017-02-27')

class NewsSentiment:

    def getPolarity(self, articleurl):

        try:
            response = natural_language_understanding.analyze(
                url=articleurl,
                features=Features(
                sentiment=SentimentOptions()),
                language='en')

            #print(json.dumps(response, indent=2))
            return "This article seems to be "+response['sentiment']['document']['label']
        except Exception:
            return "I encountered an error and can't tell whether this article is positive or negative"
