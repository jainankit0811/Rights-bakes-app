# from cs50 import SQL
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

conn = sqlite3.connect('databases.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Add user data
users_data = [
    ('example_user', 'password123'),
    ('test_user', 'testpassword')
]

cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users_data)

# Commit changes and close the connection
conn.commit()
conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blocks")
def blocks():
    return render_template("blocks.html")


@app.route("/account")
def account():
    # Example data for the account page
    account_info = {
        "username": "example_user",
        "email": "user@example.com",
        "membership_status": "Active",
    }
    return render_template("account.html", **account_info)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided username and password match the database
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user_data = cursor.fetchone()

        if user_data:
            return redirect(url_for('account'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert the new user data into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            return redirect(url_for("account"))
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")


@app.route("/filter")
@app.route("/filter")
def filter():
    return render_template("filter.html")


if __name__ == "__main__":
    app.run()
