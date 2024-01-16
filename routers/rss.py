from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from selectolax.parser import HTMLParser
import json

from routers.feed import fetch
from internal.get_template import template
from internal.get_feed import get_feed

router = APIRouter()


@router.post("/rss")
async def rss_post(request: Request):
    form_data = await request.form()
    if form_data:
        html = await fetch(request=request, url=form_data.get("site"))

        tree = HTMLParser(html.body)
        items = [item for item in tree.css(form_data.get("element"))]

        content = [
            {
                "title": "".join(
                    [tit.text(strip=True) for tit in item.css(form_data.get("title"))]
                ),
                "description": "".join(
                    [
                        desc.text(strip=True)
                        for desc in item.css(form_data.get("description"))
                    ]
                ),
                "date": "".join(
                    [date.text(strip=True) for date in item.css(form_data.get("date"))]
                )
                if form_data.get("date")
                else "",
                "url": item.css_first(form_data.get("url")).attributes.get("href")
                if form_data.get("url")
                else "",
            }
            for item in items
        ]

        return template().TemplateResponse(
            request=request, name="rss.html", context={"content": content}
        )
    else:
        return RedirectResponse("/", status_code=302)
