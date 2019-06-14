#-*- coding: utf8 -*-
from flask import Flask, jsonify,request
import os
import time
app = Flask(__name__)

@app.route('/box', methods = ['POST'])
def boxindex():
    reciver = request.get_json()
    answer_destination = reciver["destination"]
    dis_json = {}
    for dis in answer_destination:
        start_time = time.time()
        response = os.system("ping -c 2 " + dis)
        timems = time.time() - start_time
        if response == 0:
            dis_json[dis]= timems
        else:
            dis_json[dis] = timems
    return jsonify(dis_json),200

app.run(host="127.0.0.1")