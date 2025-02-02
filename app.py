from flask import Flask, request, jsonify, redirect, render_template, flash, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os 

app = Flask(__name__)
app = Flask(__name__, static_folder='static')

app.secret_key = '19082005'  # Required for flash messages

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rakh@1908'
app.config['MYSQL_DB'] = 'virtual_stylist'

mysql = MySQL(app)

# ------------------ Routes ------------------

# Home Page (Quiz Page)
@app.route('/letsgopage', methods=['GET', 'POST'])
def letsgopage():
    if 'loggedin' in session:
        return render_template('letsgopage.html', name=session['name'])
    return redirect(url_for('webpage'))

# Login Page
@app.route('/webpage', methods=['GET', 'POST'])
def webpage():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('letsgopage'))
        else:
            message = 'Invalid email or password!'
    return render_template('webpage.html', message=message)

# Registration Page
@app.route('/Accountcreate', methods=['GET', 'POST'])
def Accountcreate():
    message = ''
    if request.method == 'POST':
        # Debugging: Log the form data
        print("Form Data Received:", request.form)

        # Check for required form fields
        if 'name' in request.form and 'mobileno' in request.form and 'email' in request.form and 'password' in request.form and 'confirm_password' in request.form:
            userName = request.form['name']
            mobileno = request.form['mobileno']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            # Check if passwords match
            if password != confirm_password:
                message = 'Passwords do not match!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
                account = cursor.fetchone()

                if account:
                    message = 'Account already exists!'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    message = 'Invalid email address!'
                elif not userName or not password or not email or not mobileno:
                    message = 'Please fill out all fields!'
                else:
                    cursor.execute('INSERT INTO user (name, mobileno, email, password) VALUES (%s, %s, %s, %s)', (userName, mobileno, email, password))
                    mysql.connection.commit()
                    message = 'Account created successfully! Please log in.'
                    return redirect(url_for('webpage'))  # Redirect to login page
        else:
            message = 'Please fill in all the required fields.'
    
    return render_template('Accountcreate.html', message=message)

@app.route('/recommend-outfit',methods=['POST'])
def recommend_outfit():
    data = request.json
    gender = data.get('gender')
    body_type = data.get('body_type')
    occasion = data.get('occasion')

    # Construct folder path based on selections
    folder_path=f"static/images/{gender}/{body_type}/{occasion}"
    full_path = os.path.join(app.root_path, folder_path)
    print("Full folder path:",full_path)

    if not os.path.exists(full_path):
        print("Folder not found:{full_path}")
        return jsonify({"error":"folder not found"}),404

        # Generate URLs for all images in the folder
    try:  
        images = [
            url_for('static',filename=f"images/{gender}/{body_type}/{occasion}/{file}") # Convert file paths to URLs
            for file in os.listdir(full_path)
            if file.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
    except Exception as e:
        print("Error while listing the files:",e)
        return jsonify({"error":"Unable to list files"}),500

    print("Images:",images)
    return jsonify({"images": images})  # Handle missing folder gracefully

# Feedback Page
@app.route('/feedbackpage', methods=['GET', 'POST'])
def feedbackpage():
    if request.method == 'POST':
        rate = request.form.get('rate')
        message = request.form.get('message')

        # Validate form data
        if not rate or not message:
            flash('Please provide both a rating and a message.', 'error')
            return redirect(url_for('feedbackpage'))

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO feedback (rate, message) VALUES (%s, %s)",
            (rate, message)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedbackpage'))

    return render_template('feedbackpage.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('webpage'))

if __name__ == "__main__":
    app.run(debug=True)  
