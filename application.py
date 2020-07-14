import db_funcs as db
from flask import Flask, render_template, redirect, url_for, request, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "Put your secret key here!"


@app.route("/", methods=["GET", "POST"])
def index():
    user = session.get("user")
    if not user:
        # If a session doesn't exist for the user, it means user is not logged in.
        # We'll redirect him/her to the login page.
        return redirect(url_for("login"))

    title = request.form.get("title")
    body = request.form.get("body")
    notes = db.get_notes(user)         # Fetches the notes of a specific user.
    if title and body:
        # If user provided a new note the note will be added to his/her notes in database.
        if len(title) <= 64 and len(body) <= 1024:
            # The note shout meat certain requirements.
            db.add_note(user, title, body)
            flash("Note has been added.", "success")
            return redirect(url_for("index"))
        else:
            flash("Title or body are too long.", "danger")
            return redirect(url_for("index"))
    elif title == "" or body == "":
        # If one or both fields of the note is empty.
        flash("Please fill the inputs.", "danger")
        return redirect(url_for("index"))

    return render_template("index.html", notes=notes)

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if (username is None) or (password is None):
        # Checks to see if username and password is provided by the user.
        return render_template("login.html")
    else:
        if not username or not password:
            # Checks to see if the fields ae empty.
            flash("Some fields are empty!", "danger")
            return redirect(url_for("login"))
        if db.login(username, password):
            # Checks if the data provided by user is legitemate
            session["user"] = username
            return redirect(url_for("index"))
        else:
            flash("Username or password are incorrect", "danger")
            return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    cpassword = request.form.get("cpassword")           # Stands for confirm password
    if (username is None) or (password is None) or (cpassword is None):
        # Checks to see if username, password, and confirm password  is provided by the user.
        return render_template("signup.html")
    else:
        if not username or not password:
            # Checks to see if the fields ae empty.
            flash("Some fields are empty!", "danger")
            return redirect(url_for("signup"))
        if password != cpassword:
            # If password and confirm password are equal.
            flash("Passwords don't match!", "danger")
            return redirect(url_for("signup"))
        if len(password) < 8:
            # The password sould be at least 8 characters.
            flash("Password should at least be 8 characters!", "danger")
            return redirect(url_for("signup"))
        if db.check_username(username):
            # Checks to see if the username already exists.
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))

        # If the user meats all of the requirements then we'll add him/her to the database
        db.signup(username, password)
        session["user"] = username
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
