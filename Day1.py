from flask import Flask, jsonify
import psutil as ps
my_app = Flask(__name__)

@my_app.route('/api/usage', methods = ['GET'])
def getUtilize():
    data = {
        'cpu': getcpu(),
        'mem': getmem(),
        'disk': getdisk(),
    }
    return jsonify(data),200

def getcpu():
    cpu = ps.cpu_percent(interval=1)
    return cpu

def getmem():
    mem = ps.virtual_memory().used
    # print "MEM %s" %(mem*1.0)/(1024**3)
    return mem

def getdisk():
    disk = ps.disk_usage('/')
    return disk

my_app.run(host="127.0.0.1")