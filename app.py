import pandas as pd
import joblib
from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    flash,
    session
)
from forms import InputForm, SignupForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Replace with an environment variable for security

# Load the model (ensure model.joblib is in the correct path)
model = joblib.load("model.joblib")

@app.route("/")
def index():
    if not session.get("signed_up"):
        return render_template("index.html", title="Main")
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("signed_up"):
        return redirect(url_for("login"))
    form = SignupForm()
    if form.validate_on_submit():
        # Store user data or set a flag that user has signed up
        session["signed_up"] = True
        flash(f"Successfully Registered {form.username.data}", "success")
        return redirect(url_for("login"))
    return render_template("signup.html", title="Signup", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if not session.get("signed_up"):
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw = form.password.data
        # Example hardcoded credentials; replace with database or proper authentication
        if email and pw:
            session["logged_in"] = True
            flash("Logged in Successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Incorrect email or password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if not session.get("logged_in"):
        flash("Please log in to access the home page.", "danger")
        return redirect(url_for("login"))
    return render_template("home.html", title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if not session.get("logged_in"):
        flash("Please log in to access the prediction page.", "danger")
        return redirect(url_for("login"))

    form = InputForm()
    if form.validate_on_submit():
        x_new = pd.DataFrame({
            "airline": [form.airline.data],
            "date_of_journey": [form.date_of_journey.data.strftime("%Y-%m-%d")],
            "source": [form.source.data],
            "destination": [form.destination.data],
            "dep_time": [form.dep_time.data.strftime("%H:%M:%S")],
            "arrival_time": [form.arrival_time.data.strftime("%H:%M:%S")],
            "duration": [form.duration.data],
            "total_stops": [form.total_stops.data],
            "additional_info": [form.additional_info.data]
        })
        prediction = model.predict(x_new)[0]
        message = f"The predicted price is {prediction:,.0f} INR!"
        flash(message, "success")
    else:
        message = "Please provide valid input details!"
        flash(message, "danger")
    return render_template("predict.html", title="Predict", form=form, output=message)

if __name__ == "__main__":
    app.run(debug=True)
