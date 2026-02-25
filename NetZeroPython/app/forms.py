from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FloatField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

class CommuteForm(FlaskForm):
    commute_type = SelectField(
        "Select your commute method",
        choices = [
            ("walk", "Walk"),
            ("cycle", "Cycle"),
            ("car", "Car/Taxi"),
            ("train", "Train"),
            ("bus", "Bus")
            ],
    )
    commute_distance = FloatField("Distance (km)")

    submit = SubmitField("Submit")

class EnergyLogForm(FlaskForm):
    business_name = StringField(
        "Business Name",
        validators=[DataRequired(), Length(max=80)]
    )

    log_date = DateField("Date", validators=[DataRequired()], default=date.today)
    use_for = StringField("Used for (e.g. freezers)", validators=[DataRequired(), Length(max=80)])
    kwh = FloatField("Energy (kWh)", validators=[DataRequired(), NumberRange(min=0)])
    cost = FloatField("Cost (£)", validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField("Add log")

