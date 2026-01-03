from fastapi import FastAPI, Request
from core.config import settings
from utils.completion import text_completion_with_tracing
from schemas.completion import CompletionRequest
from utils.rate_limiter import limiter
from utils.constants import constants


app = FastAPI(title=settings.APP_NAME, description=settings.APP_DESCRIPTION, docs_url="/api/docs")


@app.get("/")
async def root(request: Request):
    return {"message": "Hello World"}


@app.post("/completion")
@limiter.limit(constants.ONE_PER_ONE_MINUTE)
async def completion(request: Request, data: CompletionRequest):
    system_prompt = "Please respond to the user's prompt in a friendly and helpful manner."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": data.user_prompt},
    ]
    response = text_completion_with_tracing(messages, data.model)
    return {"response": response.choices[0].message.content}
