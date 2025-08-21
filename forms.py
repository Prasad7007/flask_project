#forms.py
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateField,
    TimeField,
    IntegerField,
    SubmitField,
    StringField,
    BooleanField,
    PasswordField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Optional,
    EqualTo
)

# Load data for form choices
train = pd.read_csv("data/train.csv")
val = pd.read_csv("data/val.csv")
X_data = pd.concat([train, val], axis=0).drop(columns="price")

class InputForm(FlaskForm):
    airline = SelectField(
        label="Airline",
        choices=X_data.airline.unique().tolist(),
        validators=[DataRequired()]
    )
    date_of_journey = DateField(
        label="Date of Journey",
        validators=[DataRequired()]
    )
    source = SelectField(
        label="Source",
        choices=X_data.source.unique().tolist(),
        validators=[DataRequired()]
    )
    destination = SelectField(
        label="Destination",
        choices=X_data.destination.unique().tolist(),
        validators=[DataRequired()]
    )
    dep_time = TimeField(
        label="Departure Time",
        validators=[DataRequired()]
    )
    arrival_time = TimeField(
        label="Arrival Time",
        validators=[DataRequired()]
    )
    duration = IntegerField(
        label="Duration",
        validators=[DataRequired()]
    )
    total_stops = IntegerField(
        label="Total Stops",
        validators=[DataRequired()]
    )
    additional_info = SelectField(
        label="Additional Info",
        choices=X_data.additional_info.unique().tolist(),
        validators=[DataRequired()]
    )
    submit = SubmitField("Predict")

class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(2, 30)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    gender = SelectField(
        "Gender",
        choices=["Male", "Female", "Other"],
        validators=[Optional()]
    )
    dob = DateField(
        "Date of Birth",
        validators=[Optional()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(8, 30)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")]
    )
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(8, 30)]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
