from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)


paymentInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/payment")
adminInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/admin")


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/list_accounts', methods = ['GET'])
def list_all_students():
    loginFinder = paymentInstance.db.payment
    result = []
    for m in loginFinder.find():
        member = {}
        member['roll'] = m['roll']
        member['balance']  = m['balance']
        print(member)
        result.append(member)
    return jsonify({'accounts':result})


@app.route('/list_canteens', methods = ['GET'])
def list_all_canteens():
    canteenFinder = adminInstance.db.admin
    result = []
    for m in canteenFinder.find():
        result.append(m['canteen'])
    return jsonify({'canteens':result})



@app.route('/add_account',methods = ['POST'])
def add_account():
    response = {}
    accountAdder = paymentInstance.db.payment
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
    data = dict(request.form)
    canteen = data['canteen']
    password = data['password']
    canteens = adminAdder.find({'canteen':canteen}) 
    print(data)
    len = 0
    for _ in canteens:
        len += 1
    if len == 0:
        adminAdder.insert({'canteen':canteen, 'password':password})
        success = True
    else:
        print('Already Exists')
        success = False

    # print('Exception')
    # success = False
    if success:
        return render_template('main.html', val = canteen)
    else:
        return jsonify({"Error":"Database Entry Failed"})


@app.route("/login_admin", methods = ['POST'])
def login_admin():
    adminChecker = adminInstance.db.admin
    data = request.form
    print(data)
    canteen = data['canteen']
    password = data['password']
    success = False
    canteens = adminChecker.find({'canteen':data['canteen']})
    len = 0
    for _ in canteens:
        len += 1
    if len == 0:
        success=False
    else:
        canteendata = adminChecker.find({'canteen':canteen})[0] 
        if canteendata['password'] == password:
            success = True
        else:
            success = False
    if success:
        return render_template('main.html',val = canteen)
    else:
        return jsonify({"Error":"Login failed.. Check Username Password"})


@app.route("/pay",methods = ['POST'])
def pay():
    pass





if __name__ == '__main__':
    app.run(debug=True)
