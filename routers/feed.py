from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
import requests
from selectolax.parser import HTMLParser

from models.feed import Feed

router = APIRouter()


@router.get("/feed")
async def feed_get(request: Request, url: str):
    return {"asdad": "adasd"}


@router.post("/feed")
async def feed_post(request: Request, url: str = Form()):
    return RedirectResponse("iframe")


@router.post("/auto")
async def auto_post(request: Request, url: str = Form()):
    user_agent = request.headers.get("user-agent")

    if not user_agent:
        user_agent = ""
    req = requests.get(url=url, headers={"user-agent": user_agent}, timeout=10)
    if req.status_code != 200:
        return JSONResponse("Site cannot fetched!", 404)

    tree = HTMLParser(req.content)
    articles = [element for element in tree.css("article")]
    if articles:
        headings = [element.css_first("header") for element in articles]
        print(headings)

        return JSONResponse(
            {
                "count": len(articles),
                "articles": [
                    {
                        "title": art.css_first("a").text(strip=True),
                        "description": art.css_first("p").text(strip=True),
                        "url": art.css_first("a").attributes.get("href"),
                        "image": art.css_first("img").attributes.get("src")
                        if art.css_first("img")
                        else None,
                    }
                    for art in articles
                ],
            }
        )

    return {"req": "asda", "headers": request.headers.get("user-agent")}
