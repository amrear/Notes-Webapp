import db_funcs as db
from flask import Flask, render_template, redirect, url_for, request, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "0973a08f7f57a61b0353bc8b6683169c"


@app.route("/", methods=["GET", "POST"])
def index():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))

    title = request.form.get("title")
    body = request.form.get("body")
    notes = db.get_notes(user)
    if title and body:
        if len(title) <= 64 and len(body) <= 1024:
            db.add_note(user, title, body)
            flash("Note has been added.", "success")
            return redirect(url_for("index"))
        else:
            flash("Title or body are too long.", "danger")
            return redirect(url_for("index"))
    elif title == "" or body == "":
        flash("Please fill the inputs.", "danger")
        return redirect(url_for("index"))

    return render_template("index.html", notes=notes)

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if (username is None) or (password is None):
        return render_template("login.html")
    else:
        if not username or not password:
            flash("Some fields are empty!", "danger")
            return redirect(url_for("login"))
        if db.login(username, password):
            session["user"] = username
            return redirect(url_for("index"))
        else:
            flash("Username or password are incorrect", "danger")
            return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    cpassword = request.form.get("cpassword")
    if (username is None) or (password is None) or (cpassword is None):
        return render_template("signup.html")
    else:
        if not username or not password:
            flash("Some fields are empty!", "danger")
            return redirect(url_for("signup"))
        if password != cpassword:
            flash("Passwords don't match!", "danger")
            return redirect(url_for("signup"))
        if len(password) < 8:
            flash("Password should at least be 8 characters!", "danger")
            return redirect(url_for("signup"))
        if not db.check_username(username):
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))

        db.signup(username, password)
        session["user"] = username
        return redirect(url_for("index"))


@app.route("/json")
def json():
    return "json"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
