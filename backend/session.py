import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

sessions = {}

def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"data": {}}
    return session_id

auth_scheme = HTTPBearer(auto_error=False)

def get_session(token: Optional[HTTPAuthorizationCredentials] = Depends(auth_scheme)):
    if token is None:
        # 테스트용 빈 세션 반환
        return {"data": {}}
    
    session_id = token.credentials
    if session_id not in sessions:
        # 존재하지 않는 세션이면 빈 세션 반환 (테스트용)
        return {"data": {}}
        
    return sessions[session_id]