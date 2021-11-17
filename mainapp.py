from flask import Flask, render_template  # importing the render_template function

app = Flask(__name__)
# home route
@app.route("/")
def hello():
    return render_template('startpage.html')
    
@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/registerCustomer')
def registerCustomer():
  return render_template('registerCust.html')

app.run(debug = True)
