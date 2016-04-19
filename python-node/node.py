import web
import pysqlw
import config

urls = (
    "/user/checkusername", "user_checkusername"
)

mysql_db = pysqlw.pysqlw(**{
    "db_type": config.mysql.db_type,
    "db_host": config.mysql.db_host,
    "db_user": config.mysql.db_user,
    "db_pass": config.mysql.db_pass,
    "db_name": config.mysql.db_name
})

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

class user_checkusername:
    def POST(self):
        new_request(self)
        data = web.input()

        if data["username"]:
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


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
    mysql_db.close()
