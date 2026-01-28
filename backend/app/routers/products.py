from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.schemas import (
    ProductResponse, ProductDetailResponse, PriceHistoryResponse,
    ProductWithHistoryResponse, SuccessResponse, PaginatedResponse
)
from app.services.scraping_service import ProductService
from app.models.models import Product

router = APIRouter(prefix="/api/v1/products", tags=["Products"])

def get_current_user_id(authorization: Optional[str] = None) -> int:
    """Dependency to extract user ID from token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    token = authorization.split(" ")[1]
    return verify_token(token)

@router.get("", response_model=SuccessResponse)
async def list_products(
    platform: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """List all products for the current user"""
    user_id = get_current_user_id(authorization)
    
    products = ProductService.get_user_products(db, user_id, platform, skip, limit)
    total = db.query(Product).filter(Product.user_id == user_id).count()
    
    return SuccessResponse(
        success=True,
        message="Products retrieved successfully",
        data=PaginatedResponse(
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            items=[ProductResponse.model_validate(p) for p in products]
        )
    )

@router.get("/{product_id}", response_model=SuccessResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """Get a specific product with details"""
    user_id = get_current_user_id(authorization)
    
    product = ProductService.get_product_by_id(db, product_id, user_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return SuccessResponse(
        success=True,
        message="Product retrieved successfully",
        data=ProductDetailResponse.model_validate(product)
    )

@router.get("/{product_id}/history", response_model=SuccessResponse)
async def get_product_price_history(
    product_id: int,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """Get price history for a product"""
    user_id = get_current_user_id(authorization)
    
    product = ProductService.get_product_by_id(db, product_id, user_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    history = ProductService.get_price_history(db, product_id, user_id, limit)
    
    return SuccessResponse(
        success=True,
        message="Price history retrieved successfully",
        data=[PriceHistoryResponse.model_validate(h) for h in history]
    )

@router.get("/search/{query}", response_model=SuccessResponse)
async def search_products(
    query: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    authorization: Optional[str] = None
):
    """Search products by name or category"""
    user_id = get_current_user_id(authorization)
    
    products = ProductService.search_products(db, user_id, query, skip, limit)
    
    return SuccessResponse(
        success=True,
        message="Products found",
        data=PaginatedResponse(
            total=len(products),
            page=skip // limit + 1,
            page_size=limit,
            items=[ProductResponse.model_validate(p) for p in products]
        )
    )
