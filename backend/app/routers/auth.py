from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from app.schemas.schemas import LoginRequest, TokenResponse, UserResponse, SuccessResponse
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# Hardcoded user for demo (replace with real user lookup in production)
DEMO_USER = {
    "id": 1,
    "email": "demo@scrapper.com",
    "username": "demo_user",
    "full_name": "Demo User",
    "role": "user",
    "is_active": True,
    "is_verified": True,
    "avatar_url": None
}

@router.post("/login", response_model=SuccessResponse)
async def login(credentials: LoginRequest):
    """Login endpoint"""
    # Demo authentication - replace with real database lookup
    if credentials.email == DEMO_USER["email"] and credentials.password == "demo123":
        access_token = create_access_token(
            data={"sub": DEMO_USER["id"]},
            expires_delta=timedelta(minutes=30)
        )
        
        user_response = UserResponse(**DEMO_USER)
        token_response = TokenResponse(
            access_token=access_token,
            user=user_response
        )
        
        return SuccessResponse(
            success=True,
            message="Login successful",
            data=token_response
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@router.get("/me", response_model=SuccessResponse)
async def get_current_user(authorization: str = None):
    """Get current user info"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Demo: return hardcoded user
    user_response = UserResponse(**DEMO_USER)
    return SuccessResponse(
        success=True,
        message="User retrieved successfully",
        data=user_response
    )
