from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("employee.db")

con = get_db()
con.execute("""
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    salary INTEGER
)
""")
con.commit()
con.close()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Employee Management</title>
</head>
<body>
<h2>Employee Management System</h2>

<form method="POST">
    <input type="text" name="name" placeholder="Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <input type="number" name="salary" placeholder="Salary" required>
    <button type="submit">Add Employee</button>
</form>

<hr>

<h3>Employee List</h3>
<table border="1">
<tr>
<th>ID</th><th>Name</th><th>Email</th><th>Salary</th><th>Action</th>
</tr>
{% for emp in data %}
<tr>
<td>{{emp[0]}}</td>
<td>{{emp[1]}}</td>
<td>{{emp[2]}}</td>
<td>{{emp[3]}}</td>
<td><a href="/delete/{{emp[0]}}">Delete</a></td>
</tr>
{% endfor %}
</table>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    con = get_db()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        salary = request.form["salary"]
        con.execute(
            "INSERT INTO employee (name, email, salary) VALUES (?,?,?)",
            (name, email, salary)
        )
        con.commit()

    data = con.execute("SELECT * FROM employee").fetchall()
    con.close()
    return render_template_string(HTML, data=data)

@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    con.execute("DELETE FROM employee WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
