from pydantic import BaseModel


class Database(BaseModel):
    id: int
    item: str
    title: str
    description: str
    link: str
    date: str
