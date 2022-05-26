from flask import Flask, render_template, request, session, url_for, redirect  # importing the render_template function
import pymysql
import datetime
 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#Configure MySQL
conn = pymysql.connect(host='localhost', user='root', password='', db='finalairline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
    # database name is 'finalairline'

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
    try:
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
        error = None
        #print(data)
        
        if(data):
            if usertype == 'staff':
                session['username'] = (email, 1)
                return redirect(url_for('staffHome')) #redirect to staff home page
            elif usertype == 'customer':
                session['username'] = (email, 0)
                return redirect(url_for('customerHome')) #redirect to customer home page
        else:
          error = 'Invalid login or username'
          return render_template('login.html', error = error)
    except conn.Error as e:
        print("Error reading data from airline_staff or customer table while login", e)
    finally:
        cursor.close()
    error = 'Invalid login attempt. Please try again'
    return render_template('login.html', error = error)
      
@app.route('/customerHome')
def customerHome():
    error = None
    try:
        if session['username'][1] != 0:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    email = session['username'][0]
    num = session['username'][1]
    try:
        cursor = conn.cursor();
        query = 'SELECT purchase.t_id, Ticket.airline_operator, ticket.flight_num FROM purchase, Ticket, Flight WHERE purchase.t_id = Ticket.t_id AND Ticket.airline_operator = Flight.airline_operator AND Ticket.flight_num = Flight.flight_num AND Flight.dept_datetime > curdate() AND purchase.email = %s'
        cursor.execute(query, (email))
        data = cursor.fetchall()
        cursor.close()
    except conn.Error as e:
        print("Error reading data from purchase, Ticket, Flight table", e)
    finally:
        cursor.close()
    return render_template('customerhome.html', email=email, ticketinfo=data, num=num)
      
      



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
    error = None
    try:
        #cursor used to send queries
        cursor = conn.cursor()
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, (email))
        #stores the results in a variable
        # data = result of query
        data = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        error = None
    except conn.Error as e:
        print("Error reading data from customer", e)
        error = "Error reading data from customer. Please try again"
        cursor.close()
        return render_template('registerCust.html', error = error)
    if(data): #if data exists
        error = "This user already exists"
        cursor.close()
        return render_template('registerCust.html', error = error)
    else:
        try:
            ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            #insert query
            cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country,DOB))
            conn.commit()
            cursor.close()
            return render_template('startpage.html')
        except conn.Error as e:
            print("Error writing data into customer", e)
            cursor.close()
            error = "Error writing data into customer. Please try again"
    return render_template('registerCust.html', error = error)
        

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
    error = None
    try:
        cursor = conn.cursor()
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
    except conn.Error as e:
        print("Error reading data from airline_staff", e)
        error = "Error reading data from airline_staff. Please try again"
        cursor.close()
        return render_template('registerStaff.html', error = error)
    if data:
        error = "This user already exists"
        return render_template('registerStaff.html')
    else:
        try:
            ins = 'INSERT INTO Airline_staff VALUES(%s, %s, md5(%s), %s, %s, %s)'
            cursor.execute(ins, (username, airline_name, password, f_name, l_name, DOB))
            conn.commit()
            cursor.close()
            return render_template('startpage.html')
        except conn.Error as e:
            print("Error writing data into airline_staff", e)
            cursor.close()
            error = "Error writing data into airline_staff. Please try again"
    return render_template('registerStaff.html', error = error)

@app.route('/staffHome')
def staffHome():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][0]
    return render_template('staffhome.html', username=username)


@app.route('/addAirport')
def addAirportPage():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    return render_template('addAirport.html')

@app.route('/addAirportAuth', methods=['POST'])
def addAirport():
    id = request.form['airport_id']
    name = request.form['airport_name']
    city = request.form['city']
    try:
        cursor = conn.cursor()
        query = 'insert into airport values (%s, %s, %s)'
        cursor.execute(query, (id, name, city))
        conn.commit()
        cursor.close()
    except conn.Error as e:
        print("Error writing data into airport table", e)
    finally:
        cursor.close()
    return redirect(url_for('staffHome'))

