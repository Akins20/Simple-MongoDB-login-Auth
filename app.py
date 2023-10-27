from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'anythingsecret'  # Change this to a secret key

# Define your MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['myDB']  # Replace with your database name
users_collection = db['users']

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = users_collection.find_one({"username": username})

    if user:
        error = "Username already exists."
        return render_template('signup.html', error=error)

    user_data = {
        "username": username,
        "email": email,
        "password": password,
    }

    users_collection.insert_one(user_data)
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session['username'] = user['username']  # Store the username in the session
            return redirect(url_for('welcome'))
        else:
            error = "Invalid username or password."
            return render_template('signin.html', error=error)
    return render_template('signin.html')

@app.route('/signout', methods=['POST'])
def signout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('signin'))


@app.route('/index')
def welcome():
    username = session.get('username')
    if username:
        return render_template('index.html', username=username)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
