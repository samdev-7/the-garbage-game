import os, mongo
from flask import Flask
from flask import render_template, session, request, redirect

db = mongo.MongoDB(os.getenv('MONGODB_URL'), 'accounts', 'users')

app = Flask(__name__, static_folder='./static')
app.secret_key = os.getenv('SESSION_KEY')

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    '''Creating account with username and password'''
    if not session.get('logged_in'):
        # Not logged in
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            # Create account
            email = request.form('email')
            password = request.form['password']
            if db[email]:
                # ALready signed up
                return "You are already signed up"
            else:
                # No account exists
                db[email] = {'password': password}
                return redirect('/dashboard')
    else:
        # Logged in
        return redirect('/dashboard')

@app.route("/login", methods=['GET', 'POST'])
def login():    
    '''Will either login or not'''
    #if request.method
    if not session.get('logged_in'):
        # Not logged in
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            # Check if username and password are correct
            if db[email]:
                if db[email]['password'] == password:
                    session['logged_in'] = True
                    return redirect('/dashboard')
                else:
                    return "Incorrect email or password"
            else:
                return "This email is not signed up"
    else:
        return redirect('/dashboard')

if __name__ == "__main__":
    app.run()
    