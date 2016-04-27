import web
import pysqlw
import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
        data = web.input()

        if data["wefwef"]:
            print "exists"
        else:
            print "nah"

################################################
#
#                  user classes
#
################################################

################################################
#
#                  config
#
################################################

urls = (
    "node/init", "node_init",
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

engine = sqlalchemy.create_engine("sqlite:///db.db")

if not os.path.isfile("db.db"):
    base.metadata.create_all(engine)

base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

    #get public ip

    try:
        my_ip = requests.get('http://jsonip.com').json()['ip']
    except Exception as e:
        print "Error:", e
        print "Error getting public IP. "
        sys.exit()

    #if firstnode, populate self
    #else populate from init node

    if firstnode:
        session.add(Node(ip=my_ip, reliability=0))
        session.commit()

    else:
        try:
            i = requests.post(initnode, data={"ip": my_ip, "port": port}).json()
            print i
            #do inserting of all data here
        except Exception as e:
            print "Error:", e
            print "Could not POST to init node. "
            sys.exit()

    app = web.application(urls, globals())
    app.notfound = notfound
    app.add_processor(new_request)
    app.run()
