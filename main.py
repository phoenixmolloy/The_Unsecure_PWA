from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import bcrypt
import user_management as dbHandler
import data_handler as sanitiser

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)


@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        print(feedback)
        feedback = sanitiser.make_web_safe(feedback)  # sanitise xss
        print(feedback)
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        print(username)
        # username = sanitiser.make_web_safe(username)
        print(username)
        # Input field validation: creates an error based off specific requirements
        try:
            password = sanitiser.check_password(password)
        except TypeError:
            # logger.error()
            print("TypeError logged")
        except ValueError as inst:
            # logger.error()
            print("ValueError logged")
        else:
            encoded_password = password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password=encoded_password, salt=salt)
            dbHandler.insertUser(username, hashed_password, DoB, salt)
            return render_template("/index.html")
        return render_template("/signup.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # sanitise username and password
        username = sanitiser.make_web_safe(username)
        password = sanitiser.make_web_safe(password)
        # hashed_password = bcrypt.hashpw(password)
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=8080)
