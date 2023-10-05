from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.v7tnfvp.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('main.html')


@app.route("/main", methods=["POST"])
def room_post():

    response = requests.get("https://gakusei.suumo.jp/jj/chintai/ichiran/FR301FC005/?fw2=&mt=9999999&cn=9999999&ra=013&et=9999999&shkr1=03&ar=030&bs=040&ct=9999999&shkr3=03&shkr2=03&mb=0&rn=0005&shkr4=03&cb=0.0")
    soup = BeautifulSoup(response.text, 'html.parser')

    rooms = soup.select('#js-bukkenList > div > div')
    for room in rooms:
        title = room.select_one('.property_inner-title > .js-cassetLinkHref').text
        price = room.select_one('.detailbox-property-point').text
        proxy = room.select_one('td > div:nth-of-type(2)').text
        image = room.select_one('li > img[src]')
    # 이미지 태그가 존재하는 경우

        doc = {
            'title': title,
            'price': price,
            'proxy': proxy,
            'image': image
        }

        db.rooms.insert_one(doc)

        return jsonify({'msg': '完了'})


@app.route("/main", methods=["GET"])
def main_get():
    all_room = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'result': all_room})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'POST(完了) 接続完了!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
