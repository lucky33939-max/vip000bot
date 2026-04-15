# ===== IMPORT =====
import os, time
from html import escape
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from zoneinfo import ZoneInfo
from urllib.parse import urlencode

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
import uvicorn

from db import *

# ===== ENV =====
load_dotenv()
WEB_TOKEN = (os.getenv("WEB_TOKEN") or "").strip()
PORT = int(os.getenv("PORT", "8080"))
BEIJING_TZ = ZoneInfo("Asia/Shanghai")

# ===== APP =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# ===== AUTH =====
def require_token(token):
    if WEB_TOKEN and token != WEB_TOKEN:
        raise HTTPException(401)

# ===== UI CORE =====
def page_shell(title, body):
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>

<style>
body {{
    margin:0;
    font-family:Arial;
    background:#0b1120;
    color:white;
    display:flex;
}}

.sidebar {{
    width:230px;
    background:#020617;
    padding:20px;
}}

.logo {{
    font-size:20px;
    font-weight:bold;
    margin-bottom:20px;
}}

.menu div {{
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    color:#9ca3af;
}}

.menu div:hover {{
    background:#1e293b;
    color:white;
}}

.main {{
    flex:1;
    padding:20px;
}}

.cards {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}}

.card {{
    padding:20px;
    border-radius:16px;
    font-weight:bold;
}}

.c1 {{background:linear-gradient(45deg,#ff6b6b,#ff3b3b);}}
.c2 {{background:linear-gradient(45deg,#3b82f6,#2563eb);}}
.c3 {{background:linear-gradient(45deg,#a855f7,#7c3aed);}}
.c4 {{background:linear-gradient(45deg,#22c55e,#16a34a);}}

.chart {{
    margin-top:30px;
    background:#020617;
    padding:20px;
    border-radius:16px;
}}
</style>
</head>

<body>

<div class="sidebar">
    <div class="logo">🚀 BOT</div>
    <div class="menu">
        <div>Dashboard</div>
        <div>Orders</div>
        <div>Users</div>
        <div>Groups</div>
    </div>
</div>

<div class="main">
{body}
</div>

</body>
</html>
""")

# ===== DASHBOARD =====
@app.get("/dashboard")
def dashboard(token: str | None = Query(None)):
    require_token(token)

    stats = get_dashboard_stats()

    body = f"""
    <h1>Dashboard</h1>

    <div class="cards">
        <div class="card c1">Users<br>{stats["total_users"]}</div>
        <div class="card c2">Active<br>{stats["active_users"]}</div>
        <div class="card c3">Permanent<br>{stats["permanent_users"]}</div>
        <div class="card c4">Orders<br>{stats["pending_orders"]}</div>
    </div>

    <div class="chart">
        <canvas id="chart"></canvas>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'),{{
        type:'bar',
        data:{{
            labels:['Jan','Feb','Mar','Apr'],
            datasets:[{{label:'Orders',data:[10,20,30,40]}}]
        }}
    }})
    </script>
    """

    return page_shell("Dashboard", body)

# ===== USERS =====
@app.get("/users")
def users(token: str | None = Query(None)):
    require_token(token)

    rows = get_access_users_page(limit=50, offset=0)

    html = ""
    for u in rows:
        html += f"<tr><td>{u[0]}</td><td>{u[1]}</td></tr>"

    return page_shell("Users", f"<table>{html}</table>")

# ===== ORDERS (FIX LỖI) =====
@app.get("/orders")
def orders(token: str | None = Query(None)):
    require_token(token)

    rows = get_rental_orders_by_status(None)

    html = ""
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[6]}</td></tr>"

    return page_shell("Orders", f"<table>{html}</table>")

# ===== ROOT =====
@app.get("/")
def home(token: str | None = Query(None)):
    return RedirectResponse("/dashboard")

# ===== RUN =====
if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=PORT)
