import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi_jwt import JwtAccessBearer
from jose import jwt


load_dotenv("src/.env")
access_security = JwtAccessBearer(
    secret_key=os.getenv("JWT_SECRET_KEY"),
    auto_error=True,
    algorithm=jwt.ALGORITHMS.HS256,
    access_expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
)