@app.route('/addAirplane')
def addAirplane():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    airline=getStaffAirline()
    cursor=conn.cursor()
    query = 'Select * from airplane where airline_name = %s'
    cursor.execute(query, (airline))
    airplanes = cursor.fetchall()
    return render_template('addAirplane.html', airplanes=airplanes)

@app.route('/addAirplaneAuth', methods=['POST'])
def addAirplaneAuth():
    id = request.form['id']
    owner_name = request.form['owner']
    seats = request.form['seats']
    try:
        cursor = conn.cursor()
        query = 'insert into airplane values (%s, %s, %s)'
        cursor.execute(query, (id, owner_name, seats))
        conn.commit()
        cursor.close()
    except conn.Error as e:
        print("Error inserting data into airplane table", e)
    finally:
        cursor.close()
    return redirect(url_for('staffHome'))

def getStaffAirline():
    username = session['username'][0]
    try:
        cursor = conn.cursor()
        query = 'select airline_name from Airline_staff where username = %s'
        cursor.execute(query, (username))
        airline = cursor.fetchone()['airline_name']
        cursor.close()
        return airline
    except conn.Error as e:
        print("Error reading data into airline_staff table", e)
    finally:
        cursor.close()
    return None
    
@app.route('/createFlight')
def createFlight():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    airline = getStaffAirline()
    if airline is None:
        error = 'Staff has no airline? Please log in again'
        session.pop('username')
        return render_template('error.html', error=error)
    
    cursor = conn.cursor()
    query = 'select name from airport'
    cursor.execute(query)
    airports = cursor.fetchall()
    
    query = 'select airplane_id from airplane where airline_name = %s' #Specified that the airline that the staff works for is the only airline we want?
    cursor.execute(query, (airline))
    availableairplane = cursor.fetchall()

    #query = 'select flight_num, dept_datetime, status from flight where airline_operator = %s'
    query = 'select * from flight where airline_operator = %s and ((dept_datetime between curdate() and date_add(curdate(), interval 30 day)) or (arrive_datetime between curdate() and date_add(curdate(), interval 30 day)))'
    cursor.execute(query, (airline))
    futureFlights = cursor.fetchall()
    
    cursor.close()
    return render_template('createFlight.html', airports=airports, availableairplane=availableairplane, futureFlights=futureFlights)

@app.route('/createFlightAuth', methods=['POST'])
def createFlightAuth():
    flightnum = request.form['flightnum']
    arrivetime = request.form['arrivetime']
    departtime = request.form['departtime']
    airline_operator = request.form['airline_operator']
    owner_name = request.form['owner_airline']
    departnum = request.form['departnum']
    arrivenum = request.form['arrivenum']
    airplane_num = request.form['airplanenum']
    base_price = request.form['base_price']
    status = request.form['status']
    try:
        cursor = conn.cursor()
        query = 'insert into flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (flightnum, departtime, airline_operator, owner_name, arrivetime, departnum, arrivenum, airplane_num, base_price, status))
        conn.commit()
        query = 'select max(t_id) from Ticket'
        cursor.execute(query)
        data=cursor.fetchall()
        lasttid=data[0]['max(t_id)']
        if not lasttid:
            lasttid = -1
        query = 'select * from airplane where airplane_id=%s'
        cursor.execute(query, airplane_num)
        data = cursor.fetchall()
        numseats=data[0]['num_seats']
        print(lasttid,flightnum,departnum,departnum,airline_operator,numseats)
        for i in range(1, numseats):
            try:
                query = 'insert into Ticket values (%s, %s, %s, %s, %s)'
                cursor.execute(query, (lasttid+i,flightnum,departtime,airline_operator,None))
                conn.commit()
            except conn.Error as e:
                print("Error inserting data into ticket table", e)
        
    except conn.Error as e:
        print("Error inserting data into flight table", e)
    finally:
        cursor.close()
    return redirect(url_for('staffHome'))
    
