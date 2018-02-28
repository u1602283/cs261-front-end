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
            data = json.loads(web.data())
            print(data)
            #Check for the type of request sent
            if data['type'] == "newMessage":
                #Handling for a message
                #a.addQuery(self, data['message'])
                result = main(data['message'])
                return result
                #return data['message']
            elif data['type'] == 'suggestMessages':
                #Handle suggested messages
                #return a.suggestCategories(self, 2)
                categories = suggestCategories()
                print(categories)
                return data['message']
            elif data['type'] == 'detectAnomalies':
                #return a.detectAnomalies(self)
                return data['message']

    if __name__ == "__main__":
        app.run()

except KeyboardInterrupt :
    print("Shutting down")
    writeToFile()
