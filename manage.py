from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(_name_)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database
def init_db():
    conn = sqlite3.connect("projects.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        status TEXT,
        start_date TEXT,
        end_date TEXT,
        location TEXT,
        image TEXT
    )""")

    conn.commit()
    conn.close()

init_db()

# Admin Page
@app.route("/admin", methods=["GET","POST"])
def admin():

    if request.method == "POST":

        title = request.form["title"]
        desc = request.form["description"]
        status = request.form["status"]
        start = request.form["start"]
        end = request.form["end"]
        location = request.form["location"]

        image = request.files["image"]
        image_path = ""

        if image:
            image_path = os.path.join(UPLOAD_FOLDER,image.filename)
            image.save(image_path)

        conn = sqlite3.connect("projects.db")
        c = conn.cursor()

        c.execute("INSERT INTO projects(title,description,status,start_date,end_date,location,image) VALUES(?,?,?,?,?,?,?)",
                  (title,desc,status,start,end,location,image_path))

        conn.commit()
        conn.close()

        return redirect("/projects")

    return render_template_string("""

    <h2>Admin - Manage Projects</h2>

    <form method="POST" enctype="multipart/form-data">

    Project Title <br>
    <input name="title"><br><br>

    Description <br>
    <textarea name="description"></textarea><br><br>

    Status <br>
    <select name="status">
    <option>Ongoing</option>
    <option>Completed</option>
    <option>Upcoming</option>
    </select><br><br>

    Start Date <br>
    <input type="date" name="start"><br><br>

    End Date <br>
    <input type="date" name="end"><br><br>

    Location <br>
    <input name="location"><br><br>

    Upload Image <br>
    <input type="file" name="image"><br><br>

    <button type="submit">Save Project</button>

    </form>

    """)

# Frontend Page
@app.route("/projects")
def projects():

    status = request.args.get("status")

    conn = sqlite3.connect("projects.db")
    c = conn.cursor()

    if status:
        c.execute("SELECT * FROM projects WHERE status=?", (status,))
    else:
        c.execute("SELECT * FROM projects")

    data = c.fetchall()
    conn.close()

    html = """

    <h1>Our Projects</h1>

    <a href="/projects">All</a> |
    <a href="/projects?status=Ongoing">Ongoing</a> |
    <a href="/projects?status=Completed">Completed</a> |
    <a href="/projects?status=Upcoming">Upcoming</a>

    <hr>

    """

    for p in data:

        html += f"""
        <div style="border:1px solid gray;padding:15px;margin:10px">

        <h2>{p[1]}</h2>

        <img src='/{p[7]}' width="200"><br>

        <p>{p[2]}</p>

        <b>Status:</b> {p[3]} <br>
        <b>Location:</b> {p[6]}

        </div>
        """

    return html


if _name_ == "_main_":
    app.run(debug=True)