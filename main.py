from flask import Flask, render_template
import img
import math

app = Flask(__name__)


@app.route('/')
def index():
    try:
        img.main()
    except:
        pass
    f = open('img_urls.txt', 'r')
    urls = f.readlines()
    f.close()
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
    
    return render_template('index.html', d =d)
    
if __name__ == "__main__":
    app.run(debug=True)
