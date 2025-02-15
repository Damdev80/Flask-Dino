from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    request.method
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/recover')
def recover_password():
    return render_template('recover.html')
    

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')