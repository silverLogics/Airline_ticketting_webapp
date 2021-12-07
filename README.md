# Airline_ticketting_webapp
All files and what they are used for:
mainapp.py
This is the main file that controls the whole webapp. It initializes the Flaskapp and the webpage on local host. It also contains all of the staff and customer functions that renders the html pages and queries the db to send data to those html pages. 
addAirplane.html
This page is used by staff to insert a new airplane (through a form) and view all airplanes operated by the staffs airline
addAirport.tml
This page is used by staff to insert a new airport into the airport database (through a form)
createFlight.thml
This page is a little misleading (it actually contains all of the info on managing flights.) It holds the forms for creating a flight, changing the status, and viewing the ratings of a specific flight. It also displays the flights occuring in the next 30 days for that staffs airline
customerhome.html
error.html
login.html
logsuccess.html
purchaseTicket.html
registerCust.html
This page holds the form so the customer can fill in their info to make an account.
registerStaff.html
This page holds the form so the staff can fill in their info to make an account.
search.html
**??**
staffhome.html
This page contains all of the links to the mainapp.py functions to query the db and render pages to fufill all of the staff usecases (manageflights, add airport and airplanes, view revenue...)
startpage.html
This page contains all of the links to mainapp.py to view flights or to regester or login as a customer or staff
topDestinations.html
This page displays the top destinations in the last 3 months and last year for the staff's(who is logged in) airline
viewCustomers.html
This page displays the top customer in the past year for the staffs'(who is logged in) airline
viewFlights.html
viewReports.html
This page displays a bar chart showing ticket tickets sales over the years for each month. It also has a form to input dates and see the total number of tickets sold between the two dates
viewReportswDate.html
This page is where view reports is redirected to if the date form is filledout. It displays the total number of tickets sold between those two dates
viewRevenue.html
This page displays the revenue from the past year and past 3 months for the staff's(who is logged in) airlien
viewflightRatings:
This page is where the view rating form redirects the staff. It displays all of the ratings and comments as well as average ratings for the flight that was inputed. 
viewRatings.html:
**delete this is extra**







Use cases and how they were completed:

1. View Public Info: All users, whether logged in or not, can
a. Search for future flights based on source city/airport name, destination city/airport name,
departure date for one way (departure and return dates for round trip).
b. Will be able to see the flights status based on airline name, flight number, arrival/departure
date.
2. Register: 2 types of user registrations (Customer, and Airline Staff) option via forms.
This usecase was fullfilled in the the mainapp and registerCust.html/registerStaff.html
When the link to register a customer is clicked. mainapp.py renders registerCust.html. This page contains a form with all of the necissary info for inserting a customer in the DB. The form once submited then refers to the function AuthCustomer which takes in the inputed values, checks if the email entered is already being used by a customer through this query: 'SELECT * FROM customer WHERE email = %s'.
If it hasn't been used it then submits this query to insert the data as a new customer
ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country,DOB))
conn.commit()
Click on register staff does a similar thing of rendering registerStaff.html. This page also has a form that goes to mainapp and AuthStaff.
Auth staff similar checks if the username is already in use:
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()
 And then similarly inserts a new staff if this check passes:
             ins = 'INSERT INTO Airline_staff VALUES(%s, %s, md5(%s), %s, %s, %s)'
            cursor.execute(ins, (username, airline_name, password, f_name, l_name, DOB))
            conn.commit()
            cursor.close()
 Both return to the start page once these tasks are successfully completed or stays on register if it fails.
4. Login: 2 types of user login (Customer, and Airline Staff). Users enters their username (email address
will be used as username), x, and password, y, via forms on login page. This data is sent as POST
parameters to the login-authentication component, which checks whether there is a tuple in the
corresponding user’s table with username=x and the password = md5(y).
a. If so, login is successful. A session is initiated with the member’s username stored as a session
variable. Optionally, you can store other session variables. Control is redirected to a component that
displays the user’s home page.
b. If not, login is unsuccessful. A message is displayed indicating this to the user.
Note: In real applications, members’ passwords are stored as md5/other hashes, not as plain text. This
keeps the passwords more secure, in case someone is able to break into the system and see the
passwords. You can perform the hash using MySQL’s md5 function or a library provided with your host
language.) Once a user has logged in, reservation system should display his/her home page. Also, after
other actions or sequences of related actions, are executed, control will return to component that
displays the home page. The home page should display
c. Error message if the previous action was not successful,
d. Some mechanism for the user to choose the use case he/she wants to execute. You may
choose to provide links to other URLS that will present the interfaces for other use cases, or you
may include those interfaces directly on the home page.
e. Any other information you’d like to include. For example, you might want to show customer's
future flights information on the customer's home page, or you may prefer to just show them
when he/she does some of the following use cases.
Customer use cases:
After logging in successfully a user(customer) may do any of the following use cases:
4. View My flights: Provide various ways for the user to see flights information which he/she purchased.
The default should be showing for the future flights. Optionally you may include a way for the user to
specify a range of dates, specify destination and/or source airport name or city name etc.
5. Search for flights: Search for future flights (one way or round trip) based on source city/airport name,
destination city/airport name, dates (departure or return).
6. Purchase tickets: Customer chooses a flight and purchase ticket for this flight, providing all the
needed data, via forms. You may find it easier to implement this along with a use case to search for
flights.
6. Give Ratings and Comment on previous flights: Customer will be able to rate and comment on their
previous flights (for which he/she purchased tickets and already took that flight) for the airline they
logged in.
7.Track My Spending: Default view will be total amount of money spent in the past year and a bar
chart/table showing month wise money spent for last 6 months. He/she will also have option to specify
a range of dates to view total amount of money spent within that range and a bar chart/table showing
monthwise money spent within that range.
8.Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
Airline Staff use cases:
After logging in successfully an airline staff may do any of the following use cases:
4. View flights: Defaults will be showing all the future flights operated by the airline he/she works for
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see
all the customers of a particular flight.
**need to fix this page**

5. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The
application should prevent unauthorized users from doing this action. Defaults will be showing all the
future flights operated by the airline he/she works for the next 30 days.
This use case is also successfully done on the manageflights page. On the page there is a form section at the top with all of the necissary information for inserting a new flight. When submit is clicked it sends a request to the function createFlightAuth.
This starts off by grabbing the form info then inserting a new flight:
 query = 'insert into flight values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (flightnum, departtime, airline_operator, owner_name, arrivetime, departnum, arrivenum, airplane_num, base_price, status))
        conn.commit()
 It then sees the most recent t_id:
 query = 'select max(t_id) from Ticket'
 and finds the number of seats on the plane
  query = 'select * from airplane where airplane_id=%s'
        cursor.execute(query, airplane_num)
        data = cursor.fetchall()
        numseats=data[0]['num_seats']
  And then uses the number of seats and the tid to inser the correct ammount of tickets:
  for i in range(1, numseats):
            query = 'insert into Ticket values (%s, %s, %s, %s, %s)'
            cursor.execute(query, (lasttid+i,flightnum,departtime,airline_operator,None))
            conn.commit()

6. Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via
forms.
This is also done on manageflights page and is also done through a form. This form just has the two options for flight status and one input for which flight it is. When changestatus function is ran it makes sure the correct user is logged in and then updates the flight status with this query:
query = 'update flight set status=%s where flight_num=%s and airline_operator = %s'
cursor.execute(query, (status, flightnum, airline))

7. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms.
The application should prevent unauthorized users from doing this action. In the confirmation page,
she/he will be able to see all the airplanes owned by the airline he/she works for. **need to do**
This is done on the addairplane.html page which includes a form for the type of airplane that it is.  When the request is submitted it first checks to make sure that the user is the correct type of staff.
It then adds the airplane with this query.
        cursor = conn.cursor()
        query = 'insert into airplane values (%s, %s, %s)'
        cursor.execute(query, (id, owner_name, seats))
        conn.commit()
 And queries all of the airplanes the staff has 
 **need to do**
 This is then rendered in conformation.html

8. Add new airport in the system: He or she adds a new airport, providing all the needed data, via
forms. The application should prevent unauthorized users from doing this action.
This is done the exact same way as usecase 7.
This is done on the addairport.html page which includes a form for the type of airport that it is.  When the request is submitted it first checks to make sure that the user is the correct type of staff.
It then adds the airport with this query.
 cursor = conn.cursor()
        query = 'insert into airport values (%s, %s, %s)'
        cursor.execute(query, (id, name, city))
        conn.commit()
9. View flight ratings: Airline Staff will be able to see each flight’s average ratings and all the comments
and ratings of that flight given by the customers.
This is done in the manageflight page which has a form for viewing a flights ratings that takes in the flight number.
The viewRatings function in mainapp.py then takes this info and executes this query
    flightnum = request.form['fli']
    query = 'select * from review where flight_num=%s'
    cursor.execute(query, (flightnum))
To get all of the ratings and then uses a for loop to go through all of them add them up and average them.
The ratings comments and avg ratings are then rendered on viewRatings.html by looping through the data generated in the viewRatings functon

11. View frequent customers: Airline Staff will also be able to see the most frequent customer within
the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has
taken only on that particular airline.**need to do this last part
This page first grabs the customers and the ammount of tickets they got through this query
query = 'select email, count(t_id) as tickets from purchase natural join Ticket where airline_operator= %s and purchasedate_time >= date_sub(curdate(), interval 1 year) group by email having tickets >= all (select count(t_id) from purchase natural join ticket  where airline_operator = %s and purchasedate_time >= date_sub(curdate(), interval 1 year) GROUP by email)'
    cursor.execute(query, (airline, airline))
