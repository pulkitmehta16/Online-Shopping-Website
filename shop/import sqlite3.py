import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
# Create Database and Table
def create_db():
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
roll_no INTEGER UNIQUE NOT NULL,
admission_date TEXT NOT NULL,
course TEXT NOT NULL,
email TEXT NOT NULL,
marks REAL DEFAULT 0,
fee_paid REAL DEFAULT 0,
fee_balance REAL DEFAULT 0
)
""")
conn.commit()
conn.close()# Validate Numeric Fields
def validate_numeric(value, field_name):
try:
if value == "": # Allow empty values
return True
float(value)
return True
except ValueError:
messagebox.showerror("Error", f"{field_name} must be a numeric value!")
return False
# Validate Date Format
def validate_date(date_text):
try:
datetime.strptime(date_text, "%Y-%m-%d")
return True
except ValueError:
messagebox.showerror("Error", "Admission Date must be in YYYY-MM-DD format!")
return False
# Add Student to Database
def add_student():
name = name_entry.get()
roll_no = roll_no_entry.get()
admission_date = admission_date_entry.get()
course = course_entry.get()
email = email_entry.get()marks = marks_entry.get()
fee_paid = fee_paid_entry.get()
fee_balance = fee_balance_entry.get()
if name and roll_no and admission_date and course and email:
if not validate_date(admission_date):
return
if not (validate_numeric(marks, "Marks") and validate_numeric(fee_paid, "Fee Paid") and 
validate_numeric(fee_balance, "Fee Balance")):
return
try:
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute("""
INSERT INTO students (name, roll_no, admission_date, course, email, marks, fee_paid, fee_balance) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (name, roll_no, admission_date, course, email, marks or 0, fee_paid or 0, fee_balance or 0))
conn.commit()
conn.close()
fetch_data()
clear_entries()
messagebox.showinfo("Success", "Student added successfully!")
except sqlite3.IntegrityError:
messagebox.showerror("Error", "Roll number must be unique!")
else:
messagebox.showerror("Error", "Name, Roll No, Admission Date, Course, and Email are required!")
# Fetch and Display Datadef fetch_data():
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
conn.close()
# Clear existing data in the Treeview
for row in tree.get_children():
tree.delete(row)
# Insert the fetched rows into the Treeview
for row in rows:
tree.insert("", END, values=row)
# Update Student in Database (Specific Columns)
def update_student():
# Check if a student is selected in the Treeview
if not tree.selection():
messagebox.showerror("Error", "No student selected!")
return
# Get the selected student's ID (primary key)
selected_item = tree.selection()[0]
selected_id = tree.item(selected_item)['values'][0]
# Retrieve the values from the entry fields (only non-empty ones will be updated)name = name_entry.get()
roll_no = roll_no_entry.get()
admission_date = admission_date_entry.get()
course = course_entry.get()
email = email_entry.get()
marks = marks_entry.get()
fee_paid = fee_paid_entry.get()
fee_balance = fee_balance_entry.get()
# List to hold the columns that need updating
update_columns = []
update_values = []
# Check if the fields are changed and add them to the update list
if name:
update_columns.append("name = ?")
update_values.append(name)
if roll_no:
update_columns.append("roll_no = ?")
update_values.append(roll_no)
if admission_date:
if not validate_date(admission_date): # Validate the date format
return
update_columns.append("admission_date = ?")
update_values.append(admission_date)
if course:
update_columns.append("course = ?")update_values.append(course)
if email:
update_columns.append("email = ?")
update_values.append(email)
if marks:
if not validate_numeric(marks, "Marks"):
return
update_columns.append("marks = ?")
update_values.append(marks)
if fee_paid:
if not validate_numeric(fee_paid, "Fee Paid"):
return
update_columns.append("fee_paid = ?")
update_values.append(fee_paid)
if fee_balance:
if not validate_numeric(fee_balance, "Fee Balance"):
return
update_columns.append("fee_balance = ?")
update_values.append(fee_balance)
# If no fields are selected for update, show an error
if not update_columns:
messagebox.showerror("Error", "No changes made to update!")
return
# Add the student ID to the update values list (to identify the record)
update_values.append(selected_id)# Construct the SQL update query
update_query = f"""
UPDATE students
SET {', '.join(update_columns)}
WHERE id = ?
"""
try:
# Execute the update query
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute(update_query, tuple(update_values))
conn.commit()
conn.close()
# Refresh the displayed data in the Treeview
fetch_data()
clear_entries()
messagebox.showinfo("Success", "Student updated successfully!")
except sqlite3.Error as e:
messagebox.showerror("Error", f"An error occurred: {e}")
# Delete Student from Database
def delete_student():
    if not tree.selection():
        messagebox.showerror("Error", "No student selected!")return
