from flask import Flask, render_template, request  # importing the render_template function
import pymysql

app = Flask(__name__)
#Configure MySQL
conn = pymysql.connect(host='localhost', user='root', password='', db='finalairline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
    # database name is 'air_ticket_reservations'

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
    cursor = conn.cursor()
    if usrtype == 'staff':
      query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
    elif usrtype == 'customer':
      query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    
    cursor.execute(query, (username, password))
    #stores the results in a variable
    # data = result of query
    data = cursor.fetchone()
    cursor.close()
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
  DOB = request.form['date_of_birth']
    
  #cursor used to send queries
  cursor = conn.cursor()
    
  query = 'SELECT * FROM customer WHERE email = %s'
  cursor.execute(query, (email))
  #stores the results in a variable
  # data = result of query
  data = cursor.fetchone()
  # use fetchall() if you are expecting more than 1 data row
  error = None
    
  if(data): #if data exists
    error = "This user already exists"
    cursor.close()
    return render_template('registerCust.html', error = error)
  else:
    ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #insert query
    cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country,DOB))
    conn.commit()
    cursor.close()
    return render_template('startpage.html')

app.run(debug = True)
