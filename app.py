from flask import Flask, render_template_string, request, redirect, session
import pandas as pd
import json

from ai import generate_ai_email
from analytics import log, get_stats

app = Flask(__name__)
app.secret_key = "secret123"

df = pd.read_csv("data.csv")

# LOAD USERS
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

# LOGIN HTML
LOGIN_HTML = """
<h2>🔐 Login</h2>

<form method="POST">

<input name="username" placeholder="Username"><br><br>

<input type="password" name="password" placeholder="Password"><br><br>

<button type="submit">Login</button>

</form>

<p style='color:red;'>{{error}}</p>
"""

# DASHBOARD HTML
HTML = """
<!DOCTYPE html>
<html>
<head>

<title>AI Email SaaS</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>

<body style="font-family:Arial;text-align:center;">

<h1>🤖 AI EMAIL COMMAND CENTER</h1>

<a href="/logout">Logout</a>

<hr>

<form method="POST">

<select name="name">

{% for n in names %}
<option value="{{n}}">{{n}}</option>
{% endfor %}

</select>

<input name="purpose" placeholder="Enter Purpose">

<button type="submit">
Generate AI Email
</button>

</form>

{% if email %}

<h3>📧 Generated Email</h3>

<pre style="text-align:left;background:#eee;padding:10px;">
{{email}}
</pre>

{% endif %}

<hr>

<h2>👥 Contacts</h2>

<table border="1" style="margin:auto;">

<tr>
<th>Name</th>
<th>Email</th>
</tr>

{% for i in rows %}

<tr>
<td>{{i[0]}}</td>
<td>{{i[1]}}</td>
</tr>

{% endfor %}

</table>

<hr>

<h2>📊 Analytics Dashboard</h2>

<div style="width:600px;margin:auto;">
<canvas id="barChart"></canvas>
</div>

<br>

<div style="width:400px;margin:auto;">
<canvas id="pieChart"></canvas>
</div>

<script>

const sent = {{sent}};
const failed = {{failed}};

new Chart(document.getElementById("barChart"), {

type:"bar",

data:{
labels:["Sent","Failed"],

datasets:[{
label:"Emails",
data:[sent, failed],
backgroundColor:["green","red"]
}]
}

});

new Chart(document.getElementById("pieChart"), {

type:"pie",

data:{
labels:["Sent","Failed"],

datasets:[{
data:[sent, failed],
backgroundColor:["green","red"]
}]
}

});

</script>

</body>
</html>
"""

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    error = None
    users = load_users()

    if request.method == "POST":

        u = request.form["username"]
        p = request.form["password"]

        if u in users and users[u]["password"] == p:
            session["user"] = u
            return redirect("/")
        else:
            error = "Invalid Login"

    return render_template_string(LOGIN_HTML, error=error)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# HOME
@app.route("/", methods=["GET","POST"])
def home():

    if "user" not in session:
        return redirect("/login")

    email = None

    if request.method == "POST":

        name = request.form["name"]
        purpose = request.form["purpose"]

        email = generate_ai_email(name, purpose)

        log("sent")

    stats = get_stats()

    return render_template_string(
        HTML,
        names=df["name"].tolist(),
        rows=df.values,
        email=email,
        sent=stats["sent"],
        failed=stats["failed"]
    )

if__name__ == "__main__":
    app.run(debug=True)
   
   