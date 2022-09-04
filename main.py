from fileinput import filename
import os, mongo
from flask import Flask
from flask import render_template, session, request, redirect, abort, url_for
from werkzeug.utils import secure_filename
import html

db = mongo.MongoDB(connectionString=os.getenv('MONGODB_URL'), database='accounts', collection='users')

app = Flask(__name__, static_url_path='', static_folder='./static')
app.secret_key = os.getenv('SESSION_SECRET')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dashboard/")
def dashboard():
    """Render dashboard"""
    if session.get('email'):
        return render_template('dashboard.html', session=session)
    else:
        return redirect('/login')

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    '''Creating account with username and password'''
    if not session.get('email'):
        # Not logged in
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            # Create account
            email = request.form['email']
            password = request.form['password']
            name = request.form['name']
            if email in db:
                # ALready signed up
                return "Account already exists"
            else:
                # No account exists
                db[email] = {'password': password, 'name': name}
                session['email'] = email
                session['name'] = name
                return "Success"
    else:
        # Logged in
        return redirect('/dashboard')

@app.route("/login/", methods=['GET', 'POST'])
def login():    
    '''Will either login or not'''
    #if request.method
    if not session.get('email'):
        # Not logged in
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            if email in db:
                print("in db")
                if db[email]['password'] == password:
                    session['email'] = email
                    session['name'] = db[email]['name']
                    return 'Success'
                else:
                    return "Incorrect credentials"
            else:
                return "No account exists"
    else:
        return redirect('/dashboard')


def is_signed_in(email: str) -> bool:
    """Check if user is signed in"""

    #TODO
    #wait do we need this tho because by default they will already be signed in or logged in from the first part right
    #like if we call the earlier functions first than it's already guarenteed that they are logged or signed in

def get_streak(email: str) -> int:
    """Get streak from database"""
    if email in db:
        if 'streak' in db[email]:
            return db[email]['streak']
        else:
            db[email]['streak'] = 0
            return 0

@app.route("/api/log/", methods=['POST'])
def log_info():
    '''log()
    will count last day they logged and then increment if it was consecutive'''
    streak = get_streak(session.get('email')) #SAM IS THIS OK

    #check if implemented, if it is then add increment that is in db[email]['streak'] 
    #if amount of time 
    # TODO: Implement this
    # db[email]['streak']
    # request.form['name']
    pass

@app.route('/api/streak/', methods=['GET'])
def streak():
    '''streak()
    will tell you the streak'''
    pass

@app.route("/logout/")
def logout():
    '''Logout'''
    session.pop('email', None)
    return redirect('/')

@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    '''Creating account with username and password'''
    if not session.get('email'):
        # Not logged in
        return redirect('/login')
 
    else:
        # Logged in
        if request.method == 'GET':
            return render_template('upload_file.html')
        elif request.method == 'POST':
            f = request.files['file']
            file_ext = os.path.splitext(f.filename)[1]
            
            if 'seq_no' in session:
                seq_no = session['seq_no'] + 1
            else:
                seq_no = 1

            file_path = str(seq_no)+file_ext
            file_key = 'image'+str(seq_no)

            f.save(os.path.dirname(os.path.abspath(__file__))+"/static/upload/"+file_path)
            db[file_key] = {'name': file_path}

            session['seq_no'] = seq_no
            return render_template('upload_file.html')

@app.route("/sortgarbage/<image_id>", methods=['GET', 'POST'])
def sortgarbage(image_id):
    '''Creating account with username and password'''
    if not session.get('email'):
        # Not logged in
        return redirect('/login')
 
    else:
        # Logged in
        if request.method == 'GET':
            return render_template('sort_garbage.html', image_name=html.unescape(db['image'+image_id]["name"]))
        elif request.method == 'POST':
            #if request.args.get("submit") == 'Next':
            new_name = 'image'+str(int(image_id)+1)
            return render_template('sort_garbage.html', image_name=html.unescape(db[new_name]["name"]))


if __name__ == "__main__":
    app.run(debug=True)
    