from flask import Flask, flash, redirect, url_for, request, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from app import app
from app.forms import CommuteForm

@app.route('/')
def home():
    return render_template("home.html")

# Sean's pages
@app.route('/personal')
def personal():
    return render_template("personal.html")

@app.route('/trackcommute', methods = ["GET", "POST"])
def commutetracker():
    carbon_per_km = {"walk": 0, "cycle": 0, "car": 200, "train": 32, "bus": 75}
    form = CommuteForm()
    summary = None
    if form.validate_on_submit():
        commute_type = form.commute_type.data
        distance = form.commute_distance.data
        emissions = distance * carbon_per_km[commute_type]
        summary = {"type": commute_type,
                   "distance": distance,
                   "emissions": emissions}
        if commute_type != "car":
            summary["car_emissions"] = distance * carbon_per_km["car"]
    return render_template("commutetracker.html", form = form, summary = summary)

# Ed's pages
@app.route('/business')
def business():
    return "For businesses."

# Tannbir's pages
@app.route('/gov')
def gov():
    return "For the government."