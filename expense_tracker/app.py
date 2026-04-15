from flask import Flask, render_template, request, redirect, session
import sqlite3

import matplotlib.pyplot as plt
import os

def show_chart(cursor):
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    if not data:
        return
    
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts)
    plt.title("Expense by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_dir, exist_ok=True)
    plt.savefig(os.path.join(static_dir, 'chart.png'))
    plt.close()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "mysecretkey"
with sqlite3.connect("expenses.db") as conn:
    cursor = conn.cursor()

    # expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():

    if "user" not in session:
        return redirect("/login")   # 🔒 protection

    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()

        if request.method == "POST":
            amount = request.form["amount"]
            category = request.form["category"]
            date = request.form["date"]

            cursor.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?)",
                           (amount, category, date))
            conn.commit()

        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()

    return render_template("index.html", data=data)
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]

        cursor.execute("UPDATE expenses SET amount=?, category=?, date=? WHERE id=?",
                       (amount, category, date, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM expenses WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()

    return render_template("edit.html", data=data)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None    

    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == "admin" and pwd == "123":
            session["user"] = user   # ✅ store login
            return redirect("/")
        else:
            error = "Invalid login"

    return render_template("login.html", error=error)
@app.route("/chart")
def chart():

    if "user" not in session:
        return redirect("/login")

    with sqlite3.connect("expenses.db") as conn:
        cursor = conn.cursor()
        show_chart(cursor)

    return render_template("chart.html")
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)