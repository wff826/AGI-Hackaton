import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

sessions = {}

def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"data": {}}
    return session_id

def get_session(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    session_id = token.credentials
    if session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return sessions[session_id]