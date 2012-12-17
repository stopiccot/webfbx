import coffeescript, flask, werkzeug, os, json
from fbx_test import fbx_test

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'fbx'

# Index page
@app.route("/")
def index():
    return flask.render_template('index.html', fbx_json = fbx_test('fbx/test.fbx'))

# Compile FBX to JSON
@app.route("/fbx/<file>")
def fbx(file):
    return fbx_test('fbx/' + file)

# Compile coffeescript to javascript
@app.route('/coffee/<file>')
def coffee(file):
    return coffeescript.compile_file('coffee/' + file)

# Upload hander
@app.route('/upload_fbx', methods = ['GET', 'POST'])
def upload_fbx_hanlder():
    if flask.request.method == 'POST':
        print(flask.request.files)
        file = flask.request.files.get('files[]')
        print(file)
        if file:
            print(file.filename)
            if file.filename.endswith('.fbx'):
                filename = werkzeug.secure_filename(file.filename)
                print(filename)
                file.save(os.path.join('./fbx', filename))

                return json.dumps({
                    'name' : file.filename,
                    'size' : 0,
                    'url'  : '/fbx/' + filename,
                })

    # Return empty json on error
    return json.dumps({})

if __name__ == "__main__":
    app.run(debug = True)