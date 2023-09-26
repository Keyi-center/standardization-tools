from flask import Flask,jsonify
from base_util.response_utils import response,ok
from base_util.filter_null_params import filter_null_values

app = Flask(__name__)

@app.route("/")
def test_index():
    data = None
    data = ""
    data = 123
    data = 12.3
    data = [12,None]
    data = {'abc':None,'def':12,'hij':'abc','jjj':None,'hello':{'a':None,'b':12,'c':'abc','d':None},'test':[],
            'te2':None,'te3':[1,2,3,None],'te4':[1,2,3,4,None,{'a':None,'b':12,'c':'abc','d':None}]}
    resp = {'msg':'','code':200,'data':data}
    return response(200, "msg",data)


@app.route("/2")
def test_index_3():
    data = None
    data = ""
    data = 123
    data = 12.3
    data = [12,None]
    data = {'abc':None,'def':12,'hij':'abc','jjj':None,'hello':{'a':None,'b':12,'c':'abc','d':None},'test':[],
            'te2':None,'te3':[1,2,3,None],'te4':[1,2,3,4,None,{'a':None,'b':12,'c':'abc','d':None}]}
    resp = {'msg':'','code':200,'data':data}
    return ok(data)


@app.route("/hello")
@filter_null_values
def test_index_2():
    data = None
    data = ""
    data = 123
    data = 12.3
    data = [12,None]
    data = {'abc':None,'def':12,'hij':'abc','jjj':None,'hello':{'a':None,'b':12,'c':'abc','d':None},'test':[],
            'te2':None,'te3':[1,2,3,None],'te4':[1,2,3,4,None,{'a':None,'b':12,'c':'abc','d':None}]}
    resp = {'msg':'','code':200,'data':data}
    return jsonify(resp)


app.run()