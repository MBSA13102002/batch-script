
from flask import Flask,render_template,request,g,url_for,redirect,make_response
import os
import json,time
from firebase import Firebase
config = {
    "apiKey": "AIzaSyDO2W0QCmFCo0a-PTsT7ficA_QLI5e_WHg",
    "authDomain": "chat-a7bab.firebaseapp.com",
    "databaseURL": "https://chat-a7bab-default-rtdb.firebaseio.com",
    "projectId": "chat-a7bab",
    "storageBucket": "chat-a7bab.appspot.com",
    "messagingSenderId": "550345253145",
    "appId": "1:550345253145:web:c6f493380c62bed2d02588",
    "measurementId": "G-R8DG3WGW88"
  };

firebase = Firebase(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = os.urandom(24)
with open('config.json', 'r') as c:                                                                
    params = json.load(c)["params"]
def handle_catch(caller, on_exception):
    try:
         return caller()
    except:
         return on_exception
@app.route("/",methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        uname = request.form.get("username")
        upass = request.form.get("password")
        try:
            user_ = auth.sign_in_with_email_and_password(uname ,upass)
            friends_list = db.child("Users").child(user_['localId']).child("friends").get()
            resp = make_response(render_template("friend_list.html",friends_list =friends_list,handle_catch = handle_catch ))
            # resp.set_cookie('framework', 'flask')
            resp.set_cookie('__user__', user_['localId'],max_age=60*60*24)
            resp.set_cookie('__email__', user_['email'],max_age=60*60*24)
            # session['user'] = user_['localId']
            # session['email'] = user_['email']
            # g.user  = session['user']

            return resp
       except Exception  as e:
            mes_code = json.loads(e.args[1])['error']['message']
            if(mes_code == "INVALID_PASSWORD"):
                res_code = 500
            elif(mes_code == "EMAIL_NOT_FOUND"):
                res_code = 502
            return render_template("index.html",res_code = res_code)
    
    if request.cookies.get('__user__')is not None and request.cookies.get('__email__') is not None:
        friends_list = db.child("Users").child(request.cookies.get('__user__')).child("friends").get()
        return render_template("friend_list.html",friends_list =friends_list,handle_catch = handle_catch )

    return render_template("index.html")
@app.route('/dashboard')
def dashboard():
    if request.cookies.get('__user__') != None and request.cookies.get('__email__') != None:
        # return render_template("dashboard_temp.html")
        friends_list = db.child("Users").child(request.cookies.get('__user__')).child("friends").get()
        return render_template("friend_list.html",friends_list =friends_list,handle_catch = handle_catch )
    return redirect(url_for('index'))

@app.route("/drop",methods=['GET','POST'])
def drop():
    if request.method=='POST':
        resp = make_response(redirect(url_for('index')))
        resp.delete_cookie('__user__')
        resp.delete_cookie('__email__')
        return resp
    return "go to sigin"

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            _user_ = auth.create_user_with_email_and_password(username ,password)
            auth.send_email_verification(_user_['idToken'])
            db.child("User_Emails").child(username.split("@")[0]).set({
                "UID":_user_['localId']
            })
            db.child("Users").child(_user_['localId']).set({
                "name":name,    
            })
            return render_template("success.html")
        except Exception as e:
            pass
            return render_template(url_for('index'))
    return render_template("signup.html")

@app.route('/passchange',methods = ['GET','POST'])
def passchange():
    if request.method == 'POST':
        email = request.form.get("pass_change_email")
        auth.send_password_reset_email(email)
        return render_template("passwordchange.html",val = "true")
    return render_template("passwordchange.html",val = "false")

@app.route('/addfriend',methods = ['GET','POST'])
def addfriend():
    if request.method=='POST':
        femail = request.form.get('friend_add_email').split("@")[0]
        all_emails = dict(db.child("User_Emails").get().val())
        all_emails_list  = list(all_emails.keys())
        try:
            user_friend_list = list(dict(db.child("Users").child(request.cookies.get('__user__')).child("friends").get().val()).keys())
            if femail in all_emails_list and femail not in user_friend_list:
                friends_name = db.child('Users').child(all_emails[femail]['UID']).child("name").get().val()
                db.child("Users").child(request.cookies.get('__user__')).child("friends").child(all_emails[femail]['UID']).update({
                    'name':friends_name
                })
                user_name = db.child('Users').child(request.cookies.get('__user__')).child("name").get().val()
                db.child("Users").child(all_emails[femail]['UID']).child("friends").child(request.cookies.get('__user__')).update({
                'name':user_name
                })
        except:

            if femail in all_emails_list:
                friends_name = db.child('Users').child(all_emails[femail]['UID']).child("name").get().val()
                db.child("Users").child(request.cookies.get('__user__')).child("friends").child(all_emails[femail]['UID']).update({
                    'name':friends_name
                })
                user_name = db.child('Users').child(request.cookies.get('__user__')).child("name").get().val()
                db.child("Users").child(all_emails[femail]['UID']).child("friends").child(request.cookies.get('__user__')).update({
                'name':user_name
                })
            
        return redirect(url_for('dashboard')) 
    return redirect(url_for('dashboard')) 

@app.route("/<string:friend_uid>/",methods = ['GET'])
def chat(friend_uid):
    if request.cookies.get('__user__') != None and request.cookies.get('__email__') != None:
        user_name = db.child('Users').child(request.cookies.get('__user__')).child("name").get().val()
        friends_name = db.child('Users').child(friend_uid).child("name").get().val()
        friends_list = db.child("Users").child(request.cookies.get('__user__')).child("friends").get()
        return render_template("message.html",user_uid = request.cookies.get('__user__'),friend_uid = friend_uid,user_name = user_name,friend_name =friends_name,friends_list =friends_list,handle_catch = handle_catch )
    return render_template("message.html")

@app.route('/forward',methods = ['GET','POST'])
def forward_mssg():
    if request.method == 'POST':
        all_mssg_str = request.form.get("all_forwarded_Messages")
        friend_to_be_forwarded = request.form.get("friend_to_be_forwarded")
        data = json.loads(all_mssg_str)
        for key,value in data.items():
            db.child('Users').child(friend_to_be_forwarded).child("friends").child(request.cookies.get('__user__')).child(request.cookies.get('__user__')).push({
                'chat':value['chat'],
                'type':value['type'],
                'name':value['name']

            })
            db.child('Users').child(request.cookies.get('__user__')).child("friends").child(friend_to_be_forwarded).child(friend_to_be_forwarded).push({
                'chat':value['chat'],
                'type':value['type'],
                'name':value['name']

            })
        # return render_template("painter.html")
        return redirect(url_for('chat',friend_uid = friend_to_be_forwarded))
# @app.before_request
# def before_request():
#     g.user = None
#     if 'user' in session:
#         g.user = session['user']

