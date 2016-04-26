import web
import pysqlw
import config
import json
import hashlib

################################################
#
#                  config
#
################################################

urls = (
    "/user/checkusername", "user_checkusername",
    "/user/createuser", "user_createuser"
)

mysql_db = pysqlw.pysqlw(**{
    "db_type": config.mysql.db_type,
    "db_host": config.mysql.db_host,
    "db_user": config.mysql.db_user,
    "db_pass": config.mysql.db_pass,
    "db_name": config.mysql.db_name
})

################################################
#
#                  support methods
#
################################################

def write(payload, status):
    payload["status"] = status
    return json.dumps({"payload": payload, "status": status})

def notfound():
    # web.header("Content-Type", "application/json; charset=UTF-8")
    return web.notfound("404 Not Found")
    #return web.notfound(render.notfound())

def new_request(request):
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")

################################################
#
#                  user classes
#
################################################

class user_createuser:
    def POST(self):
        new_request(self)
        data = web.input()

        if data["username"] and data["password"] and data["pubkey"]:
            username = data["username"]
            password = data["password"]
            pubkey = data["pubkey"]

            try:
                username = username.decode("utf-8")
            except UnicodeError:
                return write({"error": "Username not valid UTF-8 format. "}, 400)

            if len(username) > 20 or len(username) < 1:
                return write({"error": "Username must be between 1 and 20 chars. "}, 400)

            user = mysql_db.where("username", mysql_db.escape(username)).get("users")

            if user != ():
                return write({"error": "Username already exists. "}, 400)

            try:
                password = password.decode("utf-8")
            except UnicodeError:
                return write({"error": "Password not valid UTF-8 format. "}, 400)

            if len(password) < 1 or len(password) > 64:
                return write({"error": "Password must be between 1 and 64 chars. "}, 400)

            try:
                pubkey = pubkey.decode("utf-8")
            except UnicodeError:
                return write({"error": "Public key not valud UTF-8 format. "}, 400)

            password_hash = hashlib.sha224(password).hexdigest()

            inserted = mysql_db.insert("users", {"username": mysql_db.escape(username), "password": mysql_db.escape(password_hash), "pubkey": mysql_db.escape(pubkey)})

            print inserted

            if inserted:
                return write({"message": "Success. "}, 200)
            else:
                return write({"error": "Error inserting into database. "}, 500)

        else:
            return write({"error": "Either username, password, or pubkey not supplied. "}, 400)

class user_checkusername:
    def POST(self):
        new_request(self)
        data = web.input()

        if data["username"]:
            username = data["username"]
            try:
                username.decode("utf-8")
            except UnicodeError:
                return write({"error": "Username not valid UTF-8 format. "}, 400)

            if len(username) > 20 or len(username) < 1:
                return write({"error": "Username must be between 1 and 20 chars. "}, 400)

            user = mysql_db.where("username", mysql_db.escape(username)).get("users")

            if user == ():
                return write({"unique": True}, 200)
            else:
                return write({"unique": False}, 200)
        else:
            return write({"error": "Username can't be empty. "}, 400)

################################################
#
#                  init
#
################################################

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
    mysql_db.close()
