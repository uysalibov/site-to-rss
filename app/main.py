from fastapi import FastAPI
import uvicorn

app = FastAPI(debug=True)


@app.get("/")
async def homepage():
    return {"msg": "hello kagi!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
