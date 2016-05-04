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
        new_request(self)
        data = web.input()

        if data["ip"]:
            try:
                ip = data["ip"].encode("utf-8")
            except UnicodeError:
                return write({"error": "Port or IP not UTF-8 encoded. "}, 500)

            nodes = session.query(Node).all()

            res = []

            for node in nodes:
                res.append({"ip": node.ip, "reliability": node.reliability})
                if node.ip != my_ip:
                    i = requests.post(node.ip, data={"ip": ip}).json()

            session.add(Node(ip=ip, reliability=0))
            session.commit()

            return write({"nodes": res}, 200)

        else:
            return write({"error": "Port or IP not supplied. "}, 500)

class node_new:
    def POST(self):
        new_request(self)

        if data["ip"]:
            try:
                ip = data["ip"].encode("utf-8")
            except UnicodeError:
                return write({"error": "Port or IP not UTF-8 encoded. "}, 500)

            res = session.query(Node).filter(Node.ip == ip)

            if not res: #not sure about the real check for existence atm
                session.add(Node(ip=ip, reliability=0))
                session.commit()


        else:
            return write({"error": "Port or IP not supplied. "}, 500)

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
    "/node/init", "node_init",
    "/node/add", "node_add"
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
