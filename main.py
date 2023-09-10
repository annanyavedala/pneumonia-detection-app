from math import expm1
import pandas as pd
from flask import Flask, jsonify, request, render_template,url_for, flash, redirect,session,g
from flask_mysqldb import MySQL
from flask_login import login_user, current_user, logout_user, login_required,UserMixin
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import cv2
app = Flask(__name__, template_folder='templates')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model = keras.models.load_model("./modelpneumonia.h5")
import MySQLdb.cursors
from forms import RegistrationForm,LoginForm,UploadImage,Permission
from flask_login import LoginManager
import os
from flask_mail import Mail, Message



# database setup
app.config['SECRET_KEY'] = ''
  
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lungdisease'
app.config['UPLOAD_PATH'] = './uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
mysql = MySQL(app)

#mail configuration
app.config['MAIL_SERVER']=''
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(userid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE userid = % s ', (userid))
    account = cursor.fetchone()
    
    return account
class User(UserMixin):
    def __init__(self, account):
        self.account = account

    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details
    def get_id(self):
        object_id = self.account.get('userid')
        return str(object_id)



@app.before_request
def before_request():

    g.username = None
    if 'username' in session:
        g.username = session['username']
    
    g.email=None
    if 'email' in session:
        g.email=session['email']
    #return g.username


@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            phone_number = form.phone_number.data
            Age = form.Age.data
            Height = form.Height.data
            Weight = form.Weight.data
            password = form.password.data
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('insert into user (username,email,password1,age,height,weight,phone_number)values(%s,%s,%s,%s,%s,%s,%s)',(username,email,password,Age,Height,Weight,phone_number))
            mysql.connection.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
             flash(f'SOME SHIT HAPPENEd', 'success')
        
    return render_template('register.html', form=form)

@app.route("/login",methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
 
        email = form.email.data
        password = form.password.data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password1 = % s', (email, password))
        account = cursor.fetchone()
        session.pop('username',None)
        session.pop('email',None)
        if account:
           # 
            session['loggedin'] = True
            session['id']=account['userid']
            session['username']=account['username']
            session['email'] = account['email']
          #  loginuser = User(account)
           # login_user(loginuser, remember=form.remember.data)
            flash(f'You have been logged in! welcome {form.email.data}', 'success')
          #  next_page = request.args.get('next')
            #return redirect(next_page) if next_page else 
            # redirect(url_for('home'))
           
            return redirect(url_for('home'))
            
        else:
          flash(f'incorect credentials','error')
    return render_template('login.html',form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))
    


@app.route("/",methods = ['GET', 'POST'])

def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM hospital ')
    account1 = cursor.fetchall()
   # ADDING IMAGE
   #def upload()
    m=request.args.get("email")
   # return render_template("index.html",form_data=form)
    image_file = url_for('static', filename='profile_pics/' )
    form = UploadImage()
    form1=Permission()
    email_id=g.email
    patient=g.username
    if form1.validate_on_submit():
        if form1.share.data==True:
            msg = Message(
                    'Treatment required',
                    sender =email_id,
                    recipients = ['']
                )
            msg.body = 'Patient name:'+patient+'Disease: Pneumonia'
            mail.send(msg)
            return render_template('index.html', title='Account',
                            image_file=image_file, form_data=form,data=account1,form1=form1)


    if request.method =='POST':
        file = request.files['picture']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_PATH'],filename))
        img_dims = 150
        test_data=[]
        img = plt.imread(file)
        img = cv2.resize(img, (img_dims, img_dims))
        img = np.dstack([img, img, img])
        img = img.astype('float32') / 255
        test_data.append(img)
        test_data = np.array(test_data)
        preds = model.predict(test_data)
        print('helloo')
        return render_template('index.html', prediction=preds, form1=form1, form_data= form, image_file=image_file, title='Account',data=account1)

    return render_template('index.html', title='Account',
                           image_file=image_file, form_data=form,data=account1,form1=form1)

@app.route("/account")

def account():
    if g.username:
       return render_template('account.html')
    return render_template('index.html',)
 





