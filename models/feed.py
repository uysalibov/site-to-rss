from pydantic import BaseModel


class Feed(BaseModel):
    url: str
