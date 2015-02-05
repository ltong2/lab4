from flask import Flask
app = Flask(__name__)
@app.route('/hello')
def hello():
    return '<h1>hello flask</h1>'
@app.route('/second')
@app.route('/second/<name>')
def hello2(name ='Flask'):
    return '<h1>hello %s flask(second Test)</h1>' % name


if __name__ == '__main__':
    app.debug=True
    app.run()