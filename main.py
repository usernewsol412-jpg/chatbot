from fastapi import FastAPI
from webhook import router

app = FastAPI()
app.include_router(router)