It then buble them using this forloop based on how many tickets they bought
n=len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j]['tickets'] < data[j+1]['tickets']:
                data[j],data[j+1]= data[j+1],data[j]
It then passes in data[0] as the most frequent customer to viewCustomers.html and displays its data and flights **need to do**


12. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month
wise tickets sold in a bar chart/table.
This was done on the view reports page which again makes sure that the user is staff.
It then goes month by month with a forloop that executes queries based on the month
for i in range(0, 12):
        query = 'select count(t_id) as num_tic from purchase natural join ticket where year(purchasedate_time) = year(curdate() - interval ' + str(i) + ' month) and month(purchasedate_time) = month(curdate() - interval ' + str(i) + ' month) and airline_operator=%s'
        cursor.execute(query, (airline))
        data = cursor.fetchall()
        salemonth = ((currentmonth - (i+1)) % 12) + 1
        monthtickets.append([data[0]['num_tic'], salemonth])
The monthly ticket data is then passed into viewReports.html to be desplayed by a premade chart:
**reference the link to the premade chart**
There is also a form that takes in a range of dates which is sent to the function viewreportsdates.
This takes those dates and finds the total ammount of tickets sold between those dates through this query:
query = 'select count(t_id) as num_tic from purchase natural join ticket where airline_operator=%s and purchasedate_time between %s and %s'
    cursor.execute(query, (airline, start, end))
This is once more rendered on 'viewReportswDate.html' displaying the dates and number of tickets

13. View Earned Revenue: Show total amount of revenue earned from ticket sales in the last month and
last year.
These two types of revenues (three month and a year) are found in the revenue function.
The user is first authenticated and then these queries are executed:
airline = getStaffAirline()
    cursor = conn.cursor()
    query = 'select sum(sold_price) as yearrev from purchase natural join ticket where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 year) and curdate()'
    cursor.execute(query, (airline))
    yearrev = cursor.fetchall()
    query = 'select sum(sold_price) as monthrev from purchase natural join ticket where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 month) and curdate()'
    cursor.execute(query, (airline))
    monthrev = cursor.fetchall()
These two revenues are then passed into viewRevenue.html and displayed

14. View Top destinations: Find the top 3 most popular destinations for last 3 months and last year
(based on tickets already sold).
This is done in the top destination function.
This function first makes sure that the user is a staff.
It then finds the number of tickets sold for each destination between the the two time frames:
query = 'select arrive_airport_id, count(t_id) from ticket NATURAL JOIN flight NATURAL JOIN purchase where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 3 month) and curdate() group by arrive_airport_id'
    cursor.execute(query, (airline))
    monthdata=cursor.fetchall()
    #sort and get top 3
    query = 'select arrive_airport_id, count(t_id) from ticket NATURAL JOIN flight NATURAL JOIN purchase where airline_operator=%s and purchasedate_time between DATE_SUB(curdate(), interval 1 year) and curdate() group by arrive_airport_id'
    cursor.execute(query, (airline))
    yeardata=cursor.fetchall()
    query= 'select * from Airport'
It then sorts this data to find the most popular destination:
    for i in range(n):
        for j in range(0, n-i-1):
            if monthdata[j]['count(t_id)'] < monthdata[j+1]['count(t_id)']:
                monthdata[j],monthdata[j+1]= monthdata[j+1],monthdata[j]
    r=len(yeardata)
    for i in range(n):
        for j in range(0, r-i-1):
            if yeardata[j]['count(t_id)'] < yeardata[j+1]['count(t_id)']:
                yeardata[j],yeardata[j+1]= yeardata[j+1],yeardata[j]
  And then it picks out all of there actual names so the top three of both can be displayed
      for i in monthdata:
        for j in Airport_data:
            if j['airport_id']==i['arrive_airport_id']:
                i['city']=j['city']
    for i in yeardata:
        for j in Airport_data:
            if j['airport_id']==i['arrive_airport_id']:
                i['city']=j['city']
   These top three names are then displayed in 
  topDestinations.html
15. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
The login function occurs on many of the pages and is very simple. It just pops the session and redirects to home.
    session.pop('username')
    return redirect('/login')

Teammember responsibilities (who did what)
Part 1 and Part 2 were split evenly among the two of us so that we both did everything.
Elijah:
I did some of the initial work on the log in and registration for the customer and staff. 
I also setup some of the initial structure of the customer home page
From there I made all of the staff pages in order to fullfill the usecases of the staff
  **Daniel helped me with the error handling for someo of these pages**

Daniel:

