import os
from html import escape
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()


def page_shell(title: str, body_html: str):
    return HTMLResponse(f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
:root {{
--bg: linear-gradient(135deg,#020617,#0f172a);
--panel: rgba(17,24,39,.7);
--panel-2: rgba(31,41,55,.7);
--border: rgba(255,255,255,.08);

--text:#e5e7eb;
--muted:#9ca3af;

--blue:#3b82f6;
--green:#22c55e;
--red:#ef4444;
}}

* {{
box-sizing:border-box;
transition:.2s;
}}

body {{
margin:0;
font-family:'Inter',sans-serif;
background:var(--bg);
color:var(--text);
display:flex;
}}

/* SIDEBAR */
.sidebar {{
width:240px;
height:100vh;
position:fixed;
background:rgba(2,6,23,.9);
border-right:1px solid var(--border);
padding:20px;
}}

.logo {{
font-weight:700;
margin-bottom:20px;
}}

.nav a {{
display:block;
padding:10px;
border-radius:10px;
color:var(--muted);
text-decoration:none;
}}

.nav a:hover {{
background:var(--panel-2);
color:white;
}}

/* MAIN */
.main {{
margin-left:240px;
width:100%;
padding:24px;
}}

.container {{
max-width:1200px;
margin:auto;
}}

/* CARD */
.card {{
background:var(--panel);
border-radius:16px;
padding:16px;
border:1px solid var(--border);
}}

.card:hover {{
transform:translateY(-4px);
}}

.value {{
font-size:22px;
font-weight:600;
}}

/* BUTTON */
.btn {{
padding:10px 14px;
border-radius:10px;
border:none;
cursor:pointer;
background:linear-gradient(135deg,#2563eb,#3b82f6);
color:white;
}}

.btn.secondary {{
background:var(--panel-2);
}}

/* TABLE */
table {{
width:100%;
border-collapse:collapse;
margin-top:16px;
}}

td,th {{
padding:12px;
border-bottom:1px solid var(--border);
}}

tr:hover {{
background:rgba(255,255,255,.05);
}}

/* TAG */
.tag {{
padding:4px 10px;
border-radius:999px;
font-size:12px;
}}

.ok {{
background:rgba(34,197,94,.2);
color:#4ade80;
}}

.bad {{
background:rgba(239,68,68,.2);
color:#f87171;
}}

@media(max-width:768px){{
.sidebar{{display:none}}
.main{{margin-left:0}}
}}
</style>
</head>

<body>

<div class="sidebar">
<div class="logo">⚡ Admin</div>
<div class="nav">
<a href="/dashboard">Dashboard</a>
<a href="/users">Users</a>
<a href="/orders">Orders</a>
<a href="/groups">Groups</a>
</div>
</div>

<div class="main">
<div class="container">
{body_html}
</div>
</div>

</body>
</html>
""")


@app.get("/")
def home():
    return RedirectResponse("/dashboard")


@app.get("/dashboard")
def dashboard():
    body = """
    <h1>Dashboard</h1>

    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
        <div class="card"><div class="value">120</div><div>Total Users</div></div>
        <div class="card"><div class="value">87</div><div>Active</div></div>
        <div class="card"><div class="value">12</div><div>Expired</div></div>
        <div class="card"><div class="value">34</div><div>Orders</div></div>
    </div>
    """
    return page_shell("Dashboard", body)


@app.get("/users")
def users():
    body = """
    <h1>Users</h1>

    <table>
    <tr><th>ID</th><th>Name</th><th>Status</th></tr>
    <tr><td>1</td><td>John</td><td><span class="tag ok">Active</span></td></tr>
    <tr><td>2</td><td>Anna</td><td><span class="tag bad">Expired</span></td></tr>
    </table>
    """
    return page_shell("Users", body)


@app.get("/orders")
def orders():
    body = """
    <h1>Orders</h1>

    <table>
    <tr><th>ID</th><th>Amount</th><th>Status</th></tr>
    <tr><td>ORD1</td><td>100</td><td><span class="tag ok">Paid</span></td></tr>
    <tr><td>ORD2</td><td>50</td><td><span class="tag bad">Pending</span></td></tr>
    </table>
    """
    return page_shell("Orders", body)


@app.get("/groups")
def groups():
    body = """
    <h1>Groups</h1>

    <table>
    <tr><th>ID</th><th>Name</th></tr>
    <tr><td>123</td><td>Group A</td></tr>
    <tr><td>456</td><td>Group B</td></tr>
    </table>
    """
    return page_shell("Groups", body)
