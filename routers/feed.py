from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import requests, json
from selectolax.parser import HTMLParser
from internal.get_template import template

router = APIRouter()


@router.get("/fetch")
async def fetch(request: Request, url: str):
    res = requests.get(
        url, timeout=30, headers={"user-agent": request.headers.get("user-agent")}
    )
    print(res.status_code)
    return HTMLResponse(res.text.replace("<head>", f"<head>\n<base href='{url}' > "))


@router.get("/feed")
async def feed_get(request: Request):
    form_data = request.query_params

    return template().TemplateResponse(
        request=request,
        name="iframe.html",
        context={"url": form_data.get("url")},
    )


@router.post("/feed")
async def feed_post(request: Request):
    form_data = await request.form()

    insert_query = """INSERT INTO rss (url, item, title, description, link, date)
                  VALUES (?, ?, ?, ?, ?, ?)"""
    veri = (
        form_data.get("site"),
        form_data.get("element"),
        form_data.get("title"),
        form_data.get("description"),
        form_data.get("url"),
        form_data.get("date"),
    )

    request.app.cur.execute(insert_query, veri)
    request.app.db.commit()
    return RedirectResponse("/rss")


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
