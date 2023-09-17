from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.v7tnfvp.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogtitle = soup.select_one('meta[property="og:title"]')['content'].split(':')[0]
    ogdesc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': ogtitle,
        'desc': ogdesc,
        'image': ogimage,
        'star': star_receive,
        'comment': comment_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg': '保存完了!'})


@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({}, {'_id': False}))
    return jsonify({'result': all_movies})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
