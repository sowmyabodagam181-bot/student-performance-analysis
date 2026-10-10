from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("students.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                semester INTEGER NOT NULL,
                math REAL NOT NULL,
                python REAL NOT NULL,
                dbms REAL NOT NULL,
                attendance REAL NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        if count == 0:
            conn.executemany("""
                INSERT INTO students
                (student_id, name, department, semester, math, python, dbms, attendance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("CSE001", "Aarav Sharma", "CSE", 3, 82, 91, 78, 92),
                ("CSE002", "Priya Reddy", "CSE", 3, 67, 74, 81, 86),
                ("CSE003", "Rahul Kumar", "CSE", 3, 43, 58, 49, 72),
            ])

def student_stats(row):
    marks = [row["math"], row["python"], row["dbms"]]
    average = round(sum(marks) / len(marks), 1)
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 50:
        grade = "C"
    else:
        grade = "Needs support"
    return average, grade

@app.route("/")
def dashboard():
    with get_db() as conn:
        students = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    records = []
    for s in students:
        avg, grade = student_stats(s)
        records.append({
            "id": s["id"], "student_id": s["student_id"], "name": s["name"],
            "department": s["department"], "semester": s["semester"],
            "math": s["math"], "python": s["python"], "dbms": s["dbms"],
            "attendance": s["attendance"], "average": avg, "grade": grade
        })
    total = len(records)
    overall_average = round(sum(r["average"] for r in records) / total, 1) if total else 0
    attendance_average = round(sum(r["attendance"] for r in records) / total, 1) if total else 0
    support_count = sum(1 for r in records if r["average"] < 50 or r["attendance"] < 75)
    subject_averages = {
        "Mathematics": round(sum(r["math"] for r in records) / total, 1) if total else 0,
        "Python": round(sum(r["python"] for r in records) / total, 1) if total else 0,
        "DBMS": round(sum(r["dbms"] for r in records) / total, 1) if total else 0,
    }
    return render_template("dashboard.html", students=records, total=total,
        overall_average=overall_average, attendance_average=attendance_average,
        support_count=support_count, subject_averages=subject_averages)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            student_id = request.form["student_id"].strip()
            name = request.form["name"].strip()
            department = request.form["department"].strip()
            semester = int(request.form["semester"])
            math = float(request.form["math"])
            python = float(request.form["python"])
            dbms = float(request.form["dbms"])
            attendance = float(request.form["attendance"])
            if not student_id or not name or not department:
                raise ValueError("Please complete all required fields.")
            if not 1 <= semester <= 12:
                raise ValueError("Semester must be between 1 and 12.")
            if any(m < 0 or m > 100 for m in (math, python, dbms)):
                raise ValueError("Marks must be between 0 and 100.")
            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")
            with get_db() as conn:
                conn.execute("""
                    INSERT INTO students
                    (student_id, name, department, semester, math, python, dbms, attendance)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (student_id, name, department, semester, math, python, dbms, attendance))
            flash("Student added successfully.", "success")
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("That student ID already exists. Please use a unique ID.", "error")
        except (ValueError, KeyError):
            flash("Please enter valid details. Marks and attendance must be from 0 to 100.", "error")
    return render_template("add_student.html")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    flash("Student record deleted.", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
