from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, sqlite3

from internal.get_template import template
from routers import feed, rss

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=("GET", "POST"),
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./static"), name="static")

app.include_router(feed.router)
app.include_router(rss.router)


@app.on_event("startup")
async def startup():
    app.db: sqlite3.Connection = sqlite3.connect("rss.db")

    app.cur = app.db.cursor()

    sql = """CREATE TABLE IF NOT EXISTS rss (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT,
                            item TEXT,
                            title TEXT,
                            description TEXT,
                            link TEXT,
                            date TEXT
                        )"""
    app.cur.execute(sql)


@app.on_event("shutdown")
async def shutdown():
    app.db.close()


@app.get("/")
async def homepage(request: Request):
    return template().TemplateResponse(request=request, name="index.html", context={})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
