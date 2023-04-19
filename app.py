from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import flash

app = Flask(__name__)

app.secret_key = 'aadyaditi'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'monster_dairy'

mysql = MySQL(app)

@app.route('/')
@app.route('/index', methods =['GET', 'POST'])
def index():
	msg = ''
	return render_template('index.html', msg = msg)

@app.route('/customer', methods =['GET', 'POST'])
def customer():
	msg = ''
	return render_template('customer.html', msg = msg)

@app.route('/adminindex', methods =['GET', 'POST'])
def adminindex():
	msg = ''
	return render_template('adminindex.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['CustomerID']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('customer.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/admin', methods =['GET', 'POST'])
def admin():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['adminin'] = True
			session['aid'] = account['AdminID']
			session['username'] = account['username']
			msg = 'Admin Logged in successfully !'
			return render_template('adminindex.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('admin.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/adminlogout')
def adminlogout():
    session.pop('adminin', None)
    session.pop('aid', None)
    session.pop('username', None)
    return redirect(url_for('admin'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'postalcode' in request.form and 'accountnum' in request.form and 'age' in request.form and 'state' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		accountnum = request.form['accountnum']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		age = request.form['age']
		postalcode = request.form['postalcode']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE username = %s', (username,))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			addresslist = address.split()
			apt_num = addresslist[0]
			street_name = addresslist[1]
			street_number = addresslist[2]
			cursor.execute('INSERT INTO customer VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, accountnum, age, street_number, street_name, apt_num, city, state, postalcode, email, password))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route("/shop", methods=['GET', 'POST'])
def shop():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM item WHERE ItemID >= 1 and ItemID <= 30')
        account = cursor.fetchall()
        if request.method == 'POST':
            item_id = request.form['item_id']
            item_price = request.form['item_price']
            try:
                cursor.execute('INSERT INTO cart_item (CustomerID, CartID, ItemID, TotalQuantity, Price) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE TotalQuantity = TotalQuantity + %s, Price = Price + %s', (session['id'], session['id'], item_id, 1, item_price, 1, item_price))
                mysql.connection.commit()
                flash('Item added to cart successfully', 'success')
                return redirect(url_for('cart'))
            except MySQLdb.OperationalError as error:
                flash(str(error), 'error')
        return render_template("shop.html", account = account)
    return redirect(url_for('login'))

@app.route("/cart")
def cart():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT SUM(TotalQuantity), SUM(price) FROM cart_item WHERE customerID = % s', (session['id'], ))
		account = cursor.fetchone()
		return render_template("cart.html", account = account)
	return redirect(url_for('login'))

@app.route("/profile")
def profile():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT SUM(TotalQuantity), SUM(price) FROM cart_item WHERE customerID = % s', (session['id'], ))
		# account = cursor.fetchone()
		return render_template("profile.html")
	return redirect(url_for('login'))

@app.route("/sales")
def sales():
	if 'adminin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""SELECT BranchID, 
							SUM(DailySales) AS TotalDailySales,
							SUM(MonthlySales) AS TotalMonthlySales,
							SUM(QuaterlySales) AS TotalQuarterlySales,
							SUM(AnnualSales) AS TotalAnnualSales,
							SUM(TotalSales) AS TotalSales
							FROM sales
							GROUP BY BranchID WITH ROLLUP;""")
		account = cursor.fetchall()
		return render_template("sales.html", account = account)
	return redirect(url_for('admin'))

@app.route("/products")
def products():
	if 'adminin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""SELECT 
						ItemID, 
						SUM(CASE WHEN YEAR(ManufacturingDate) = 2021 THEN QuantityLeft ELSE 0 END) AS QuantityLeft_2021,
						SUM(CASE WHEN YEAR(ManufacturingDate) = 2022 THEN QuantityLeft ELSE 0 END) AS QuantityLeft_2022,
						SUM(CASE WHEN YEAR(ManufacturingDate) = 2023 THEN QuantityLeft ELSE 0 END) AS QuantityLeft_2023,
						AVG(Price) AS AvgPrice 
						FROM 
							item 
						GROUP BY 
							ItemID;""")
		account = cursor.fetchall()
		return render_template("products.html", account = account)
	return redirect(url_for('admin'))

@app.route("/inventory")
def inventory():
	if 'adminin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""SELECT 
							warehouse.State AS State,
							farm.City AS City,
							admin.username AS AdminUserName,
							SUM(distributor.QuantitySupplied) AS TotalQuantitySupplied
						FROM 
							distributor 
							JOIN warehouse ON distributor.WarehouseID = warehouse.WarehouseID
							JOIN farm ON distributor.FarmID = farm.FarmID
							JOIN admin ON distributor.AdminID = admin.AdminID
						GROUP BY 
							warehouse.State, 
							farm.City, 
							admin.username WITH ROLLUP;""")
		account = cursor.fetchall()
		return render_template("inventory.html", account = account)
	return redirect(url_for('admin'))

@app.route('/orders')
def orders():
	if 'adminin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""SELECT 
							customer_order.CustomerID AS CustomerID, 
							YEAR(customer_order.dateOfOrder) AS Year, 
							SUM(cart_item.TotalQuantity) AS TotalQuantity,
							AVG(cart_item.Price) AS AvgPrice,
							SUM(cart_item.TotalQuantity * cart_item.Price) AS TotalRevenue
						FROM 
							customer_order 
							JOIN cart_item ON customer_order.CustomerID = cart_item.CustomerID AND customer_order.CartID = cart_item.CartID
						WHERE 
							customer_order.dateOfOrder >= '2000-01-01' AND customer_order.dateOfOrder < '2023-01-01' -- slice by date range
						GROUP BY
							customer_order.CustomerID, 
							YEAR(customer_order.dateOfOrder);""")
		account = cursor.fetchall()
		return render_template("orders.html", account = account)
	return redirect(url_for('admin'))

@app.route("/staff")
def staff():
	if 'adminin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("""SELECT 
							branch.State AS State, 
							branch.City AS City, 
							SUM(branch.NumofEmployees) AS TotalEmployees, 
							SUM(sales.TotalSales) AS TotalSales 
						FROM 
							branch 
							JOIN sales ON branch.BranchID = sales.BranchID 
						GROUP BY 
							branch.State, 
							branch.City 
						WITH ROLLUP;
						""")
		account = cursor.fetchall()
		return render_template("staff.html", account = account)
	return redirect(url_for('admin'))

if __name__ == "__main__":
	app.debug = True
	app.run(host ="localhost", port = int("5002"))

app.static_folder = 'static'