@app.route('/changeStatus', methods=['POST'])
def changeStatus():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    cursor = conn.cursor()
    airline = getStaffAirline()
    flightnum = request.form['flight_num']
    status = request.form['status']
    if not status:
        error = 'no new status selected'
        return redirect(url_for('createFlight', error=error))
    
    query = 'update flight set status=%s where flight_num=%s and airline_operator = %s'
    cursor.execute(query, (status, flightnum, airline))
    conn.commit()
    cursor.close()
    return redirect(url_for('createFlight'))

@app.route('/createFlight/viewRatings', methods=['POST'])
def viewRatings():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    cursor = conn.cursor()
    flightnum = request.form['fli']
    query = 'select * from review where flight_num=%s'
    cursor.execute(query, (flightnum))
    ratedata=cursor.fetchall()
    total=0
    count=0
    for i in ratedata:
        count+=1
        total+=i['rating']
    print(ratedata)
    avgrate=total/count
    print(total)
    return render_template('viewflightRatings.html', ratedata=ratedata, avgrate=avgrate)


    
    
@app.route('/viewCustomers')
def viewCustomers():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    
    airline = getStaffAirline()
        
    cursor = conn.cursor()
    query = 'select email, count(t_id) as tickets from purchase natural join Ticket where airline_operator= %s and purchasedate_time >= date_sub(curdate(), interval 1 year) group by email having tickets >= all (select count(t_id) from purchase natural join ticket  where airline_operator = %s and purchasedate_time >= date_sub(curdate(), interval 1 year) GROUP by email)'
    cursor.execute(query, (airline, airline))
    data = cursor.fetchall()
    cursor.close()
    n=len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j]['tickets'] < data[j+1]['tickets']:
                data[j],data[j+1]= data[j+1],data[j]
    user=data[0]['email']
    cursor = conn.cursor()
    query = 'select * from purchase Natural Join Ticket Natural Join Flight where email=%s and date(dept_datetime) < now() and date(arrive_datetime) < now() group by t_id'
    cursor.execute(query,(user))
    flights=cursor.fetchall()
    query= 'select * from Airport'
    cursor.execute(query)
    Airport_data=cursor.fetchall()
    cursor.close()
    return render_template('viewCustomers.html', results=data[0:1],flights=flights,Airports=Airport_data)
    #return render_template('viewCustomers.html', results=data[0:1])
@app.route('/viewReports')
def viewReports():
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)

    airline = getStaffAirline()
    currentmonth = datetime.datetime.now().month
    monthtickets = []
        
    cursor = conn.cursor()
    for i in range(0, 12):
        query = 'select count(t_id) as num_tic from purchase natural join ticket where year(purchasedate_time) = year(curdate() - interval ' + str(i) + ' month) and month(purchasedate_time) = month(curdate() - interval ' + str(i) + ' month) and airline_operator=%s'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        salemonth = ((currentmonth - (i+1)) % 12) + 1
        print (data[0]['num_tic'])
        monthtickets.append([data[0]['num_tic'], salemonth])
        print(monthtickets)
    cursor.close()
    return render_template('viewReports.html', results=monthtickets)


@app.route('/viewReports/dates', methods=['POST'])
def viewReportsDates():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    
    airline = getStaffAirline()
    start = request.form['start']
    end = request.form['end']
    
    cursor = conn.cursor()
    query = 'select count(t_id) as num_tic from purchase natural join ticket where airline_operator=%s and purchasedate_time between %s and %s'
    cursor.execute(query, (airline, start, end))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    
    return render_template('viewReportswDate.html', tot_sales=data[0]['num_tic'], start=start, end=end)

@app.route('/Revenue')
def Revenue():
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    
    airline = getStaffAirline()
    cursor = conn.cursor()
    query = 'select sum(sold_price) as yearrev from purchase natural join ticket where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 year) and curdate()'
    cursor.execute(query, (airline))
    yearrev = cursor.fetchall()
    query = 'select sum(sold_price) as monthrev from purchase natural join ticket where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 month) and curdate()'
    cursor.execute(query, (airline))
    monthrev = cursor.fetchall()
    cursor.close()
    return render_template('viewRevenue.html', yearrev=yearrev, monthrev=monthrev)

@app.route('/topDestinations')
def topDestinations():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a staff. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying staff", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    
    airline = getStaffAirline()
    cursor = conn.cursor()
    query = 'select arrive_airport_id, count(t_id) from ticket NATURAL JOIN flight NATURAL JOIN purchase where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 3 month) and curdate() group by arrive_airport_id'
    cursor.execute(query, (airline))
    monthdata=cursor.fetchall()
    #sort and get top 3
    query = 'select arrive_airport_id, count(t_id) from ticket NATURAL JOIN flight NATURAL JOIN purchase where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 year) and curdate() group by arrive_airport_id'
    cursor.execute(query, (airline))
    yeardata=cursor.fetchall()
    query= 'select * from Airport'
    cursor.execute(query)
    Airport_data=cursor.fetchall()
    cursor.close()

    n=len(monthdata)
    for i in range(n):
        for j in range(0, n-i-1):
            if monthdata[j]['count(t_id)'] < monthdata[j+1]['count(t_id)']:
                monthdata[j],monthdata[j+1]= monthdata[j+1],monthdata[j]
    r=len(yeardata)
    for i in range(n):
        for j in range(0, r-i-1):
            if yeardata[j]['count(t_id)'] < yeardata[j+1]['count(t_id)']:
                yeardata[j],yeardata[j+1]= yeardata[j+1],yeardata[j]
    for i in monthdata:
        for j in Airport_data:
            if j['airport_id']==i['arrive_airport_id']:
                i['city']=j['city']
    for i in yeardata:
        for j in Airport_data:
            if j['airport_id']==i['arrive_airport_id']:
                i['city']=j['city']
    #return redirect(url_for('createFlight'))
    return render_template('topDestinations.html', monthdata=monthdata[0:3], yeardata=yeardata[0:3])

@app.route('/customerSearch')
def custSearch():
    return render_template('custSearch.html')

