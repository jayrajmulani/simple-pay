from flask import Flask, request, jsonify,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)


paymentInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/payment")
adminInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/admin")


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/list_accounts', methods = ['GET'])
def list_all_accounts():
    loginFinder = loginInstance.db.login
    result = []
    for m in loginFinder.find():
        member = {}
        member['roll'] = m['roll']
        member['balance']  = m['balance']
        print(member)
        result.append(member)
    return jsonify({'accounts':result})


@app.route('/list_canteens', methods = ['GET'])
def list_all_accounts():
    canteenFinder = adminInstance.db.admin
    result = []
    for m in canteenFinder.find():
        canteen = {}
        canteen['canteen'] = m['canteen']
        result.append(canteen)
    return jsonify({'canteens':result})



@app.route('/add_account',methods = ['POST'])
def add_account():
    response = {}
    accountAdder = loginInstance.db.login
    data = request.get_json()
    try:
        accountAdder.insert({'roll':data['roll'], 'balance':data['balance']})
        response['code'] = 'OK'
    except:
        response['code'] = 'ERROR'

    return jsonify(response)



@app.route("/add_canteen", methods = ['POST'])
def add_canteen_acc():
    adminAdder = adminInstance.db.admin
    response = {}
    data = request.get_json()
    canteens = adminAdder.find({'canteen':data['canteen']}) 
    len = 0
    try:
        for _ in canteens:
            len += 1
        if len == 0:
            password = data['password']
            adminAdder.insert({'canteen':data['canteen'], 'password':password})
            response['code'] = 'OK'
        else:
            response['code'] = 'ALREADY EXISTS'
    except:
        response['code'] = 'ERROR'

    return jsonify(response)


@app.route("/login", methods = ['POST'])
def login():
    adminChecker = adminInstance.db.admin
    response = {}
    data = request.get_json()
    canteen = data['canteen']
    password = data['password']
    canteens = adminChecker.find({'canteen':data['canteen']})
    len = 0
    for _ in canteens:
        len += 1
    if len == 0:
        response['code'] = 'NOT EXISTS'
    else:
        canteendata = adminChecker.find({'canteen':canteen})[0] 
        print(password)
        print(canteendata['password'])
        if canteendata['password'] == password:
            response['code'] = 'OK'
        else:
            response['code'] = 'INCORRECT'
    return jsonify(response)


@app.route("/pay",methods = ['POST'])
def pay():






if __name__ == '__main__':
    app.run(debug=True)

