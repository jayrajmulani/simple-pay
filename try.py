
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

menuInstance = PyMongo(app,uri = "mongodb://127.0.0.1:27017/menu")
@app.route('/')
def home_page():
    menu = []
    for m in menuInstance.db.menu.find():
        menu.append(m['name'])
    print(menu)
    return render_template('try.html',items = menu,length = len(menu))
        
app.run(debug=True)