import web
import pysqlw
import json
import sqlalchemy as sql
import getopt
import sys
import requests
from urllib2 import urlopen

################################################
#
#                  config
#
################################################

urls = (
    "node/init", "node_init",
)

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
#                  init
#
################################################

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:i:")
    except getopt.GetoptError as e:
        print e
        print """
        -p defines the port you want the node to run at
        -i defines the ip and port "12.34.56.78:90" of the init stable node
        """
        sys.exit(2)

    for o, a in opts:
        if o == "p":
            port = a
        elif o == "i":
            initnode = a

    try:
        my_ip = requests.get('http://jsonip.com').json()['ip']
    except Exception as e:
        print "Error:", e
        print "Error getting public IP. "
        sys.exit()

    try:
        i = requests.post(initnode, data={"ip": my_ip, "port": port}).json()
        print i
    except Exception as e:
        print "Error:", e
        print "Could not POST to init node. "
        sys.exit()


    # engine = sql.create_engine("sqlite://", echo=True)
    # metadata = sql.MetaData()
    # users = sql.Table("users", metadata,
    #     sql.Column("id", sql.Integer, primary_key=True),
    #     sql.Column("username", sql.String),
    #     sql.Column("pubkey", sql.String)
    # )
    # nodes = sql.Table("nodes", metadata,
    #     sql.Column("id", sql.Integer, primary_key=True),
    #     sql.Column("ip", sql.String),
    #     sql.Column("reliability", sql.Integer)
    # )
    #
    # metadata.create_all(engine)


    app = web.application(urls, globals())
    app.notfound = notfound
    app.add_processor(new_request)
    app.run()
