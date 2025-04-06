import sqlite3 as sql
import time
import random
import bcrypt
import data_handler as sanitiser


def insertUser(username, password, DoB, salt):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth,salt) VALUES (?,?,?,?)",
        (username, password, DoB, salt),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    result = cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    # print(result.fetchone())
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        hashed_password = gethashed_password(username, password)
        cur.execute(f"SELECT * FROM users WHERE password = (?)", (hashed_password,))
        # print(result.fetchone())
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()


def gethashed_password(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    result = cur.execute(f"SELECT salt FROM users WHERE username = '{username}'")
    salt = result.fetchone()[0]
    my_encoded_password = password.encode()
    hashed_password = bcrypt.hashpw(password=my_encoded_password, salt=salt)
    return hashed_password


# retrieveUsers("user", "userpassword")
