"""This script contains some functions for querying database that are used in `application.py`"""

import sqlite3

def check_username(username):
    """
    This function checks to see if the username exists.
    Returns True if it exists and False if it doesn't.
    """
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT username FROM users WHERE username = ?;", (username,))
    return bool(c.fetchall())

def signup(username, password):
    """This function adds new users to database."""
    con = sqlite3.connect("database.db")
    c = con.cursor()
    with con:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    con.close()

def login(username, password):
    """
    This function checks if the provided password is legitemate or not.
    Returns True if it is and False if it's not.
    """
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT password FROM users WHERE username = ?;", (username,))
    resault = c.fetchone()
    con.close()
    if resault:
        return resault[0] == password

    return False

def add_note(username, title, body):
    """This function adds new notes to the database"""
    con = sqlite3.connect("database.db")
    c = con.cursor()
    with con:
        c.execute("INSERT INTO notes (username, title, body) VALUES (?, ?, ?);", (username, title, body))
    con.close()

def get_notes(username):
    """This function fetches the notes for a specific user from database."""
    con = sqlite3.connect("database.db")
    c = con.cursor()
    c.execute("SELECT title, body FROM notes WHERE username = ?;", (username,))
    resaults = c.fetchall()
    con.close()
    return resaults