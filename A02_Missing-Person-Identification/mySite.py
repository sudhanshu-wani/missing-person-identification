# # import the necessary packages
# from flask import Flask, render_template, redirect, url_for, request,session,Response
# from werkzeug.utils import secure_filename
# import os
# import cv2
# from supportFile import *
# import pandas as pd
# import sqlite3
# from datetime import datetime

# app = Flask(__name__)

# app.secret_key = '1234'
# app.config["CACHE_TYPE"] = "null"
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# @app.route('/', methods=['GET', 'POST'])
# def landing():
# 	return redirect(url_for('home'))


# @app.route('/input', methods=['GET', 'POST'])
# def input():
	
# 	if request.method == 'POST':
# 		if request.form['sub']=='Submit':
# 			name = request.form['Name']
# 			email = request.form['Email']
# 			num = request.form['Contact']
# 			Mname = request.form['MName']
# 			age = request.form['Age']
# 			gender = request.form['Gender']
# 			date = request.form['Mdate']
# 			location = request.form['Mlocation']
# 			photo = request.files['Photo']
# 			savepath= r'dataset'
# 			photo.save(os.path.join(savepath,secure_filename(Mname)))
# 			password = request.form['password']

# 			now = datetime.now()
# 			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
# 			con = sqlite3.connect('mydatabase.db')
# 			cursorObj = con.cursor()
# 			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (name text,num text,email text,Mname text,date text,location text,age text,gender text, password text)")
# 			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?,?,?)",(name,num,email,Mname,date,location,age,gender, password))
# 			con.commit()

# 			return redirect(url_for('login'))

# 	return render_template('input.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	error = None
# 	# global video
# 	global email
# 	if request.method == 'POST':
# 		email = request.form['Email']
# 		# video = request.form['video']
# 		# if(video == '0'):
# 		# 	video = 0
			
# 		password = request.form['password']
# 		con = sqlite3.connect('mydatabase.db')
# 		cursorObj = con.cursor()
# 		cursorObj.execute(f"SELECT email from Users WHERE Email='{email}' AND password = '{password}';")
	
# 		if(cursorObj.fetchone()):
# 			return redirect(url_for('video'))
# 		else:
# 			error = "Invalid Credentials Please try again..!!!"
# 	return render_template('login.html',error=error)

# @app.route('/home', methods=['GET', 'POST'])
# def home():
# 	return render_template('home.html')

# @app.route('/info', methods=['GET', 'POST'])
# def info():
# 	return render_template('info.html')

# @app.route('/video', methods=['GET', 'POST'])
# def video():
# 	return render_template('video.html')

# @app.route('/video_stream')
# def video_stream():
# 	global video
 
# 	return Response(get_frame(video),mimetype='multipart/x-mixed-replace; boundary=frame')

# # No caching at all for API endpoints.
# @app.after_request
# def add_header(response):
# 	# response.cache_control.no_store = True
# 	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
# 	response.headers['Pragma'] = 'no-cache'
# 	response.headers['Expires'] = '-1'
# 	return response


# if __name__ == '__main__' and run:
# 	app.run(host='0.0.0.0', debug=True, threaded=True)


# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request, session, Response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import cv2
from supportFile import *
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
    return redirect(url_for('home'))

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        if request.form['sub'] == 'Submit':
            name = request.form['Name']
            email = request.form['Email']
            num = request.form['Contact']
            Mname = request.form['MName']
            age = request.form['Age']
            gender = request.form['Gender']
            date = request.form['Mdate']
            location = request.form['Mlocation']
            password = request.form['password']
            password_hash = generate_password_hash(password)  # Hash the password

            savepath = r'dataset'
            photo = request.files['Photo']
            photo.save(os.path.join(savepath, secure_filename(Mname+'.jpg')))

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")           
            con = sqlite3.connect('mydatabase.db')
            cursorObj = con.cursor()
            cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (name text,num text,email text,Mname text,date text,location text,age text,gender text, password_hash text)")
            cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?,?,?)", (name, num, email, Mname, date, location, age, gender, password_hash))
            con.commit()

            return redirect(url_for('login'))

    return render_template('input.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        con = sqlite3.connect('mydatabase.db')
        cursorObj = con.cursor()
        cursorObj.execute("SELECT email, password_hash FROM Users WHERE Email=?", (email,))
        user = cursorObj.fetchone()
        if user and check_password_hash(user[1], password):  # Compare hashed passwords
            return redirect(url_for('video'))
        else:
            error = "Invalid Credentials Please try again..!!!"
    return render_template('login.html', error=error)

# Other routes and functions...
@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('info.html')

@app.route('/video', methods=['GET', 'POST'])
def video():
	return render_template('video.html')

@app.route('/video_stream')
def video_stream():
	global video
 
	return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response
run = True

if __name__ == '__main__' and run:
	app.run(host='0.0.0.0', debug=True, threaded=True)
