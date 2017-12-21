from flask import Flask, render_template, redirect
import requests
import lxml.etree
import threading
import math
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.dirname(os.path.abspath(__file__))
dbpath = os.path.join(basedir, '64.db')
dbpath = dbpath.replace("\\", "\\\\")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+ dbpath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPDATING'] = False
db = SQLAlchemy(app)


class Img(db.Model):
    __tablename__ = "img"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))

def update():
    try:
        with app.app_context():
            app.config['UPDATING'] = True
            Img.query.delete()
            urls = spider()
            for url in urls:
                img = Img(url=url)
                db.session.add(img)
            db.session.commit()
    except Exception as e:
        print(e)
    finally:
        app.config['UPDATING'] = False


def spider(index_url = "https://movie.douban.com/people/49583935/collect"):
    urls = []
    next_url = index_url
    while next_url:
        resp = requests.get(next_url)
        html = lxml.etree.HTML(resp.text)
        items = html.xpath('//div[@class="item"]')
        for item in items:
            _ = item.xpath('./div[@class="pic"]/a[@class="nbg"]/img/@src')
            if _:
                urls.append(_[0])
        _ = html.xpath('//span[@class="next"]/a/@href')
        if _:
            next_url = _[0]
        else:
            break
    return urls

@app.route("/u")
def u():
    if app.config['UPDATING']:
        return "updating..."
    threading.Thread(target=update).start()
    return "updating..."

@app.route('/')
def index():
    if app.config['UPDATING']:
        return "updating..."
    imgs = Img.query.all()
    urls = [x.url for x in imgs]
    if not urls:
        return redirect("u")
    n_urls = []
    for url in urls:
        n_url = url.strip()
        n_urls.append(n_url)
    i = 1
    d = {}
    height = math.ceil(len(n_urls)/18)
    while i <= height:
        d[i] = n_urls[(i-1)*18:i*18]
        i += 1
    
    return render_template('index.html', d =d, last=urls[-1])
    
if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()