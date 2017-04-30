import web
import os
import time
from config import Config
import pgpy

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

        try:
            username = web.cookies().get('username').encode('utf-8')
        except:
            raise web.seeother('/')

        cleartext = web.cookies().get('cleartext')
        signature = web.cookies().get('signature')

        if signature is None or cleartext is None:

            web.setcookie('cleartext', int(round(time.time() * 1000)))

            f = open('%s/static/verifier.html' % __location__)
            html = f.read()
            f.close()

            return html

        try:
            if int(round(time.time() * 1000)) - 20000 > int(cleartext):
                web.setcookie('cleartext', int(round(time.time() * 1000)))

                f = open('%s/static/verifier.html' % __location__)
                html = f.read()
                f.close()

                return html
        except:
            web.setcookie('cleartext', '', expires=-1)
            web.setcookie('signature', '', expires=-1)
            raise web.seeother('/messages')

        try:
            params = dict(username=username)
            user = db.select('users', params, where='username = $username').list()[0]
        except IndexError:
            web.setcookie('username', '', expires=-1)
            raise web.seeother('/')


        pubkey, _ = pgpy.PGPKey.from_blob(user.pubkey)
        if pubkey.verify(cleartext, pgpy.PGPSignature.from_blob(signature)).__bool__():

            web.setcookie('signature', '', expires=-1)
            web.setcookie('cleartext', '', expires=-1)

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

db = web.database(dbn='postgres', db=Config.dbname, user=Config.dbuser, pw=Config.dbpass)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == '__main__':

    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
