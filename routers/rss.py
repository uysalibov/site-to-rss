from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from selectolax.parser import HTMLParser
import requests
from datetime import datetime
from xml.etree import ElementTree as et
from routers.feed import fetch
from internal.get_template import template
from internal.get_feed import get_all_feeds


class XMLResponse(Response):
    media_type = "text/xml"


router = APIRouter()


@router.get("/rss")
async def rss_get(request: Request):
    feeds = get_all_feeds(request.app.cur)
    parsed = {}
    for feed in feeds:
        res = requests.get(
            feed[1],
            timeout=30,
            headers={"user-agent": request.headers.get("user-agent")},
        )
        if res.status_code == 200:
            tree = HTMLParser(res.content)
            items = tree.css(feed[2])
            parsed[feed[1]] = []
            for item in items:
                temp = {
                    "title": item.css_first(feed[3]),
                    "desc": item.css_first(feed[4]),
                    "link": item.css_first(feed[5]).attributes.get("href")
                    if feed[5]
                    else None,
                    "date": item.css_first(feed[6]) if feed[6] else None,
                }
                if temp["title"]:
                    temp["title"] = temp["title"].text(strip=True)
                if temp["desc"]:
                    temp["desc"] = temp["desc"].text(strip=True)
                if temp["date"]:
                    temp["date"] = temp["date"].text(strip=True)

                parsed[feed[1]].append(temp)

    rss = et.Element("rss")
    rss.set("version", "2.0")

    for parse in parsed.items():
        channel = et.Element("channel")
        rss.append(channel)

        title = et.SubElement(channel, "title")
        title.text = parse[0]
        description = et.SubElement(channel, "description")
        description.text = "Channel items of " + parse[0]
        link = et.SubElement(channel, "link")
        link.text = parse[0]

        for item in parse[1]:
            xitem = et.Element("item")
            channel.append(xitem)

            title = et.SubElement(xitem, "title")
            title.text = item["title"]

            description = et.SubElement(xitem, "description")
            description.text = item["desc"]

            link = et.SubElement(xitem, "link")
            link.text = item["link"]

            date = et.SubElement(xitem, "date")
            date.text = item["date"]

    return XMLResponse(et.tostring(rss))


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
