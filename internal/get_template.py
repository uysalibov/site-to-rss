from fastapi.templating import Jinja2Templates


def template():
    return Jinja2Templates(directory="./templates")
