import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import matplotlib.pyplot as plt

# ======================
# Database Setup
# ======================
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ======================
# Add Expense GUI
# ======================
def add_expense():
    category = simpledialog.askstring("Category", "Enter expense category:")
    if not category:
        return
    try:
        amount = float(simpledialog.askstring("Amount", "Enter expense amount:"))
    except:
        messagebox.showerror("Error", "Invalid amount!")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense added successfully!")

# ======================
# View Expenses GUI
# ======================
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel(root)
    view_window.title("All Expenses")
    
    tree = ttk.Treeview(view_window, columns=("ID", "Category", "Amount"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    
    for exp in expenses:
        tree.insert("", tk.END, values=exp)
    
    tree.pack(fill=tk.BOTH, expand=True)

# ======================
# Delete Expense GUI
# ======================
def delete_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        messagebox.showinfo("Info", "No expenses to delete!")
        return

    # Create a selection window
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Expense")

    tree = ttk.Treeview(delete_window, columns=("ID", "Category", "Amount"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")
    
    for exp in expenses:
        tree.insert("", tk.END, values=exp)
    
    tree.pack(fill=tk.BOTH, expand=True)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an expense to delete!")
            return
        exp_id = tree.item(selected[0])["values"][0]
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Expense deleted!")
        delete_window.destroy()

    del_btn = tk.Button(delete_window, text="Delete Selected", command=delete_selected)
    del_btn.pack(pady=5)

# ======================
# Category Pie Chart GUI
# ======================
def category_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Info", "No data to plot!")
        return

    categories = [i[0] for i in data]
    amounts = [i[1] for i in data]

    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    plt.show()

# ======================
# Main GUI Window
# ======================
init_db()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("300x250")

tk.Label(root, text="Expense Tracker", font=("Arial", 16, "bold")).pack(pady=10)

tk.Button(root, text="Add Expense", width=20, command=add_expense).pack(pady=5)
tk.Button(root, text="View Expenses", width=20, command=view_expenses).pack(pady=5)
tk.Button(root, text="Delete Expense", width=20, command=delete_expense).pack(pady=5)
tk.Button(root, text="Show Category Chart", width=20, command=category_chart).pack(pady=5)
tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=5)

root.mainloop()
