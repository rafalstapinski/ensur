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

class user_get:
    def POST(self):

        new_request(self)

        i = web.input()

        try:
            username = i['username'].encode('utf-8')
        except KeyError:
            return write({'message': 'you must provide username and pubkey'}, 400)
        except UnicodeError:
            return write({'message': 'inputs must be utf-8 encoded'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        dbvars = dict(username=username)

        results = db.conn.select('users', dbvars, where='username = $username')

        for result in results:
            return write({'pubkey': result['pubkey']}, 200)

        return write({'message': 'User does not exist. '}, 404)

class message_new:
    def POST(self):

        new_request(self)

        i = web.input()

        try:
            receiver = i['receiver'].encode('utf-8')
            message = i['message'].encode('utf-8')
            sender = i['sender'].encode('utf-8')
        except KeyError:
            return write({'message': 'you must provide username and pubkey'}, 400)
        except UnicodeError:
            return write({'message': 'inputs must be utf-8 encoded'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        seq_id = db.conn.insert('messages', receiver=receiver, sender=sender, message=message)

        if seq_id is not None:
            return write({'message': 'message sent'}, 200)

        return write({'message': 'error sending message'}, 500)

class message_get:

    def POST(self):

        new_request(self)

        i = web.input()

        try:
            receiver = i['receiver'].encode('utf-8')
            sender = i['sender'].encode('utf-8')
        except KeyError:
            return write({'message': 'you must provide username and pubkey'}, 400)
        except UnicodeError:
            return write({'message': 'inputs must be utf-8 encoded'}, 400)
        except:
            return write({'message': 'something went wrong'}, 500)

        myvars = dict(receiver=receiver, sender=sender)

        results = db.conn.select('messages', myvars, where='receiver = $receiver or sender = $sender')

        for result in results:
            print result


##############################################
#
#       Config and support methods
#
##############################################

urls = (
    '/user/new', 'user_new',
    '/user/get', 'user_get',
    '/message/new', 'message_new',
    '/message/get', 'message_get',
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
