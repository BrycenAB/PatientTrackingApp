# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'patient_tracker'
mysql = MySQL(app)


# check connection to database
@app.route('/test')
def test():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients")
    result = cursor.fetchall()
    return jsonify(result)


@app.route('/patients', methods=['POST'])
def create_patient():
    print("in create patient")
    fname = request.json['fname']
    lname = request.json['lname']
    gender = request.json['gender']
    dob = request.json['dob']
    address = request.json['address']
    phone_number = request.json['phone_number']
    email = request.json['email']
    medical_history = request.json['medical_history']

    # Insert the new patient record into the database
    try:
        print("in try")
        cursor = mysql.connection.cursor()
        query = "INSERT INTO patients (fname, lname, gender, dob, address, phone, email, medicalhistory) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (fname, lname, gender, dob, address, phone_number, email, medical_history)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'New patient record created successfully!'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to create new patient record.'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        medical_history = request.form['medical_history']

        # Prepare data for API request
        patient_data = {
            'fname': fname,
            'lname': lname,
            'gender': gender,
            'dob': dob,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'medical_history': medical_history
        }

        # Make a request to the Flask API to store patient information
        api_url = 'http://localhost:5000/patients'
        response = requests.post(api_url, json=patient_data)

        if response.status_code == 200:
            return redirect(url_for('registration_success'))
        else:
            return redirect(url_for('registration_failure'))

    return render_template('PatientRegistration.html')


@app.route('/registration-success')
def registration_success():
    return render_template('RegSuccess.html')


@app.route('/registration-failure')
def registration_failure():
    return render_template('RegFailure.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
