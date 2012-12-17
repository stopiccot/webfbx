import coffeescript, flask
from fbx_test import fbx_test
app = flask.Flask(__name__)

@app.route("/")
def hello():
    return flask.render_template('index.html', fbx_json = fbx_test())

@app.route("/<file>.fbx")
def fbx(file):
    return fbx_test()

@app.route('/js/<file>')
def js(file):
    return coffeescript.compile_file('views/' + file + '.coffee')

if __name__ == "__main__":
    app.run(debug = True)