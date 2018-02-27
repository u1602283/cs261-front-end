import web
import json
from main import *
from AI import *

a = AI()

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
            return main(data['message'])
            #return data['message']
        elif data['type'] == 'suggestMessages':
            #Handle suggested messages
            #return a.suggestCategories(self, 2)
            return data['message']
        elif data['type'] == 'detectAnomalies':
            #return a.detectAnomalies(self)
            return data['message']


if __name__ == "__main__":
    app.run()
