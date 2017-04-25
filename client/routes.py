import web
import os

class index:

    def GET(self):

        new_request(self)

        f = open('%s/static/index.html' % __location__)
        html = f.read()
        f.close()

        return html

class messages:

    def GET(self):

        new_request(self)

        try:
            username = web.cookies().get('username').encode('utf-8')
        except:
            raise web.seeother('/')


##############################################
#
#       Config and support methods
#
##############################################

urls = (
    '/', 'index',
    '/messages', 'messages',
)

def notfound():
    return web.notfound('404')

def new_request(request):
    web.header('Access-Control-Allow-Origin', '*')

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':

    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
