from flask import Flask, render_template, url_for, request, redirect
from json import load, dump
from random import sample

with open('urls.json', 'r') as urlsFile:
	urlsData = load(urlsFile)

def gencode():
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    result = ''.join(sample(list(chars), 6))
    if result in urlsData:
        return gencode()
    return result

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userURL = request.form.get('urlInput')
        code = gencode()
        urlsData[code] = userURL

        with open('urls.json', 'w') as urlsFile:
            dump(urlsData, urlsFile)
        
        return render_template('url.html', url=userURL, shortURL=code)
    else:
        return render_template('index.html')

@app.route('/<url>')
def url(url):
    if url in urlsData:
        return redirect(urlsData[url])
    return '<h1 style="font-family: sans-serif">404</h1><p>Page not found</p>'

if __name__ == '__main__':
	app.run('0.0.0.0', port=5001)
