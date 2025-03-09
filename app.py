from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

# MySQL Configuration
DATABASE = 'database.db'

# Connect to the database

def get_db():
  db = sqlite3.connect(DATABASE)
  db.row_factory = sqlite3.Row
  return db

# Create a table to store user information
def init_db():
  db = get_db()
  db.execute(
    '''CREATE TABLE IF NOT EXISTS tbl_user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)'''
  )
  db.commit()
  db.close()

init_db()



# Home page 

@app.route("/")
def home():
  return render_template("index.html")

# signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    # Get form data
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
      return "Please enter both username and password.", 400
      
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert user data into the database
    db = get_db()
    db.execute("INSERT INTO tbl_user (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()
    db.close()
    return redirect(url_for("home"))
  return render_template("signup.html")

#Run the App
if __name__ == "__main__":
  init_db()
  app.run(host='0.0.0.0',debug=True)

