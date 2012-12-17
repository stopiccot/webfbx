import coffeescript, flask
from fbx_test import fbx_test
app = flask.Flask(__name__)

@app.route("/")
def hello():
    return fbx_test()#flask.render_template('index.html')

@app.route("/fbx")
def fbx():
    return fbx_test()

@app.route('/js/<file>')
def js(file):
    return coffeescript.compile_file('views/' + file + '.coffee')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)