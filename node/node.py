import web
import json
import sys
import requests
from config import db

##############################################
#
#       Message Classes
#
##############################################

##############################################
#
#       User Classes
#
##############################################

class user_new:
    def POST(self):

        new_request(self)

        i = web.input()

        try:
            username = i['username'].encode('utf-8')
            pubkey = i['pubkey'].encode('utf-8')
        except KeyError:
            return write({'message': 'you must provide username and pubkey'}, 400)
        except UnicodeError:
            return write({'message': 'inputs must be utf-8 encoded'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        if exists_duplicate_username(username):
            return write({'message': 'username already exists'}, 403)

        if create_user(username, pubkey):
            return write({'message': 'user created'}, 200)

        return write({'message': 'error creating user'}, 500)



##############################################
#
#       Config and support methods
#
##############################################

urls = (
    '/user/new', 'user_new'
)

def write(payload, status):
    return json.dumps({'payload': payload, 'status': status})

def notfound():
    return web.notfound('404')

def new_request(request):
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')

def exists_duplicate_username(username):

    dbvars = dict(username=username)

    results = db.conn.select('users', dbvars, where='username = $username')

    for result in results:
        return True

    return False

def create_user(username, pubkey):

    seq_id = db.conn.insert('users', username=username, pubkey=pubkey)

    try:
        int(seq_id)
        return True
    except:
        return False


if __name__ == '__main__':

    # conn = web.database(dbn='postgres', db=config.dbname, user=config.dbuser, pw=config.dbpass)

    # initnode = None
    #
    # opts = sys.argv[1:]
    # # port = opts[0]
    #
    # for opt in opts:
    #     if opt == '-i':
    #         initnode = opts[opts.index(opt) + 1]
    #
    # try:
    #     ip = requests.get('http://jsonip.com/').json()['ip']
    # except Exception as e:
    #     print 'Error getting IP. '
    #     sys.exit()

    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
