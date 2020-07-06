import os
from flask import Flask, flash, render_template, url_for, request, redirect, jsonify
from werkzeug.utils import secure_filename
from models.load_model import load_file as lf

# Application
app = Flask(__name__)

# App Configuration
app.config['SECRET_KEY'] = '0779a2f700b8a834c5ee8e318d69cec9'

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload Route
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    return render_template('upload.html')

# Upload Handler
@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        if filename != '':            
            file.save(os.path.join('uploads', filename))
        else:
            flash('No File has been selected')

    return redirect(url_for('home'))


@app.route('/result', methods=['POST', 'GET'])
def result_handler():
    model = request.args.get('model')
    result = request.args.get('result')
    if result == str(1):
        result='High Level of Knowledge'
    return render_template('result.html', model=model, result=result)

@app.route('/test-run/', methods=['POST', 'GET'])
def test_run():
    if request.method == "POST":
        test = request.form.to_dict()
        test_input = test['test_input']
        test_input = [test_input.split(',')]
        predictions = lf.ml_model(os.path.join('uploads', 'model.sav'), test_input)

        return redirect(url_for('result_handler', model='Student Knowledge Prediction', result=str(predictions['results'][0])))

    else:
        return render_template('run.html')

if __name__ == '__main__':
    app.run(debug=True)