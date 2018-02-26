import web
import json

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
        if data['type'] == "newMessage":
            #Handling for a message
            return data['message']
        elif data['type'] == 'suggestMessages':
            #Handle suggested messages
            return data['message']



if __name__ == "__main__":
    app.run()
