from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired

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