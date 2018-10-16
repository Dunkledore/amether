from quart import Flask, request, flash, redirect, url_for, send_from_directory
import os
import string
import random
from analyser import create_chart

UPLOAD_FOLDER = 'chats'
ALLOWED_EXTENSIONS = {"zip"}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = (request.files)['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(32)])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            create_chart(filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory("outputs", f"{filename}.png")



if __name__ == "__main__":
    app.run()