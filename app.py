import coffeescript, flask, werkzeug, os
from fbx_test import fbx_test

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'fbx'

# Index page
@app.route("/")
def index():
    return flask.render_template('index.html', fbx_json = fbx_test())

# Compile FBX to JSON
@app.route("/fbx/<file>")
def fbx(file):
    return fbx_test()

# Compile coffeescript to javascript
@app.route('/coffee/<file>')
def coffee(file):
    return coffeescript.compile_file('coffee/' + file + '.coffee')

# Upload page
@app.route('/upload_fbx', methods = ['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        if file and file.filename.endswith('.fbx'):
            filename = werkzeug.secure_filename(file.filename)
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except:
                return 'Fail in file.save()'
                
            return 'Fbx was uploaded'
    return '''
    <!doctype html>
    <title>Upload new FBX</title>
    <h1>Upload new FBX</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug = True)