from flask import Flask, render_template, request, session, url_for, redirect  # importing the render_template function
import pymysql

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
  
@app.route('/logAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    usertype = request.form['usertype']
    cursor = conn.cursor()
    if usertype == 'staff':
      query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
    elif usertype == 'customer':
      query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    
    cursor.execute(query, (email, password))
    #stores the results in a variable
    # data = result of query
    data = cursor.fetchone()
    cursor.close()
    #print(data)
    
    if(data):

      if usertype == 'staff':
        session['username'] = email
        return redirect(url_for('loadstaffdata')) #redirect to staff home page
      elif usertype == 'customer':
        session['username'] = email
        return redirect(url_for('loadcustomerdata')) #redirect to customer home page
      
    else:
      error = 'Invalid login or username'
      return render_template('login.html')
      
      
@app.route('/loadcustomerdata')
def loadcustomerdata():
  email = session['username']
  cursor = conn.cursor();
  query = 'SELECT purchase.t_id, Ticket.airline_operator, ticket.flight_num FROM purchase, Ticket, Flight WHERE purchase.t_id = Ticket.t_id AND Ticket.airline_operator = Flight.airline_operator AND Ticket.flight_num = Flight.flight_num AND Flight.dept_datetime > curdate() AND purchase.email = %s'
  cursor.execute(query, (email))
  data = cursor.fetchall()
  cursor.close()
  return render_template('customerhome.html', email=email, ticketinfo=data)
      
      



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
    ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #insert query
    cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country,DOB))
    conn.commit()
    cursor.close()
    return render_template('startpage.html')

@app.route('/registerStaff')
def registerStaff():
    return render_template('registerStaff.html')
    
@app.route('/AuthStaff', methods=['GET', 'POST'])
def AuthStaff():
  username = request.form['username']
  password = request.form['password']
  f_name = request.form['first_name']
  l_name = request.form['last_name']
  DOB = request.form['date_of_birth']
  airline_name = request.form['airline_name']

  cursor = conn.cursor()
  query = 'SELECT * FROM airline_staff WHERE username = %s'
  cursor.execute(query, (username))
  data = cursor.fetchone()
  if(data):
    error = "This user already exists"
    return render_template('registerStaff.html')
  else:
    ins = 'INSERT INTO Airline_staff VALUES(%s, %s, md5(%s), %s, %s, %s)'
    cursor.execute(ins, (username, airline_name, password, f_name, l_name, DOB))
    conn.commit()
    cursor.close()
    return render_template('startpage.html')

@app.route('/loadstaffdata')
def loadstaffdata():
    username = session['username']
    return render_template('staffhome.html', username=username)


@app.route('/addAirport')
def addAirportPage():
    return render_template('addAirport.html')

@app.route('/addAirportAuth', methods=['POST'])
def addAirport():
    id = request.form['airport_id']
    name = request.form['airport_name']
    city = request.form['city']
    
    cursor = conn.cursor()
    query = 'insert into airport values (%s, %s, %s)'
    cursor.execute(query, (id, name, city))
    conn.commit()
    cursor.close()
    
    return redirect(url_for('loadstaffdata'))



@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/login')
app.run(debug = True)

