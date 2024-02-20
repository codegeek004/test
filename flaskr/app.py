from flask import Flask, render_template
from reception_table import reception
app = Flask(__name__)
app.secret_key = 'dev144'
@app.route('/')
def index():
    return render_template('index.html')
app.register_blueprint(reception)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
