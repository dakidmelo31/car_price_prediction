import numpy as np
import pandas as pd
from flask import Flask
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask import render_template, session, request, flash, jsonify
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json
import pickle
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
linear_regression_model = pickle.load( open("lin.pkl", "rb"))
pipe = pickle.load( open("pipe_model.pkl", "rb"))

X = [44,32,11,51,23]
linear_reg_prediction = linear_regression_model.predict([[22]])
print(linear_reg_prediction)
pipeline_prediction = pipe.predict([[22, 11, 15, 11]]) # horsepower curb-height engine-size highway-mpg
print( pipeline_prediction)

app.secret_key = "flaskwork"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://predictions.sqlite3"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5)

# db = SQLAlcemy(app)
# class predictions(db.Model):
#     _id = db.Column("id", db.integer, primary_key = True)
#     price = db.Column("price", db.integer)
#     horsepower = db.Column("horse_power", db.integer)
#     prediction = db.Column("prediction", db.float)

#     def __init__(self, price, horsepower, prediction):
#         self.price = price
#         self.prediction = prediction
#         self.horsepower = horsepower


@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" in session:
        user = session['user']
    else:
        return redirect(url_for("login"))

    return render_template("dashboard.html",  username= user["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        user = request.form
        session.permanent = True
        session['user'] = user
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")

@app.route("/predict", methods=["GET"])
def predict():
    mpg = request.args.get("mpg", 0, type=int)
    type = request.args.get("type", 0, type=int)
    if request.method == "GET":
        predicted_value = linear_regression_model.predict([[mpg]])

    return render_template("prediction.html", type="mpg", price= predicted_value) 

@app.route("/predict2", methods=["GET"])
def predict2():
    mpg = request.args.get("mpg", 0, type=int)
    curb_height = request.args.get("curb_height", 0, type=int)
    highway_mpg = request.args.get("highway_mpg", 0, type=int)
    horsepower = request.args.get("horsepower", 0, type=int)
    engine_size = request.args.get("engine_size", 0, type=int)
    print("show values")
    print(curb_height, highway_mpg, horsepower, engine_size)
    if request.method == "GET":
        pipeline_prediction = pipe.predict([[horsepower, curb_height, engine_size, highway_mpg]]) # horsepower curb_height engine_size highway_mpg

    return render_template("prediction2.html", price= pipeline_prediction) 

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have successfully logged out")
    return redirect(url_for("login"))


if __name__ == "__main__":
    # db.create_all()
    app.debug = True
    app.run(host ="192.168.116.106", threaded=True)