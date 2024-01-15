from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, sqlite3


from routers import feed

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=("GET", "POST"),
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

app.include_router(feed.router)


@app.on_event("startup")
async def startup():
    app.db: sqlite3.Connection = sqlite3.connect("rss.db")

    cur = app.db.cursor()

    sql = (
        """CREATE TABLE IF NOT EXISTS rss (url, item, title, description, link, date)"""
    )
    cur.execute(sql)


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/iframe")
async def iframe(request: Request):
    form_data = request.query_params
    print(form_data)

    return templates.TemplateResponse(
        request=request,
        name="iframe.html",
        context={"url": form_data.get("url")},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
