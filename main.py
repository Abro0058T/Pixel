from typing import Union
from routes.user import user
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app=FastAPI()
app.include_router(user)

# 