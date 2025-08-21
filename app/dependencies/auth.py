import jwt
import os
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # tokenUrl here is just for docs, not used in code
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")
    role = payload.get("role")
    return {"id": user_id, "role": role}
