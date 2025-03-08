from flask import Flask, render_template, request, redirect, url_for
import psycopg2 
import hashlib

app = Flask(__name__)

# MySQL Configuration
pooling_url = "postgresql://postgres:mivaflask12@db.xanuhuwknzdprmudmoph.supabase.co:5432/postgres"
db_config = {
  'host': 'db.xanuhuwknzdprmudmoph.supabase.co', 
  'port': '5432',
  'database': 'postgres',
   'password': 'mivaflask12',
  'user': 'postgres',
  'sslmode': 'require'
}

# Connect to the database
def get_db():
  db = psycopg2.connect(**db_config)
  return db

# Home page 

@app.route("/")
def home():
  return render_template("index.html")

# signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    # Get form data
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert user data into the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tbl_user (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("home"))
  return render_template("signup.html")

#Run the App
if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

