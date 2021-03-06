import web
import json
import atexit
from main import *

try:
    urls = (
        '/', 'index'
    )
    app = web.application(urls, globals())
    render = web.template.render('templates/')

    class index:
        def GET(self):
            return render.index()

        def POST(self):
            data = json.loads(web.data().decode())
            print(data)
            #Check for the type of request sent
            if data['type'] == "newMessage":
                #Handling for a message
                #a.addQuery(self, data['message'])
                result = main(data['message'])
                writeToFile()
                return result
                #return data['message']
            elif data['type'] == 'suggestMessages':
                #Handle suggested messages
                #return a.suggestCategories(self, 2)
                categories = suggestCategories()
                print(categories)
                return json.dumps(categories)
            elif data['type'] == 'detectAnomalies':
                #return a.detectAnomalies(self)
                anomalies = detectAnomalies()
                print(anomalies)
                return json.dumps(anomalies)

    if __name__ == "__main__":
        app.run()

except KeyboardInterrupt :
    print("Shutting down")
    writeToFile()
