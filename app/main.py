from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from typing import List

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Helper function to query the database
def query_sales(categories: List[str] = None):
    conn = sqlite3.connect("data/sales.db")
    cursor = conn.cursor()
    if categories and categories != ["all"]:
        # Use parameterized query to prevent SQL injection
        placeholders = ",".join("?" for _ in categories)
        cursor.execute(f"SELECT category, value FROM sales WHERE category IN ({placeholders})", categories)
    else:
        cursor.execute("SELECT category, value FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return {"categories": [row[0] for row in rows], "values": [row[1] for row in rows]}

# Endpoint to get all categories for the dropdown
@app.get("/api/categories")
async def get_categories():
    conn = sqlite3.connect("data/sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM sales")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"categories": categories}

# Endpoint to get filtered sales data
@app.get("/api/data")
async def get_data(categories: List[str] = Query(default=["all"])):
    return query_sales(categories)

# Serve the frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})