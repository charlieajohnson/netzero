from flask import Flask, flash, redirect, url_for, request, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

import os
import json
from app import app
from app import db
from app.forms import CommuteForm, EnergyLogForm
from app.models import CommuteLog, EnergyLog

@app.route('/')
def home():
    return render_template("home.html")

# Sean's pages
@app.route('/personal')
def personal():
    return render_template("personal.html")

@app.route('/personal/trackcommute', methods = ["GET", "POST"])
def commutetracker():
    carbon_per_km = {"walk": 0, "cycle": 0, "car": 200, "train": 32, "bus": 75}
    form = CommuteForm()
    summary = None

    if form.validate_on_submit():
        commute_method = str(form.commute_method.data)
        distance = float(form.distance.data)
        emissions = float(distance * carbon_per_km[commute_method])
        summary = {"type": commute_method,
                   "distance": distance,
                   "emissions": emissions}
        if commute_method != "car":
            summary["car_emissions"] = distance * carbon_per_km["car"]

        # Submit log of commute to database.
        log = CommuteLog(commute_method = commute_method,
                         distance = distance,
                         emissions = emissions)
        db.session.add(log)
        db.session.commit()
        flash(f'Commute successfully logged!')

        return redirect(url_for('personal'))

    commute_logs = CommuteLog.query.all()
    return render_template("commutetracker.html",
                           form = form,
                           commute_logs = commute_logs,
                           summary = summary)

@app.route('/personal/trackcommute/delete/<int:commute_id>', methods = ['GET', 'POST'])
def delete_commute_log(commute_id):
    commute = CommuteLog.query.get_or_404(commute_id)
    db.session.delete(commute)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/personal/trackcommute/update/<int:commute_id>', methods = ['GET', 'POST'])
def update_commute_log(commute_id):
    carbon_per_km = {"walk": 0, "cycle": 0, "car": 200, "train": 32, "bus": 75}
    commute = CommuteLog.query.get_or_404(commute_id)
    form = CommuteForm(obj=commute)

    if form.validate_on_submit():
        commute.commute_method = form.commute_method.data
        commute.distance = form.distance.data
        commute.emissions = float(commute.distance * carbon_per_km[commute.commute_method])
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('updatecommute.html', form = form)

# Ed's pages
@app.route("/business", methods=["GET", "POST"])
def business():
    form = EnergyLogForm()

    # Persist which business we're viewing via URL querystring
    business_name = request.args.get("business_name", "").strip()

    # Bonus: pre-fill business name if coming from URL
    if business_name and request.method == "GET":
        form.business_name.data = business_name

    if form.validate_on_submit():
        log = EnergyLog(
            business_name=form.business_name.data.strip(),
            log_date=form.log_date.data,
            use_for=form.use_for.data.strip(),
            kwh=float(form.kwh.data),
            cost=float(form.cost.data),
        )
        db.session.add(log)
        db.session.commit()
        flash("Energy log added.")

        # Redirect with business_name in the URL so it stays selected after POST
        return redirect(url_for("business", business_name=log.business_name))

    # Build query dynamically (search-style)
    query = EnergyLog.query
    if business_name:
        query = query.filter(EnergyLog.business_name.ilike(f"%{business_name}%"))

    logs = query.order_by(EnergyLog.log_date.desc()).all()

    total_kwh = sum(l.kwh for l in logs) if logs else 0
    total_cost = sum(l.cost for l in logs) if logs else 0

    return render_template(
        "business.html",
        form=form,
        logs=logs,
        total_kwh=total_kwh,
        total_cost=total_cost,
        business_name=business_name
    )


@app.route("/business/logs/<int:log_id>/delete")
def delete_energy_log(log_id: int):
    log = EnergyLog.query.get_or_404(log_id)
    business_name = log.business_name
    db.session.delete(log)
    db.session.commit()
    flash("Log deleted.")
    return redirect(url_for("business", business_name=business_name))

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

