from flask import Flask, render_template  # importing the render_template function

app = Flask(__name__)
# home route
@app.route("/showlogin")
def hello():
    return render_template('login.html')

app.run(debug = True)
