import web
import os
import time

class index:

    def GET(self):

        new_request(self)

        if web.cookies().get('username') is not None:

            raise web.seeother('messages')

        f = open('%s/static/index.html' % __location__)
        html = f.read()
        f.close()

        return html

class messages:

    def GET(self):

        new_request(self)

        username = web.cookies().get('username').encode('utf-8')

        if username is None:
            raise web.seeother('/')

        cleartext = web.cookies().get('cleartext')

        # if cleartext is None:
        #     web.setcookie('cleartext', int(round(time.time() * 1000)))
        #
        #     f = open('%s/static/verifier.html' % __location__)
        #     html = f.read()
        #     f.close()
        #
        #     return html

        f = open('%s/static/messages.html' % __location__)
        html = f.read()
        f.close()

        return html

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
