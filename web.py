import os
import time
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from db import (
    init_db,
    get_transactions,
    get_dashboard_stats
)

# ===== ENV =====
load_dotenv()
PORT = int(os.getenv("PORT", "8080"))

# ===== APP =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# ================= API CHART =================
@app.get("/api/chart")
def chart_data():
    txs = get_transactions()

    daily = {}

    for t in txs:
        ts = t[1]
        amount = t[8] or 0

        day = datetime.fromtimestamp(ts).strftime("%m-%d")
        daily[day] = daily.get(day, 0) + amount

    labels = list(daily.keys())[-7:]
    values = list(daily.values())[-7:]

    return {"labels": labels, "values": values}


# ================= UI =================
def page_shell(title: str, body_html: str):
    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {{
    margin:0;
    font-family:Inter;
    background:#020617;
    color:#e2e8f0;
}}

.layout {{display:flex;}}

.sidebar {{
    width:240px;
    background:#020617;
    padding:20px;
    position:fixed;
    height:100%;
}}

.sidebar a {{
    display:block;
    padding:10px;
    color:#94a3b8;
    text-decoration:none;
}}

.sidebar a:hover {{
    background:#1e293b;
    color:white;
}}

.main {{
    margin-left:240px;
    padding:20px;
    width:100%;
}}

.card {{
    background:#0f172a;
    padding:20px;
    border-radius:12px;
    margin:10px;
}}

.value {{
    font-size:28px;
    font-weight:bold;
}}

.stats {{
    display:flex;
}}

.chart {{
    margin-top:20px;
}}
</style>
</head>

<body>

<div class="layout">

<div class="sidebar">
    <h2>VIP PANEL</h2>
    <a href="/">Dashboard</a>
</div>

<div class="main">

<h1>{title}</h1>

{body_html}

<div class="chart">
<canvas id="chart"></canvas>
</div>

</div>
</div>

<script>
// ===== số chạy =====
document.querySelectorAll(".value").forEach(el=>{
    let target = parseInt(el.getAttribute("data-value"));
    let count = 0;
    let step = target / 40;

    let i = setInterval(()=>{
        count += step;
        if(count >= target){
            count = target;
            clearInterval(i);
        }
        el.innerText = Math.floor(count);
    },20);
});

// ===== chart realtime =====
let chart;

async function loadChart() {
    const res = await fetch("/api/chart");
    const data = await res.json();

    if(chart) {
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.values;
        chart.update();
        return;
    }

    chart = new Chart(document.getElementById('chart'), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                fill:true,
                tension:0.4
            }]
        },
        options: {
            plugins: { legend: { display:false } }
        }
    });
}

loadChart();
setInterval(loadChart, 5000);
</script>

</body>
</html>
"""
    return HTMLResponse(html)


# ================= MAIN PAGE =================
@app.get("/")
def dashboard():
    stats = get_dashboard_stats()

    body = f"""
<div class="stats">

<div class="card">
<div>Total Income</div>
<div class="value" data-value="{int(stats.get('total_income_unit',0))}">0</div>
</div>

<div class="card">
<div>Total Payout</div>
<div class="value" data-value="{int(stats.get('total_payout_unit',0))}">0</div>
</div>

<div class="card">
<div>Users</div>
<div class="value" data-value="{int(stats.get('user_count',0))}">0</div>
</div>

</div>
"""

    return page_shell("Dashboard", body)
