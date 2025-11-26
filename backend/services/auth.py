import os
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

# Supabase uses HS256 by default for signing tokens
ALGORITHM = "HS256"

security = HTTPBearer()

def get_supabase_jwt_secret():
    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        # Fallback for development if not set, but ideally should be in .env
        # This allows the app to start even if the secret is missing, 
        # but auth will fail if real tokens are sent.
        print("WARNING: SUPABASE_JWT_SECRET not set in .env")
        return "your-super-secret-jwt-token-with-at-least-32-characters-long"
    return secret

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Verifies the Supabase JWT token and returns the user ID (sub).
    """
    token = credentials.credentials
    secret = get_supabase_jwt_secret()
    
    try:
        # Decode the token
        # verify_aud=False because Supabase tokens might have 'authenticated' as audience 
        # but we mainly care about the signature and 'sub'
        payload = jwt.decode(
            token, 
            secret, 
            algorithms=[ALGORITHM],
            options={"verify_aud": False} 
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID (sub)",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return user_id
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Auth error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
