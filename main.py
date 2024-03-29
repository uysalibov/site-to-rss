from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, sqlite3

from internal.get_template import template
from routers import feed, rss, database

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
app.include_router(database.router)


@app.on_event("startup")
async def startup():
    print("startup başlıyor")
    app.db: sqlite3.Connection = sqlite3.connect("rss.db")
    print(app.db)
    app.cur = app.db.cursor()
    print(app.cur)

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
    app.cur.execute("SELECT * FROM rss")
    feeds = app.cur.fetchall()
    return template().TemplateResponse(
        request=request, name="index.html", context={"feeds": feeds}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, host="0.0.0.0")
