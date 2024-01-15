from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
from fastapi.responses import HTMLResponse

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


@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/fetch")
async def fetch(request: Request, url: str):
    res = requests.get(
        url, timeout=5, headers={"user-agent": request.headers.get("user-agent")}
    )
    return HTMLResponse(res.text.replace("<head>", f"<head>\n<base href='{url}' > "))


@app.get("/iframe")
async def iframe(request: Request):
    # "https://cupofjo.com/",

    return templates.TemplateResponse(
        request=request,
        name="iframe.html",
        context={"url": "https://plurrrr.com/"},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
