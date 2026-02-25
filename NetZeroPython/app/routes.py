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
    app_root = os.path.dirname(__file__)

    with open(os.path.join(app_root, "data/emissions_sector.json"), "r") as f:
        sector_data = json.load(f)

    with open(os.path.join(app_root, "data/emissions_trend.json"), "r") as f:
        trend_data = json.load(f)

    sectors = sector_data["sectors"]
    trend = trend_data["trend"]

    sector_labels = [s["sector"] for s in sectors]
    sector_values = [float(s["total"]) for s in sectors]

    trend_labels = [t["week"] for t in trend]
    trend_values = [float(t["total"]) for t in trend]

    latest_week_total = trend_values[-1] if trend_values else 0.0
    daily_avg = latest_week_total / 7.0 if latest_week_total else 0.0

    data = {
        "period": sector_data.get("period", ""),
        "emissions_by_sector": {"labels": sector_labels, "values": sector_values},
        "trend": {"labels": trend_labels, "values": trend_values},
        "summary": {"latest_week_total": latest_week_total, "daily_avg": daily_avg}
    }

    return render_template("gov.html", data=data)
