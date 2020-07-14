import sqlite3

def check_username(username):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT username FROM users WHERE username = ?;", (username,))
    if c.fetchall():
        return False

    return True

def signup(username, password):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    with con:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    con.close()

def login(username, password):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT password FROM users WHERE username = ?;", (username,))
    resault = c.fetchone()
    con.close()
    if resault:
        return resault[0] == password

    return False

def add_note(username, title, body):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    with con:
        c.execute("INSERT INTO notes (username, title, body) VALUES (?, ?, ?);", (username, title, body))
    con.close()

def get_notes(username):
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT title, body FROM notes WHERE username = ?;", (username,))
    resaults = c.fetchall()
    con.close()
    return resaults