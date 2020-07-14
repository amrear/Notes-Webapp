### Dependencies

* Flask                    1.1.1

Make sure you set the `SECRET_KEY` in `application.py`.

**This app does not hash passwords and still has some security flaws. Maybe I improved it in future.**

Database schema:
`
CREATE TABLE users(
        username TEXT,
        password TEXT
);
CREATE TABLE notes(
        username TEXT,
        title TEXT,
        body TEXT
);
`