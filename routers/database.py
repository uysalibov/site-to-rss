from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from internal.get_feed import get_feed
from internal.update_feed import update_feed
from internal.delete_feed import delete_feed
from models.database import Database

router = APIRouter()


@router.get("/database")
async def database_get(request: Request, id: int):
    return {"data": get_feed(request.app.cur, id)}


@router.post("/database")
async def database_post(request: Request, data: Database):
    update_feed(conn=request.app.db, values=data)
    return JSONResponse({"msg": "Updated successfully!"})


@router.delete("/database")
async def database_delete(request: Request, id: int):
    delete_feed(request.app.db, id)
    return JSONResponse({"msg": "Deleted successfully!"})
