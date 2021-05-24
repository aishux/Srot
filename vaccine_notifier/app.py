from flask import Flask, jsonify, request, render_template,session, redirect, flash
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import os
import datetime
import json
from threading import Thread
import time
from email.message import EmailMessage
import smtplib

####### PLEASE FILL THIS ############

EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''

app = Flask(__name__)
scheduler = APScheduler()

app.secret_key = "d1aba190fe0b7742b3589f7d636fad42"

# Locating our base directory

basedir = os.path.abspath(os.path.dirname(__file__))

# Connecting the Database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Initialize the database

db = SQLAlchemy(app)

# Create a model

class RequestedPincodes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    pincode = db.Column(db.String(6))
    email = db.Column(db.String(300))
    receive_alert = db.Column(db.Boolean,server_default='t',default=True)
    age_group = db.Column(db.String(100))

    def __init__(self,pincode,email,age_group):
        self.pincode = pincode
        self.email = email
        self.age_group = age_group

send_mail = []
available_pincodes = {}
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}


def sendMail():
    global msg,send_mail
    
    while True:
        m = 0
        while m < len(send_mail):
            curr = send_mail[m]
            if curr[0].receive_alert == False:
                send_mail.pop(0)
            else:
                m += 1
        print("Send Mail length",len(send_mail))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                while len(send_mail) > 0:
                    current_element = send_mail.pop(0)
                    print(current_element[0].id,len(send_mail))
                    print("sending mail to...",current_element[0].email)

                    msg = EmailMessage()
                    msg['Subject'] = f'Vaccine Availability alert for pincode {current_element[1]["pincode"]}'
                    msg['From'] = "Srot"
                    msg['To'] = current_element[0].email

                    msg.set_content(f'''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <meta http-equiv="X-UA-Compatible" content="ie=edge">
                            <title>Vaccine Alert</title>
                        </head>
                        <body>
                            <div>
                            <h2>INFORMATION ABOUT VACCINE AND THE CENTER</h2>
                            <h3>Pincode: {current_element[1]["pincode"]}</h3>
                            <h3>Name: {current_element[1]["name"]}</h3>
                            <h3>Address: {current_element[1]["address"]}</h3>
                            <h3>Open Time: {current_element[1]["from"]}-{current_element[1]["to"]}</h3>
                            <h3>Fee Type: {current_element[1]["fee_type"]}</h3>
                            <h3>Date Available On: {current_element[2]["date"]}</h3>
                            <h3>Total Capacity Available: {current_element[2]["available_capacity"]}</h3>
                            <h3>Dose 1 Capacity Available: {current_element[2]["available_capacity_dose1"]}</h3>
                            <h3>Dose 2 Capacity Available: {current_element[2]["available_capacity_dose2"]}</h3>
                            <h3>Age Limit: {current_element[2]["min_age_limit"]}</h3>
                            <h3>Vaccine Type: {current_element[2]["vaccine"]}</h3>
                            <h3>Slots Available: {current_element[2]["slots"]}</h3>
                            *** TO KEEP RECEIVING FURTHER ALERTS CLICK THE BELOW BUTTON ***<br><br>
                            <a href="http://127.0.0.1:5000/renewservice/{current_element[0].email}">
                            <button style="color: green;border: double;width: 164px;padding: 10px;font-weight: 700;">Keep Receving Alerts</button>
                            </a>
                            </div>
                            <span style="color: #FFF; display: none; font-size: 8px;"><%= rand(36**20).to_s(36) %></span>
                        </body>
                        </html>''',subtype="html")
                    
                    smtp.send_message(msg)

                    x = RequestedPincodes.query.filter_by(id = current_element[0].id)[0]
                    x.receive_alert = False
                    db.session.commit()
                    time.sleep(10)
        except Exception:
            pass
        time.sleep(60)


def scheduleTask():
    global available_pincodes
    
    all_data = RequestedPincodes.query.filter_by(receive_alert=True)
    current_date = datetime.datetime.now()

    for i in all_data:
        try:

            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={i.pincode}&date={current_date.day}-{current_date.month}-{current_date.year}"
            
            response = requests.request("GET", url, headers=headers, data={})
            centers = json.loads(response.text).get("centers")
            
            if centers != []:
                for center in centers:
                    session_list = center.get("sessions")

                    if session_list != []:
                        for session in session_list:
                            if session.get("available_capacity") > 0 and session.get("min_age_limit") == int(i.age_group):
                                if i.pincode not in available_pincodes:
                                    available_pincodes[i.pincode] = {i.age_group:[center,session]}
                                else:
                                    available_pincodes[i.pincode][i.age_group] = [center,session]

                                if [i,center,session] not in send_mail and i.receive_alert == True:
                                    send_mail.append([i,center,session])
            else:
                print("No center")

            time.sleep(2)
        except Exception:
            continue
    available_pincodes = {}
    print("current lenght",len(send_mail))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add",methods=["POST"])
def addPinCode():

    email = request.form.get("email")
    pincode = request.form.get("pincode")
    age_group = request.form.get("age_group")

    try:
        new_pin = RequestedPincodes(pincode=pincode,email=email,age_group=age_group)

        db.session.add(new_pin)

        db.session.commit()

        print("saved successfully!")

    except Exception as e:
        flash("There was some error", 'error')
        print(e)
    flash('Thank you! You will be notified!', 'success')
    return redirect("/")

@app.route("/renewservice/<email>")
def renewService(email):
    x = RequestedPincodes.query.filter_by(email = email)
    for i in x:
        try:
            i.receive_alert = True
        except Exception:
            continue
    db.session.commit()
    return render_template("RenewSuccess.html")

# Run the Server
if __name__ == "__main__":
    mail_thread = Thread(target=sendMail).start()
    scheduleTask()
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval",minutes=2)
    scheduler.start()
    app.run(debug=False)

