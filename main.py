from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)
USERNAME = 'admin'
PASSWORD = 'password123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            # Redirect to dashboard if login credentials are correct
            return redirect('/dashboard')
        else:
            # Show error message if login credentials are incorrect
            return render_template('login.html', error='Invalid username or password')
    # Render the login page if it's a GET request or if login credentials are incorrect
    return render_template('login.html', error=None)

# Database configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'bookinventory'

mysql = MySQL(app)

def get_books():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], database=app.config['MYSQL_DB'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return books

@app.route('/dashboard')
def dashboard():
    books = get_books()
    return render_template('dashboard.html', books=books)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        isbn = request.form.get('isbn')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        cur.execute("INSERT INTO book (title, author, genre, isbn, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)", (title, author, genre, isbn, price, quantity))
        mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')  # Redirect to dashboard page
    return render_template('add.html')

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        isbn = request.form.get('isbn')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        cur.execute("UPDATE book SET title = %s, author = %s, genre = %s, isbn = %s, price = %s, quantity = %s WHERE id = %s", (title, author, genre, isbn, price, quantity, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/dashboard')  # Redirect to dashboard page
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM book WHERE id = %s", (id,))
    book = cur.fetchone()
    cur.close()
    return render_template('edit.html', book=book)

@app.route("/delete/<int:id>", methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM book WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/dashboard')  # Redirect to dashboard page

if __name__ == '__main__':
    app.run(debug=True)
