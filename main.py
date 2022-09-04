from fileinput import filename
import os, mongo
from flask import Flask
from flask import render_template, session, request, redirect, abort, url_for
from werkzeug.utils import secure_filename
import random
import json

db = mongo.MongoDB(connectionString=os.getenv('MONGODB_URL'), database='accounts', collection='users')
img_db = mongo.MongoDB(connectionString=os.getenv('MONGODB_URL'), database='images', collection='images')

app = Flask(__name__, static_url_path='', static_folder='./static')
app.secret_key = os.getenv('SESSION_SECRET')

@app.route("/")
def index():
    return render_template('index.html')

#@app.route("/dashboard/")
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
                db[email] = {'password': password, 'name': name, 'score': 0}
                session['email'] = email
                session['name'] = name
                return "Success"
    else:
        # Logged in
        return redirect('/sortgarbage')

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
                if db[email]['password'] == password:
                    session['email'] = email
                    session['name'] = db[email]['name']
                    return 'Success'
                else:
                    return "Incorrect credentials"
            else:
                return "No account exists"
    else:
        return redirect('/sortgarbage')


def is_signed_in() -> bool:
    """Check if user is signed in"""
    return session.get('email') != None


def get_streak(email: str) -> int:
    """Get streak from database"""
    if email in db:
        if 'streak' in db[email]:
            return db[email]['streak']
        else:
            db[email]['streak'] = 0
            return 0

#@app.route("/api/log/", methods=['POST'])
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

#@app.route('/api/streak/', methods=['GET'])
def streak():
    '''streak()
    will tell you the streak'''
    pass

@app.route("/logout/")
def logout():
    '''Logout'''
    session.pop('email', None)
    return redirect('/')

#@app.route("/upload/", methods=['GET', 'POST'])
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

            can_recyc = request.form["can_recyc"]

            db[file_key] = {'name': file_path, 'can_recyc': can_recyc}

            session['seq_no'] = seq_no
            message = "Your image "+f.filename+" has been successfully uploaded."
            return render_template('upload_file.html', message=message)

with open('./static/upload/image.json') as f:
   images = json.load(f)

@app.route("/sortgarbage/", methods=['GET', 'POST'])
def sortgarbage():
    '''Creating account with username and password'''
    if not session.get('email'):
        # Not logged in
        return redirect('/login')
 
    else:
        # Logged in
        if request.method == 'GET':
            email = session['email']
            image = random.choice(images)
            return render_template('sortgarbage.html', image_src=image['url'], img_id=image['id'], score=db[email]['score'])
        elif request.method == 'POST':
            email = session['email']
            can_recyc = request.form['can_recyc']

            if can_recyc == 'yes':
                can_recyc = True
            else:
                can_recyc = False

            img_id = request.form['img_id']
            
            for image in images:
                if image['id'] == int(img_id):
                    if image['recyclable'] == can_recyc:
                        # Correct
                        db._col.update_one({'_id': email}, {"$set": {'_id': email, 'value': { "password": db[email]['password'], "name": db[email]['name'], "score" : db[email]['score']+10 }}})
                        return "Correct"
                    else:
                        # Incorrect
                        db._col.update_one({'_id': email}, {"$set": {'_id': email, 'value': { "password": db[email]['password'], "name": db[email]['name'], "score" : db[email]['score']-10 }}})
                        return "Incorrect"
        
@app.route("/leaderboard/", methods=['GET'])
def leaderboards():
    '''leaderboards() -> str
    displays the leaderboards, top 10 or smth'''
    #sort score
    leaderList = sorted(db.values(), key=lambda x: x['score'], reverse=True)

    scores = []
    for place, account in enumerate(leaderList):
        scores.append({'place': place+1, 'name': account['name'], 'score': account['score']})


    return render_template('leaderboard.html', scores=scores)
    
if __name__ == "__main__":
    app.run(debug=True)