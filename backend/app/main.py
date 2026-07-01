from fastapi import FastAPI

from app.api.chat_routes import router as chat_router
from app.api.session_routes import router as session_router

app = FastAPI()
app.include_router(session_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "initial test"
    }
