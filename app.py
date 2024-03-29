import coffeescript, flask, werkzeug, os, json
from fbx_to_json import fbx_to_json

app = flask.Flask(__name__)

# Index page
@app.route("/")
def index():
    return flask.render_template('index.html')

# Compile FBX to JSON
@app.route("/fbx/<file>")
def fbx(file):
    return json.dumps(fbx_to_json('fbx/' + file))

# Compile coffeescript to javascript
@app.route('/coffee/<file>')
def coffee(file):
    return coffeescript.compile_file('coffee/' + file)

# Upload handler
@app.route('/upload_fbx', methods = ['GET', 'POST'])
def upload_fbx():
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