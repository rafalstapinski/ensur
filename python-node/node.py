import web
import pysqlw
import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import sys
import requests
from urllib2 import urlopen
import os.path

################################################
#
#                  support methods
#
################################################

def write(payload, status):
    return json.dumps({"payload": payload, "status": status})

def notfound():
    return web.notfound("404")

def new_request(request):
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")


################################################
#
#                  node classes
#
################################################

class node_init:
    def POST(self):

        new_request(self)
        data = web.input()

        try:
            ip = data["ip"].encode("utf-8")
        except:
            return write({"error": "Port or IP not UTF-8 encoded. "}, 400)

        nodes = session.query(Node).all()

        res = []

        for node in nodes:
            res.append({"ip": node.ip, "reliability": node.reliability})
            if node.ip != my_ip:
                i = requests.post(node.ip, data={"ip": ip}).json()

        session.add(Node(ip=ip, reliability=0))
        session.commit()

        return write({"message": "Nodes returned. ", "nodes": res}, 200)

class node_new:

    # leave nodes for now, work on singular node comunication
    # see if individual node update is possible while excluding
    # already updated information, same for user data

    def POST(self):

        new_request(self)
        data = web.input()

        try:
            ip = data["ip"].encode("utf-8")
        except:
            return write({"error": "Port or IP not UTF-8 encoded. "}, 400)

        res = session.query(Node).filter(Node.ip == ip)

        if not res: #not sure about the real check for existence atm
            session.add(Node(ip=ip, reliability=0))
            session.commit()

################################################
#
#                  user classes
#
################################################

class user_new:
    def GET(self):

        new_request(self)
        data = web.input()

        try:
            username = data["username"].encode("utf-8")
            print username
            pubkey = data["pubkey"].encode("utf-8")
            print pubkey
        except:
            return write({"error": "Username or pubkey not UTF-8 encoded. "}, 400)

        if len(username) > 200 or len(pubkey) > 4096:
            return write({"error": "Username or pubkey too long. "}, 400)

        user = session.query(User).filter(User.username == username).first()

        if user is not None:
            return write({"error": "Username already exists. "}, 452)

        session.add(User(username=username, pubkey=pubkey))
        session.commit()

        user = session.query(User).filter(User.username == username).first()

        return write({"message": "Added user. ", "username": user.username, "uid": user.id}, 200)

class user_exists:
    def GET(self):

        new_request(self)
        data = web.input()

        try:
            username = data["username"].encode("utf-8")
        except:
            return write({"error": "Invalid username. "}, 400)

        user = session.query(User).filter(User.username == username).first()

        if user is not None:
            return write({"error": "Username already exists. "}, 452)

        return write({"message": "Username is available. ", "username": username}, 200)

        #probably change up status codes so they make more sense with the method name

# class user_update:
#     def GET(self):
#
#         new_request(self)
#         data = web.input()
#
#         try:
#             username = data["username"].encode("utf-8")
#
#         except:
#             return write({"error": "Username not UTF-8 encoded. "}, 500)


class user_get:
    def GET(self):

        new_request(self)
        data = web.input()

        try:
            username = data["username"].encode("utf-8")
        except:
            return write({"error": "Improper username supplied. "}, 404)

        users = session.query(User).filter(User.username == username)

        if users.count() < 1:
            return write({"error": "No user found. "}, 404)

        for user in users:
            return write({"message": "User found. ", "user": {"username": user.username, "pubkey": user.pubkey}}, 200)

    #    print users

    #    print dir(users)
    #    for user in users:


################################################
#
#                  messages classes
#
################################################

class messages_new:
    def GET(self):

        new_request(self)
        data = web.input()

        # probably get rid of anon messaging since all messages will be signed

        try:
            origin = data["origin"].encode("utf-8")
        except:
            origin = 0

        try:
            # move most operations to server to speed up client work
            # maybe store id client side and avoid lookup altogether. we'll see
            username = data["target"].encode("utf-8")

            if len(username) > 200 or len(username) < 1:
                return write({"Invalid username. "}, 400) #specify later

            target = session.query(User).filter(User.username == username).first().id

        except:
            return write({"error": "Username not found. "}, 404)

        try:
            content = data["content"].encode("utf-8")
        except:
            return write({"error": "No valid content provided. "}, 400)

        if len(content) > 2048:
            return write({"error": "Content is too long. "}, 404)

        try:
            session.add(Message(target=target, origin=origin, content=content))
            session.commit()

            return write({"message": "Sent message successfully. "}, 200)

            #implement push to user client here

        except:
            return write({"error": "Server error, could not insert into database. "}, 500)

class messages_get:
    def GET(self):

        new_request(self)
        data = web.input()

        try:
            last = int(data["last"])
        except:
            last = 0

        try:
            uid = int(data["uid"])
        except:
            return write({"error": "Improper uid supplied. "}, 400)

        messages = session.query(Message).filter(Message.target == uid)
        resulting = {}

        for message in messages:
            if message.id > last:
                resulting[message.id] = {"origin": message.origin, "content": message.content}

        # return messages
        # update newlast client side
        return write({"message": "Received messages. ", "messages": resulting, "count": len(resulting)}, 200)

################################################
#
#                  config
#
################################################

urls = (
    "/node/init", "node_init",
    "/node/add", "node_add",

    "/user/new", "user_new",
    "/user/get", "user_get",
    "/user/exists", "user_exists",

    "/messages/new", "messages_new",
    "/messages/get", "messages_get"
)

base = declarative_base()

class Node(base):
    __tablename__ = "nodes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    ip = sqlalchemy.Column(sqlalchemy.String)
    reliability = sqlalchemy.Column(sqlalchemy.Integer)

class User(base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    pubkey = sqlalchemy.Column(sqlalchemy.String)

class Message(base):
    __tablename__ = "messages"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    target = sqlalchemy.Column(sqlalchemy.Integer)
    origin = sqlalchemy.Column(sqlalchemy.Integer)
    content = sqlalchemy.Column(sqlalchemy.Text)

engine = sqlalchemy.create_engine("sqlite:///db.db")

if not os.path.isfile("db.db"):
    base.metadata.create_all(engine)

base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()
session = scoped_session(sessionmaker(bind=engine))

################################################
#
#                  init
#
################################################

if __name__ == "__main__":

    firstnode = False
    initnode = None  #default stable node here, once implemented

    #bind arguments

    opts = sys.argv[1:]
    port = opts[0]

    for opt in opts:
        if opt == "-f":
            firstnode = True
        elif opt == "-i":
            initnode = opts[opts.index(opt) + 1]

    if firstnode and initnode is not None:
        print "Can't run as first node and connect to an init node. "
        sys.exit()

    #get public ip

    try:
        my_ip = requests.get('http://jsonip.com').json()['ip']
    except Exception as e:
        print "Error:", e
        print "Error getting public IP. "
        sys.exit()

    #if firstnode, populate self
    #else populate from init node

    my_ip = my_ip + port

    if firstnode:
        session.add(Node(ip=my_ip, reliability=0))
        session.commit()

    else:
        try:
            r = "http://%s/node/init" % initnode
            print r
            i = requests.post(r, data={"ip": my_ip}).json()

            if i["status"] == 200:
                for node in i["payload"]["nodes"]:
                    session.add(Node(ip=node["ip"], reliability=node["reliability"]))
                session.commit()
                print "Success initializing. "
            else:
                print "Error %s: %s" & (i["status"], i["payload"]["error"])

        except Exception as e:
            print "Error:", e
            print "Could not initialize. "
            sys.exit()

    app = web.application(urls, globals())
    app.notfound = notfound
    #app.add_processor(new_request)
    app.run()
