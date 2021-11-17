from flask import Flask, render_template, request  # importing the render_template function

app = Flask(__name__)
# home route
@app.route("/")
def hello():
    return render_template('startpage.html')
    
@app.route('/login')
def login():
  return render_template('login.html')
  
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    usrtype = request.form['usrtype']

    if usrtype == 'staff':
      query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
    elif usrtype == 'customer':
      query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    else:
      query = 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)'

    data=None
    # data = result of query
    error = None
    if(data):

      session['username'] = username
      if usrtype == 'staff':
        return render_template('login.html') #redirect to staff home page
      elif usrtype == 'customer':
        return render_template('login.html') #redirect to customer home page
      
    else:
      error = 'Invalid login or username'
      return render_template('login.html')


@app.route('/registerCustomer')
def registerCustomer():
  return render_template('registerCust.html')

@app.route('/AuthCustomer', methods=['GET', 'POST'])
def AuthCustomer():
  email = request.form['email']
  name = request.form['name']
  password = request.form['password']
  building_number = request.form['building_number']
  street = request.form['street']
  city = request.form['city']
  state = request.form['state']
  phone_number = request.form['phone_number']
  passport_number = request.form['passport_number']
  passport_expiration = request.form['passport_expiration']
  passport_country = request.form['passport_country']
  date_of_birth = request.form['date_of_birth']
    
  query = 'SELECT * FROM customer WHERE email = %s'
  #data = execute and get the person
  error = None
  if(data): #if data exists
    error = "This user already exists"
    return render_template('registerCustomer.html', error = error)
  else:
    ins = 'INSERT INTO customer VALUES(%s, %s, %s, %d, %s, %s, %s, %s, %s, %s, %s, %s)'
    #insert query
    return render_template('index.html')

app.run(debug = True)
