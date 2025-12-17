# ---------------------------------------------------------
# STUDENT MANAGEMENT SYSTEM USING STREAMLIT + SQLITE
# ---------------------------------------------------------

import streamlit as st              # Streamlit for UI
import sqlite3 as sql               # SQLite database
import pandas as pd                 # Data handling and display

# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

# Connect to SQLite database (creates file if not exists)
conn = sql.connect("students.db", check_same_thread=False)

# Cursor object to execute SQL commands
cursor = conn.cursor()

# ---------------------------------------------------------
# CREATE TABLE
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique student ID
    name TEXT NOT NULL,                    -- Student name
    email TEXT UNIQUE,                     -- Student email
    phone TEXT,                            -- Phone number
    department TEXT,                       -- Department
    year INTEGER                           -- Academic year
)
""")

conn.commit()  # Save changes

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.title("STUDENT MANAGEMENT SYSTEM")

menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------------------------------------------------
# ADD STUDENT
# ---------------------------------------------------------

if choice == "Add Student":
    st.subheader("Add New Student")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    department = st.selectbox("Department", ["CSE", "AIML", "DS", "ECE"])
    year = st.selectbox("Year", [1, 2, 3, 4])

    if st.button("Save Student"):
        if name and email:
            cursor.execute(
                "INSERT INTO students (name, email, phone, department, year) VALUES (?, ?, ?, ?, ?)",
                (name, email, phone, department, year)
            )
            conn.commit()
            st.success("Student added successfully")
        else:
            st.error("Name and Email are mandatory")

# ---------------------------------------------------------
# VIEW STUDENTS
# ---------------------------------------------------------

elif choice == "View Students":
    st.subheader("All Students")

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "Department", "Year"])
    st.dataframe(df)

# ---------------------------------------------------------
# UPDATE STUDENT
# ---------------------------------------------------------

elif choice == "Update Student":
    st.subheader("Update Student Details")

    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    student_id = st.selectbox("Select Student ID", student_ids)

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()

    name = st.text_input("Name", student[1])
    email = st.text_input("Email", student[2])
    phone = st.text_input("Phone", student[3])
    department = st.selectbox("Department", ["CSE", "AIML", "DS", "ECE"], index=["CSE","AIML","DS","ECE"].index(student[4]))
    year = st.selectbox("Year", [1, 2, 3, 4], index=student[5]-1)

    if st.button("Update Student"):
        cursor.execute(
            """UPDATE students 
               SET name=?, email=?, phone=?, department=?, year=?
               WHERE id=?""",
            (name, email, phone, department, year, student_id)
        )
        conn.commit()
        st.success("Student updated successfully")

# ---------------------------------------------------------
# DELETE STUDENT
# ---------------------------------------------------------

elif choice == "Delete Student":
    st.subheader("Delete Student")

    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    student_id = st.selectbox("Select Student ID", student_ids)

    if st.button("Delete Student"):
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        st.warning("Student deleted successfully")

# ---------------------------------------------------------
# END OF APPLICATION
# ---------------------------------------------------------
