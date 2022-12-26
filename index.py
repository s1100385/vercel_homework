from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("final-4f34e-firebase-adminsdk-coitm-c796101b62.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>楊子青Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=tcyang>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>子青簡介網頁</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/about")
def about():
    return render_template("aboutme.html")

@app.route("/webhook", methods=["POST"])
def webhook4():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    
    if (action == "asktags"):
        tags =  req.get("queryResult").get("parameters").get("tags")
        if (tags == "小說"):
            tags = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (tags == "漫畫"):
            tags = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的書籍是：" + tags + "，相關書籍：\n"

        collection_ref = db.collection("book")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if tags in dict["tags"]:
                result += "書名：" + dict["bookname"] + "\n"
                result += "價錢：" + dict["price"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))


if __name__ == "__main__":
    app.run()