@app.route('/custsearchResult', methods=['GET', 'POST'])
def custsearchResult():
    '''
    srcName = request.form['srcName']
    srcCity = request.form['srcCity']
    dstName = request.form['dstName']
    dstCity = request.form['dstCity']
    '''
    dstid = request.form['dstid']
    srcid = request.form['srcid']
    departtime = request.form['departtime']
    arrivetime = request.form['arrivetime']
    departtime.replace('T',' ')
    print(departtime,dstid,srcid)
    try:
        #cursor used to send queries
        cursor = conn.cursor()
        #query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where date(dept_datetime) <= %s and date(arrive_datetime) <= %s and %s = S.name and %s = D.name and %s = S.city and %s = D.city and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id'
        if arrivetime == '': #1 way
            print('1way')
            query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
            cursor.execute(query, (departtime, srcid, dstid))
        else: #2 way, list of flights to dst
            print('2way')
            query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and date(arrive_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
            cursor.execute(query, (departtime, arrivetime, srcid, dstid))
        #stores the results in a variable
        data = cursor.fetchall()
        print("here", data)
        error = None
        if not data:
            error = 'No results met your filters to dst: Please try again'
        if arrivetime != '': #2 way, list of possible return flights
            try:
                #Searches for ANY POSSIBLE FLIGHT DURING THE TIME FRAME. TIMEFRAME IS NOT CALCULATED BASED ON PREVIOUSLY CALCULATED FLIGHTS TO THE DST
                query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and date(arrive_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
                cursor.execute(query, (departtime, arrivetime, dstid, srcid)) #switched for the way back
                data2 = cursor.fetchall()
                cursor.close()
                if not data2:
                    print('No results met your filters back to src: Please try again')
                    error2 = 'No results met your filters back to src: Please try again'
                return render_template('custsearch.html', error=error, error2=error2, results=data, twoway=data2)
            except conn.Error as e:
                print("Error reading data from flight,airport as S, airport as D table", e)
                cursor.close()
                error = 'Invalid search filters: Please try again'
                return render_template('custsearch.html', error=error)
        cursor.close()
        return render_template('custsearch.html', error=error, results=data)
    except conn.Error as e:
        print("Error reading data from flight,airport as S, airport as D table", e)
        cursor.close()
        error = 'Invalid search filters: Please try again'
        return render_template('custsearch.html', error=error)
 
@app.route('/publicSearch')
def publicSearch():
    return render_template('search.html')

@app.route('/searchResult', methods=['GET', 'POST'])
def searchResult():
    '''
    srcName = request.form['srcName']
    srcCity = request.form['srcCity']
    dstName = request.form['dstName']
    dstCity = request.form['dstCity']
    '''
    dstid = request.form['dstid']
    srcid = request.form['srcid']
    departtime = request.form['departtime']
    arrivetime = request.form['arrivetime']
    departtime.replace('T',' ')
    print(departtime,dstid,srcid)
    try:
        #cursor used to send queries
        cursor = conn.cursor()
        #query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where date(dept_datetime) <= %s and date(arrive_datetime) <= %s and %s = S.name and %s = D.name and %s = S.city and %s = D.city and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id'
        if arrivetime == '': #1 way
            print('1way')
            query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
            cursor.execute(query, (departtime, srcid, dstid))
        else: #2 way, list of flights to dst
            print('2way')
            query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and date(arrive_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
            cursor.execute(query, (departtime, arrivetime, srcid, dstid))
        #stores the results in a variable
        data = cursor.fetchall()
        print("here", data)
        error = None
        if not data:
            error = 'No results met your filters to dst: Please try again'
        if arrivetime != '': #2 way, list of possible return flights
            try:
                #Searches for ANY POSSIBLE FLIGHT DURING THE TIME FRAME. TIMEFRAME IS NOT CALCULATED BASED ON PREVIOUSLY CALCULATED FLIGHTS TO THE DST
                query = 'select flight_num, airline_operator, dept_datetime, arrive_datetime, base_price, status from flight,airport as S, airport as D where dept_datetime > now() and date(dept_datetime) <= %s and date(arrive_datetime) <= %s and dept_airport_id = %s and arrive_airport_id = %s and dept_airport_id = S.airport_id and arrive_airport_id = D.airport_id group by dept_datetime'
                cursor.execute(query, (departtime, arrivetime, dstid, srcid)) #switched for the way back
                data2 = cursor.fetchall()
                cursor.close()
                if not data2:
                    print('No results met your filters back to src: Please try again')
                    error2 = 'No results met your filters back to src: Please try again'
                return render_template('search.html', error=error, error2=error2, results=data, twoway=data2)
            except conn.Error as e:
                print("Error reading data from flight,airport as S, airport as D table", e)
                cursor.close()
                error = 'Invalid search filters: Please try again'
                return render_template('search.html', error=error)
        cursor.close()
        return render_template('search.html', error=error, results=data)
    except conn.Error as e:
        print("Error reading data from flight,airport as S, airport as D table", e)
        cursor.close()
        error = 'Invalid search filters: Please try again'
        return render_template('search.html', error=error)

@app.route('/customerhome/viewMyFlights', methods=['GET', 'POST'])
def viewMyFlights():
    error = None
    try:
        if session['username'][1] == 1:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    
    try:
        #cursor used to send queries
        cursor = conn.cursor()
        query = 'select ticket.t_id, flight_num, dept_datetime, airline_operator, sold_price from ticket, purchase where date(dept_datetime) >= now() and email = %s and ticket.t_id = purchase.t_id'
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchall()
        cursor.close()
        if not data:
            error = 'You have not made any future reservations. Please purchase tickets to see your history.'
        return render_template('viewFlights.html', error=error, results=data)
    except conn.Error as e:
        print("Error reading data from flight,airport as S, airport as D table", e)
        cursor.close()
        error = 'Invalid query: Please try again'
        return render_template('viewFlights.html', error=error)

@app.route('/customerhome/ratings')
def reviewTemplate():
    error = None
    try:
        if session['username'][1] == 1:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    return render_template('review.html')

@app.route('/reviewAuth', methods=['POST'])
def reviewAuth():
    username = session['username']
    flight_num = request.form['flight_num']
    dept_datetime = request.form['dept_datetime']
    airline_operator = request.form['airline_operator']
    rating = request.form['rating']
    comment = request.form['comment']
    if int(rating) > 5:
        error = 'rating is > 5'
        return render_template('review.html', error=error)
    if int(rating) < 0:
        error = 'rating is < 0'
        return render_template('review.html', error=error)
    # Verify that the flight is one they have PREVIOUSLY flown
    try:
        cursor = conn.cursor()
        query = 'select * from ticket as S, purchase as T where S.t_id = T.t_id and email = %s and flight_num = %s and dept_datetime = %s and airline_operator = %s and dept_datetime < now()'
        cursor.execute(query, (username, flight_num, dept_datetime, airline_operator))
        conn.commit()
    except conn.Error as e:
        print("Error reading data from ticket,purchase table", e)
        cursor.close()
        error = 'Ticket/Purchase Review attempt was unsuccessful, invalid Flight'
        return render_template('review.html', error=error)
    finally:
        cursor.close()
    data = cursor.fetchall()
    print(data)
    if not data:
        error = 'You have not been on that flight previously'
        return render_template('review.html', error=error)
    try:
        cursor = conn.cursor()
        query = 'insert into review values (%s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (username, flight_num, dept_datetime, airline_operator, rating, comment))
        conn.commit()
        cursor.close()
    except conn.Error as e:
        print("Error inserting data into review table", e)
        cursor.close()
        error = 'Review attempt was unsuccessful'
        return render_template('review.html', error=error)
    return redirect(url_for('customerHome'))

@app.route('/customerhome/purchaseTicket')
def purchaseTicket():
    error = None
    try:
        if session['username'][1] == 1:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    return render_template('purchaseTicket.html')

@app.route('/purchaseTicketAuth', methods=['POST'])
def purchaseTicketAuth():
    username = session['username']
    #Flight Info
    flightnum = request.form['flightnum']
    departdate = request.form['departdate']
    airline_operator = request.form['airline_operator']
    #Payment Info
    card_type = request.form['card_type']
    number = request.form['number']
    expiration = request.form['expiration']
    Cardname = request.form['Cardname']
    try:#incomplete
        cursor = conn.cursor()
        #Range of flights on that date
        query = 'select flight_num, dept_datetime, airline_operator from Flight where flight_num = %s and airline_operator = %s and month(dept_datetime) = month(%s) and day(dept_datetime) = day(%s) and year(dept_datetime) = year(%s)'
        cursor.execute(query, (flightnum, airline_operator, departdate, departdate, departdate))        
        data = cursor.fetchall()
        session['fnum'] = flightnum
        session['operator'] = airline_operator
        session['card'] = card_type
        session['c_num'] = number
        session['expiration'] = expiration
        session['c_name'] = Cardname
        return render_template('purchaseTicketFlight.html', results=data)
    except conn.Error as e:
        print("Error reading data from flight table", e)
        cursor.close()
    finally:
        cursor.close()
    return redirect(url_for('customerHome'))

@app.route('/purchaseTicketAuth2', methods=['POST'])
def purchaseTicketAuth2():
    username = session['username']
    try:
        flightnum = session['fnum']
        airline_operator = session['operator']
        card_type = session['card']
        number = session['c_num']
        expiration = session['expiration']
        Cardname = session['c_name']
    except KeyError as e:
        print("Error reading previous data of ticket purchase", e)
        error='Error reading previous data of ticket purchase'
        return render_template('purchaseTicket.html', error=error)
    #Flight Info
    departtime = request.form['departtime']
    try:
        cursor = conn.cursor()
        #YOU DONT SAY WHAT TID IS
        query = 'select t_id from ticket where flight_num = %s and dept_datetime = %s and airline_operator = %s and sold_price is NULL'
        cursor.execute(query, (flightnum, departtime, airline_operator))
        data = cursor.fetchone()
        '''
        print(data)
        print(flightnum)
        print(airline_operator)
        print(card_type)
        print(number)
        print(expiration)
        print(Cardname)
        print(departtime)
        '''
        if not data:
            query = 'select t_id from ticket where flight_num = %s and dept_datetime = %s and airline_operator = %s'
            cursor.execute(query, (flightnum, departtime, airline_operator))
            data = cursor.fetchone()
            if not data:
                error = 'Your specified datetime was incorrect. Please try again'
            else:
                error = 'All tickets of that flight are sold out. Please select another flight'
            cursor.close()
            return render_template('purchaseTicket.html', error=error)
        t_id = data['t_id']
        print(username,t_id,card_type,number,expiration,Cardname)
        query = 'insert into purchase values (%s, %s, %s, %s, %s, %s, now());'
        cursor.execute(query, (username[0], t_id, card_type, number, expiration, Cardname))
        #find which price you need to pay
        query = 'select base_price, num_seats, S.flight_num, S.dept_datetime, S.airline_operator from ticket as S, flight as T, airplane as U where t_id = %s and S.flight_num = T.flight_num and S.dept_datetime = T.dept_datetime and S.airline_operator = T.airline_operator and T.airplane_id = U.airplane_id'
        cursor.execute(query, (t_id))
        data = cursor.fetchone()
        print(data)
        base = data["base_price"]
        capacity = data["num_seats"]
        flight_num = data["flight_num"]
        dept_datetime = data["dept_datetime"]
        airline_operator = data["airline_operator"]
        query = 'select count(*) from ticket as S, flight as T where S.flight_num = T.flight_num and S.dept_datetime = T.dept_datetime and S.airline_operator = T.airline_operator and S.flight_num = %s and S.dept_datetime = %s and S.airline_operator = %s and S.sold_price is NULL'
        cursor.execute(query, (flight_num, dept_datetime, airline_operator))
        data = cursor.fetchone()
        if data["count(*)"] < (0.75 * capacity):
            query = 'update ticket set sold_price = %s where t_id = %s'
            cursor.execute(query, (base, t_id))
        else:
            query = 'update ticket set sold_price = %s * 1.25 where t_id = %s'
            cursor.execute(query, (base, t_id))
        cursor.execute(query, (t_id))
        conn.commit()
    except conn.Error as e:
        print("Error inserting data into ticket and/or purchase table", e)
        cursor.close()
    finally:
        cursor.close()
    confirm = 'You have purchased a ticket t_id: '
    confirm += str(t_id)
    confirm += '. However, you should really buy more tickets please. We totally have no ulterior motives relating to capitalism.'
    return render_template('purchaseTicket.html', confirm=confirm)

@app.route('/customerhome/trackMySpending', methods=['GET', 'POST'])
def trackSpendingDefault():
    error = None
    try:
        if session['username'][1] == 1:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    
    try:
        currentmonth = datetime.datetime.now().month
        monthdata = []
        cursor = conn.cursor()
        #Default sum
        query = 'select sum(sold_price) from purchase natural join ticket where email = %s and purchasedate_time between DATE_SUB(curdate(), interval 1 year) and curdate()'
        cursor.execute(query, (username))
        yeartotal = cursor.fetchone()
        if not yeartotal['sum(sold_price)']:
            yeartotal['sum(sold_price)'] = 0 #forces it from None to 0
        query = 'select sum(sold_price) from purchase natural join ticket where email = %s and purchasedate_time between DATE_SUB(curdate(), interval 6 month) and curdate()'
        cursor.execute(query, (username))
        total = cursor.fetchone()
        if not total['sum(sold_price)']:
            total['sum(sold_price)'] = 0 #forces it from None to 0
        total['sum(sold_price)'] = int(total['sum(sold_price)'])#forces it from string to int
        print(total)
        for i in range(1, 13): #Goes in order from Jan to Dec
            query = 'select sum(sold_price) from purchase natural join ticket where email = %s and purchasedate_time between DATE_SUB(curdate(), interval 6 month) and curdate() and month(purchasedate_time) = month(%s)'
            cursor.execute(query, (username, i))
            data = cursor.fetchone()
            if not data['sum(sold_price)']:
                data['sum(sold_price)'] = 0 #forces it from None to 0
            data['sum(sold_price)'] = int(data['sum(sold_price)'])#forces it from string to int
            monthdata.append(data)
        cursor.close()
        print(monthdata)
        most = 0 #max spending in a month
        for x in monthdata:
            if int(x['sum(sold_price)']) > most:
                most = int(x['sum(sold_price)'])
        if most == 0: 
            error = 'You have not made any reservations. Please purchase tickets to see your spending.'
            most = -1
            '''
            All datapoints should be 0 anyway. This just prevents a divide by 0 error
            '''
        else: #Absolutely completely a jork. I mean a joke. 
            error = 'Your spending level needs to be OVER 9000!!!'
        print(most)
        return render_template('trackSpending.html', error=error, results=monthdata, total=total, most=most)
    except conn.Error as e:
        print("Error reading data from purchase natural join ticket table", e)
        cursor.close()
        error = 'Invalid query: Please try again'
        return render_template('trackSpending.html', error=error)

@app.route('/customerhome/trackMySpending/results', methods=['GET', 'POST'])
def trackSpending():
    error = None
    try:
        if session['username'][1] != 1:
            error = 'You are not a customer. All active users have been logged out. Begone.'
            session.pop('username')
            return render_template('error.html', error=error)
    except KeyError as e:
        print("Error verifying customer", e)
        error = 'You have not logged in. All active users have been logged out. Begone.'
        return render_template('error.html', error=error)
    username = session['username'][1]
    
    start = request.form['start']
    end = request.form['end']
    error = None
    try:
        currentmonth = datetime.datetime.now().month
        monthdata = []
        cursor = conn.cursor()
        query = 'select sum(sold_price) from purchase natural join ticket where email = %s and purchasedate_time between %s and %s'
        cursor.execute(query, (username, start, end))
        total = cursor.fetchone()
        if not total['sum(sold_price)']:
            total['sum(sold_price)'] = 0 #forces it from None to 0
        total['sum(sold_price)'] = int(total['sum(sold_price)'])#forces it from string to int
        print(total)
        for i in range(1, 13): #Goes in order from Jan to Dec
            query = 'select sum(sold_price) from purchase natural join ticket where email = %s and purchasedate_time between %s and %s and month(purchasedate_time) = month(%s)'
            cursor.execute(query, (username, start, end, i))
            data = cursor.fetchone()
            if not data['sum(sold_price)']:
                data['sum(sold_price)'] = 0 #forces it from None to 0
            data['sum(sold_price)'] = int(data['sum(sold_price)'])#forces it from string to int
            monthdata.append(data)
        cursor.close()
        print(monthdata)
        most = 0 #max spending in a month
        for x in monthdata:
            if int(x['sum(sold_price)']) > most:
                most = int(x['sum(sold_price)'])
        if most == 0: 
            error = 'You have not made any reservations. Please purchase tickets to see your spending.'
            most = -1
            '''
            All datapoints should be 0 anyway. This just prevents a divide by 0 error
            '''
        else: #Absolutely completely a jork. I mean a joke. 
            error = 'Your spending level needs to be OVER 9000!!!'
        print(most)
        return render_template('trackSpending.html', error=error, results=monthdata, total=total, most=most)
    except conn.Error as e:
        print("Error reading data from purchase natural join ticket table", e)
        cursor.close()
        error = 'Invalid query: Please try again'
        return render_template('trackSpending.html', error=error)
       
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')
  
app.run(debug = True)

