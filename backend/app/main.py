from fastapi import FastAPI


app = FastAPI(title="InteractiveLabs API", description="API for the InteractiveLabs", docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}