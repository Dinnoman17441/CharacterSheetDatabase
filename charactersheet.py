from flask import Flask, g, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'charactersheets.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def contents():
    cursor = get_db().cursor()
    sql = "SELECT * FROM mainContents"
    cursor.execute(sql)
    sheets = cursor.fetchall()
    return render_template('contents.html', sheets=sheets)

if __name__ == "__main__":
    app.run(debug=True)