selected_item = tree.selection()[0]
selected_id = tree.item(selected_item)['values'][0]
conn = sqlite3.connect('students.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM students WHERE id = ?", (selected_id,))
conn.commit()
conn.close()
fetch_data()
clear_entries()
messagebox.showinfo("Success", "Student deleted successfully!")
# Clear Entry Fields
def clear_entries():
    for widget in frame.winfo_children():
        if isinstance(widget, Entry):
            widget.delete(0, END)
# GUI Setup
root = Tk()
root.title("Enhanced Student Management System")
root.geometry("900x600")
# Entry Form
frame = Frame(root, pady=20)
frame.pack()Label(frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(frame, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)
Label(frame, text="Roll No:").grid(row=1, column=0, padx=10, pady=5)
roll_no_entry = Entry(frame, width=30)
roll_no_entry.grid(row=1, column=1, padx=10, pady=5)
Label(frame, text="Admission Date:").grid(row=2, column=0, padx=10, pady=5)
admission_date_entry = Entry(frame, width=30)
admission_date_entry.grid(row=2, column=1, padx=10, pady=5)
Label(frame, text="Course:").grid(row=0, column=2, padx=10, pady=5)
course_entry = Entry(frame, width=20)
course_entry.grid(row=0, column=3, padx=10, pady=5)
Label(frame, text="Email ID:").grid(row=1, column=2, padx=10, pady=5)
email_entry = Entry(frame, width=20)
email_entry.grid(row=1, column=3, padx=10, pady=5)
Label(frame, text="Marks:").grid(row=2, column=2, padx=10, pady=5)
marks_entry = Entry(frame, width=20)
marks_entry.grid(row=2, column=3, padx=10, pady=5)
Label(frame, text="Fee Paid:").grid(row=3, column=0, padx=10, pady=5)
fee_paid_entry = Entry(frame, width=20)fee_paid_entry.grid(row=3, column=1, padx=10, pady=5)
Label(frame, text="Fee Balance:").grid(row=3, column=2, padx=10, pady=5)
fee_balance_entry = Entry(frame, width=20)
fee_balance_entry.grid(row=3, column=3, padx=10, pady=5)
Button(frame, text="Add", command=add_student, width=10, bg="green", fg="white").grid(row=4, column=0, 
pady=10)
Button(frame, text="Update", command=update_student, width=10, bg="blue", fg="white").grid(row=4, 
column=1, pady=10)
Button(frame, text="Delete", command=delete_student, width=10, bg="red", fg="white").grid(row=4, 
column=2, pady=10)
Button(frame, text="Clear", command=clear_entries, width=10, bg="gray", fg="white").grid(row=4, column=3, 
pady=10)
# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Roll No", "Admission Date", "Course", "Email", "Marks", "Fee 
Paid", "Fee Balance"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Roll No", text="Roll No")
tree.heading("Admission Date", text="Admission Date")
tree.heading("Course", text="Course")
tree.heading("Email", text="Email")
tree.heading("Marks", text="Marks")
tree.heading("Fee Paid", text="Fee Paid")
tree.heading("Fee Balance", text="Fee Balance")tree.column("ID", width=50)
tree.column("Name", width=200)
tree.column("Roll No", width=100)
tree.column("Admission Date", width=150)
tree.column("Course", width=150)
tree.column("Email", width=200)
tree.column("Marks", width=100)
tree.column("Fee Paid", width=100)
tree.column("Fee Balance", width=100)
tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
create_db() # Ensure database and table are created
fetch_data() # Display existing data
root.mainloop()