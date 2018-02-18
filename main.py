import apiai
import json
import requests

CLIENT_ACCESS_TOKEN='ee339c04a181469aba3549870dfeca5e'

def main(query):
    ai=apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request=ai.text_request()
    request.lang='en'
    request.session_id="1"
    request.query=query
    res=request.getresponse()

    jsonres=json.loads(res.read())
    for param in jsonres['result']['parameters']:
        company=jsonres['result']['parameters'][param]
        print(param+":"+company)
    intent=jsonres['result']['metadata']['intentName']
    message=jsonres['result']['fulfillment']['speech']
    #print(json.dumps(jsonres, indent=4, sort_keys=True))  pretty prints the response, may come in handy
    
    print("intent:"+intent)
    print(message)
    
while True:
    main(input("What's your query?\n"))
