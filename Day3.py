#-*- coding: utf8 -*-
from flask import Flask
from flaskext.mysql import MySQL
from flask import request
from flask_basicauth import BasicAuth
import requests
import time
import json

app = Flask(__name__)

app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "12345678"
app.config["MYSQL_DATABASE_DB"] = "test_database"
app.config["MYSQL_DATABASE_HOST"] = "203.154.83.124"
app.config["MYSQL_DATABASE_PORT"] = 3306

app.config['BASIC_AUTH_USERNAME'] = 'sdi'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

secure_my_api = BasicAuth(app)

mysql = MySQL()
mysql.init_app(app)
def toJson(data, columns):
    results = []
    for row in data:
        results.append(dict(zip(columns, row)))
    return results
@app.route('/api', methods = ['POST'])
def db():
    reciver = request.json
    insert_username = reciver["username"]
    insert_password = reciver["password"]
    insert_time = time.time()
    con = mysql.connect()
    cursor = con.cursor()
    try:
        sql = """INSERT INTO users (username,password,create_time) values (%s,%s)"""
        value = (insert_username,insert_password,insert_time)
        cursor.execute(sql,value)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_pool = toJson(data, columns)
        print 'pool ======',result_pool
        con.commit()
        con.close()  #ปิดการเชื่อมต่อ
    except Exception as e:
        print e
        con.rollback()
        con.close()

    url = "https://notify-api.line.me/api/notify"

    payload = "message=create %s" %insert_username
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer 3eCKae9VjqktgtVJWjU8hxnwjDHFHuiAop5JFEas1gT",
        'User-Agent': "PostmanRuntime/7.13.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "89cbcb24-a666-4bcd-95b8-3074f963d787,e5f1999a-95e4-4a86-8219-d19daee4f5da",
        'Host': "notify-api.line.me",
        'accept-encoding': "gzip, deflate",
        'content-length': "21",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    return 'success!'

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5000, threaded=True)
