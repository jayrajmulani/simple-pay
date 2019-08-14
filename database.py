from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
paymentInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/payment")
adminInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/admin")
menuInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/menu")


def get_menu():
    menuInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/menu")
    menu = []
    for m in menuInstance.db.menu.find():
        menu.append(m)
    print(menu)
    return menu

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
        items = ['aaa','bbb','ccc']
        print(len(items))
        return render_template('main.html', val = canteen, items = items)
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
    l = 0
    for _ in canteens:
        l += 1
    if l == 0:
        success=False
    else:

        canteendata = adminChecker.find({'canteen':canteen})[0] 
        if canteendata['password'] == password:
            success = True
        else:
            success = False
    price = {}
    if success:
        menu = []
        for m in menuInstance.db.menu.find():
            menu.append(m['name'])
            # price[m['']]
        print(menu)
        return render_template('main.html',items = menu,length = len(menu))
        
    else:
        return jsonify({"Error":"Login failed.. Check Username Password"})




@app.route("/pay")
def pay():
    
    menuloader = menuInstance.db.menu
    


    its = []
    for i in menuloader.find():
        item = {}
        item['item_name'] = i['item_name']
        item['item_code']  = i['item_code']
        item['price'] = i['price']
        print('-------------->', i)
        its.append(item)
        #print("---> ", type(i))
    
    return render_template('cart.html',items = its,length = len(its))
       
    #return jsonify({'items':items})
@app.route('/transact', methods=['POST'])

def transact():
   # data = request.form
    #print(data)
 #   print('Length of Data :',len(data))
  #  print('First :', data['item'][0])
    menuloader = menuInstance.db.menu
    total =0
    d = request.form
    d = d.to_dict(flat=False)
    item_price = 0

    for i in range(0,len(d['item'])):
        for j in menuloader.find({'item_name' : d['item'][i]}):
            
            print(j['price'],' type :',type(j['price']))

            item_price= j['price']


        total  += int(d['qty'][i])*int(item_price)
        print('Total Cost :',total)

    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,
)   
    data = {}
    data['cost'] = total
    data['canteen'] = canteenF
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = path +'/QRCode.jpg'
    os.remove(img_path)
    print("File Removed!")
    img.save(img_path)

    return render_template('QRCode.html')
    




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
