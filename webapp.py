from app import *
from flask import Flask, render_template, request, redirect

from datetime import datetime
import pymongo 
client=pymongo.MongoClient("mongodb+srv://saksham:qk70nd97a@cluster1.vucvhcs.mongodb.net/?retryWrites=true&w=majority")
db=client["healthAI_logins"]  #It is the DATABASE
collection=db['data']   #It is My COLLECTON

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_test_db.sqlite3"
# db.init_app(app)
app.app_context().push()


@app.route("/", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form.get("name")
        mobile = request.form.get("mbno")
        email = request.form.get("email")
        date = request.form.get("date")
        time = request.form.get("time")
        slot_time = datetime.strptime(date + ":" + time, '%Y-%m-%d:%H:%M')
        # print(name, mobile, email, date)
        # new_slot = Appointment(name=name, email=email,phone=mobile, date=slot_time)
        # db.session.add(new_slot)
        # db.session.commit()
        new_slot={"name":name,"email":email,"phone":mobile,"date":slot_time}
        existing_slot=collection.find_one({"date":slot_time})
        if existing_slot is None:
            collection.insert_one(new_slot)
        else:
            print("Slot already taken")
        return redirect("/")
    return render_template('index.html')


@app.route("/ask", methods=["GET", "POST"])
def asking():
    if request.method == "POST":
        question = request.form.get("que")
        answer = ask(question)
        return render_template("answer.html", que=question, data=answer)
    return render_template("Aboutus.html")


app.run(debug=False,host='0.0.0.0')
