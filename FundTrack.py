import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "expenses.csv"
USER_FILE = "user.csv"

class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FundTrack - Login")
        self.root.geometry("400x500")
        self.style = tb.Style("cosmo")
        self.current_theme = "cosmo"

        # Create main container with padding
        self.main_frame = tb.Frame(self.root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        self.create_auth_widgets()

    def create_auth_widgets(self):
        # Create a container frame with light background
        auth_frame = tb.Frame(self.main_frame, padding=20, bootstyle="light")
        auth_frame.pack(fill="both", expand=True)

        # App Logo/Title
        logo_label = tb.Label(
            auth_frame,
            text="💰 FundTrack",
            font=("Helvetica", 32, "bold"),
            bootstyle="primary"
        )
        logo_label.pack(pady=(0, 10))

        # Subtitle
        subtitle_label = tb.Label(
            auth_frame,
            text="Your Personal Expense Manager",
            font=("Helvetica", 12),
            bootstyle="secondary"
        )
        subtitle_label.pack(pady=(0, 30))

        # Username field
        username_frame = tb.Frame(auth_frame)
        username_frame.pack(fill="x", pady=10)

        tb.Label(
            username_frame,
            text="Username",
            font=("Helvetica", 12),
            bootstyle="primary"
        ).pack(anchor="w")

        self.username_entry = tb.Entry(
            username_frame,
            bootstyle="primary",
            font=("Helvetica", 11),
            width=30
        )
        self.username_entry.pack(fill="x", pady=(5, 0))

        # Password field
        password_frame = tb.Frame(auth_frame)
        password_frame.pack(fill="x", pady=10)

        tb.Label(
            password_frame,
            text="Password",
            font=("Helvetica", 12),
            bootstyle="primary"
        ).pack(anchor="w")

        self.password_entry = tb.Entry(
            password_frame,
            bootstyle="primary",
            font=("Helvetica", 11),
            width=30,
            show="•"
        )
        self.password_entry.pack(fill="x", pady=(5, 0))

        # Buttons
        button_frame = tb.Frame(auth_frame)
        button_frame.pack(pady=30)

        login_button = tb.Button(
            button_frame,
            text="Login",
            command=self.login,
            bootstyle="success",
            width=15,
            padding=10
        )
        login_button.pack(side="left", padx=5)

        register_button = tb.Button(
            button_frame,
            text="Register",
            command=self.register,
            bootstyle="primary",
            width=15,
            padding=10
        )
        register_button.pack(side="left", padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        users = self.read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                messagebox.showinfo("Success", "Login successful!")
                self.main_frame.destroy()
                ExpenseTracker(self.root)
                return

        messagebox.showerror("Error", "Invalid username or password!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return

        users = self.read_users()
        for user in users:
            if user[0] == username:
                messagebox.showerror("Error", "Username already exists!")
                return

        with open(USER_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

        messagebox.showinfo("Success", "Registration successful! Please login.")

    def read_users(self):
        if not os.path.exists(USER_FILE):
            return []
        with open(USER_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("FundTrack")
        self.root.geometry("1200x800")
        self.selected_id = None

        self.style = tb.Style("cosmo")
        self.current_theme = "cosmo"
        self.custom_font = ("Helvetica", 12)

        # Main container
        self.main_frame = tb.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.create_header()
        self.create_widgets()
        self.load_expenses()

    def create_header(self):
        # Header with gradient effect
        header_frame = tb.Frame(self.main_frame, bootstyle="primary")
        header_frame.pack(fill="x", pady=0)

        # Title container
        title_container = tb.Frame(header_frame, bootstyle="primary")
        title_container.pack(side="left", padx=20, pady=15)

        # App title with icon
        tb.Label(
            title_container,
            text="💰 FundTrack",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-primary"
        ).pack(side="top", anchor="w")

        # Subtitle
        tb.Label(
            title_container,
            text="Track your expenses easily and efficiently",
            font=("Helvetica", 12),
            bootstyle="inverse-primary"
        ).pack(side="top", anchor="w")

        # Right side controls
        controls_frame = tb.Frame(header_frame, bootstyle="primary")
        controls_frame.pack(side="right", padx=20, pady=15)

        # Search box with icon
        search_frame = tb.Frame(controls_frame, bootstyle="primary")
        search_frame.pack(side="left", padx=(0, 20))

        self.search_var = tk.StringVar()
        self.search_entry = tb.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            bootstyle="primary",
            font=("Helvetica", 11)
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_expenses)

        # Search button
        search_button = tb.Button(
            search_frame,
            text="🔍 Search",
            command=self.search_expenses,
            bootstyle="outline-primary",
            width=12
        )
        search_button.pack(side="left", padx=5)

        # Theme toggle
        self.theme_button = tb.Button(
            controls_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme,
            bootstyle="outline-primary",
            width=12
        )
        self.theme_button.pack(side="right")

    def create_widgets(self):
        # Content container with padding
        content_frame = tb.Frame(self.main_frame, padding=20)
        content_frame.pack(fill="both", expand=True)

        # Form section
        form_frame = tb.LabelFrame(content_frame, text="Add New Expense", padding=15, bootstyle="primary")
        form_frame.pack(fill="x", pady=(0, 20))

        # Grid layout for form
        form_grid = tb.Frame(form_frame)
        form_grid.pack(fill="x")

        # Category
        tb.Label(form_grid, text="Category:", font=self.custom_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.category = tb.Combobox(
            form_grid,
            values=["Food", "Transport", "Shopping", "Bills", "Other"],
            width=25,
            font=self.custom_font
        )
        self.category.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Amount
        tb.Label(form_grid, text="Amount:", font=self.custom_font).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.amount = tb.Entry(form_grid, width=25, font=self.custom_font)
        self.amount.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.amount.bind("<KeyRelease>", self.validate_amount)

        # Date
        tb.Label(form_grid, text="Date:", font=self.custom_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        date_frame = tb.Frame(form_grid)
        date_frame.grid(row=1, column=1, columnspan=2, sticky="w")

        self.date = tb.Entry(date_frame, width=25, font=self.custom_font)
        self.date.pack(side="left", padx=(10, 5))
        self.date.insert(0, datetime.today().strftime("%Y-%m-%d"))

        self.use_today_date = tk.BooleanVar(value=True)
        self.date_checkbox = tb.Checkbutton(
            date_frame,
            text="Use today's date",
            variable=self.use_today_date,
            command=self.toggle_date_entry,
            bootstyle="primary-round-toggle"
        )
        self.date_checkbox.pack(side="left")

        # Description
        tb.Label(form_grid, text="Description:", font=self.custom_font).grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.description = tb.Entry(form_grid, width=25, font=self.custom_font)
        self.description.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Action buttons
        button_frame = tb.Frame(content_frame)
        button_frame.pack(fill="x", pady=(0, 20))

        buttons = [
            ("➕ Add/Update", self.add_update_expense, "success"),
            ("🗑️ Delete", self.delete_expense, "danger"),
            ("📊 Show Graph", self.show_graph, "info"),
            ("💾 Export CSV", self.export_to_csv, "primary")
        ]

        for text, cmd, style in buttons:
            btn = tb.Button(
                button_frame,
                text=text,
                command=cmd,
                bootstyle=style,
                width=15,
                padding=10
            )
            btn.pack(side="left", padx=5)

        # Table
        table_frame = tb.LabelFrame(content_frame, text="Expense Records", padding=15, bootstyle="primary")
        table_frame.pack(fill="both", expand=True)

        # Configure style for treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=self.custom_font)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        # Create Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Category", "Amount", "Date", "Description"),
            show="headings",
            height=15
        )

        # Configure columns
        column_configs = {
            "ID": (80, "center"),
            "Category": (150, "center"),
            "Amount": (120, "e"),
            "Date": (120, "center"),
            "Description": (400, "w")
        }

        for col, (width, align) in column_configs.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=align)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<ButtonRelease-1>", self.select_expense)

    def toggle_theme(self):
        if self.current_theme == "cosmo":
            self.style.theme_use("darkly")
            self.current_theme = "darkly"
            self.theme_button.config(text="☀️ Light Mode")
        else:
            self.style.theme_use("cosmo")
            self.current_theme = "cosmo"
            self.theme_button.config(text="🌙 Dark Mode")

    def search_expenses(self, event=None):
        search_term = self.search_var.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.read_csv():
            if (search_term in row[1].lower() or
                search_term in row[2].lower() or
                search_term in row[3].lower() or
                search_term in row[4].lower()):
                self.tree.insert("", tk.END, values=row)

    def validate_amount(self, event):
        value = self.amount.get()
        if not value.replace(".", "", 1).isdigit() and value:
            self.amount.delete(0, tk.END)
            self.amount.insert(0, "".join(filter(lambda x: x.isdigit() or x == ".", value)))

    def toggle_date_entry(self):
        if self.use_today_date.get():
            self.date.delete(0, tk.END)
            self.date.insert(0, datetime.today().strftime("%Y-%m-%d"))
            self.date.configure(state="disabled")
        else:
            self.date.configure(state="normal")

    def add_update_expense(self):
        category, amount, description = self.category.get(), self.amount.get(), self.description.get()
        date = datetime.today().strftime("%Y-%m-%d") if self.use_today_date.get() else self.date.get()

        if not category or not amount or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Amount must be a number and Date in YYYY-MM-DD format.")
            return

        expenses = self.read_csv()
        if self.selected_id:
            for row in expenses:
                if row[0] == self.selected_id:
                    row[1:] = [category, str(amount), date, description]
                    break
        else:
            new_id = str(self.get_next_id(expenses))
            expenses.append([new_id, category, str(amount), date, description])

        self.write_csv(expenses)
        self.load_expenses()
        self.clear_entries()

    def select_expense(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = values[0]
        self.category.set(values[1])
        self.amount.delete(0, tk.END)
        self.amount.insert(0, values[2])
        self.date.delete(0, tk.END)
        self.date.insert(0, values[3])
        self.use_today_date.set(False)
        self.date.configure(state="normal")
        self.description.delete(0, tk.END)
        self.description.insert(0, values[4])

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
            expense_id = self.tree.item(selected[0], "values")[0]
            expenses = [row for row in self.read_csv() if row[0] != expense_id]
            self.write_csv(expenses)
            self.load_expenses()
            self.clear_entries()

    def load_expenses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.read_csv():
            self.tree.insert("", tk.END, values=row)

    def export_to_csv(self):
        expenses = self.read_csv()
        if not expenses:
            messagebox.showwarning("Warning", "No expenses to export!")
            return

        export_file = "exported_expenses.csv"
        with open(export_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Category", "Amount", "Date", "Description"])
            writer.writerows(expenses)
        messagebox.showinfo("Success", f"Expenses exported to {export_file}!")

    def show_graph(self):
        expenses = self.read_csv()
        if not expenses:
            messagebox.showinfo("Info", "No expenses to display!")
            return

        categories = {}
        for row in expenses:
            category = row[1]
            amount = float(row[2])
            categories[category] = categories.get(category, 0) + amount

        plt.figure(figsize=(10, 6))
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
        plt.pie(categories.values(), labels=categories.keys(), colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title("Expense Distribution by Category")
        plt.show()

    def read_csv(self):
        if not os.path.exists(CSV_FILE):
            return []
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)

    def write_csv(self, data):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def clear_entries(self):
        self.category.set("")
        self.amount.delete(0, tk.END)
        self.date.delete(0, tk.END)
        self.date.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.use_today_date.set(True)
        self.date.configure(state="disabled")
        self.description.delete(0, tk.END)
        self.selected_id = None

    def get_next_id(self, expenses):
        if not expenses:
            return 1
        return max(int(row[0]) for row in expenses) + 1

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    auth_app = AuthApp(root)
    root.mainloop()