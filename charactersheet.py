from flask import Flask, g, render_template, request, redirect, session, url_for, escape
import sqlite3

app = Flask(__name__)
app.secret_key = "1234567890qwertyuiopasdfghjklzxcvbnmokayherewego121234asdeRTFeDRAtAtygvdtygyatg7615287yGAsdTGAo7821g273gh87td9wyd678gyGFUAYdgouy9"
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

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
        session['username'] = request.form['username']
        return render_template('login.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/login')

@app.route('/')
def contents():
    cursor = get_db().cursor()
    sql = "SELECT * FROM sheet"
    cursor.execute(sql)
    sheets = cursor.fetchall()
    return render_template('contents.html', sheets=sheets)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["character_name"]
        new_class = request.form["character_class"]
        new_race = request.form["character_race"]
        sql = "INSERT INTO sheet(CharacterName, Class, Race) VALUES (?, ?, ?)"
        cursor.execute(sql,(new_name, new_class, new_race))
        get_db().commit()
    return render_template('newsheet.html')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["c_id"])
        sql = "DELETE FROM sheet WHERE id = ?"
        cursor.execute(sql, (id, ))
        get_db().commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST", "UPDATE"])
def edit(id):
    if request.method == "POST":
        cursor = get_db().cursor()
        edit_name = request.form["edit_character_name"]
        edit_class = request.form["edit_character_class"]
        edit_race = request.form["edit_character_race"]
        sql = '''UPDATE sheet 
        SET CharacterName = ?, Class = ?, Race = ?
        WHERE ID = ?'''
        cursor.execute(sql, (edit_name, edit_class, edit_race, id))
        get_db().commit()
        return redirect("/")
    return render_template('editsheet.html')

if __name__ == "__main__":
    app.run(debug=True)