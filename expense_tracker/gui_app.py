import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Add expense
def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()

    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                   (amount, category, date))
    conn.commit()
    messagebox.showinfo("Success", "Expense Added!")

# View expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    output.delete("1.0", tk.END)
    for row in rows:
        output.insert(tk.END, str(row) + "\n")

# GUI Window
root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Amount").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Date").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack()
tk.Button(root, text="View Expenses", command=view_expenses).pack()

output = tk.Text(root, height=10)
output.pack()

root.mainloop()