from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    
    f = open('1.txt', 'r')
    urls = f.readlines()
    f.close()
    n_urls = []
    for url in urls:
        n_url = url.strip()
        n_urls.append(n_url)
    i = 1
    d = {}
    while i <= 40:
        d[i] = n_urls[(i-1)*18:i*18]
        i += 1
    
    return render_template('index.html', d =d)
    
if __name__ == "__main__":
    app.run()