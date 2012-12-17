import coffeescript, flask, werkzeug, os
from fbx_test import fbx_test
app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'fbx'

@app.route("/")
def hello():
    return flask.render_template('index.html', fbx_json = fbx_test())

@app.route("/<file>.fbx")
def fbx(file):
    return fbx_test()

# For serving coffee script code
@app.route('/coffee/<file>')
def js(file):
    return coffeescript.compile_file('coffee/' + file + '.coffee')

@app.route('/upload_fbx', methods = ['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        if file and file.filename.endswith('.fbx'):
            filename = werkzeug.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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