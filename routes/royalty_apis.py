import json
from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from services.royalty_service import ( 
get_all_authors_with_balance, 
get_author_with_books_and_balance, 
get_sales_for_author, create_withdrawal, 
get_author_withdrawals,)
from utils.logger import get_logger
from utils.validation import WithdrawalRequest


router = APIRouter()
logger = get_logger("AuthorAPI")

INTERNAL_SERVER_ERROR_MESSAGE = "Internal Server Error"

# ---------------- GET /authors ----------------

@router.get("/authors")
def get_authors(db: Session = Depends(get_db)):
    """
    Returns a list of all authors with:
    id, name, total_earnings, current_balance
    """
    logger.info("GET /authors called")
    try:
        return get_all_authors_with_balance(db)
    except Exception:
        logger.exception("Unexpected error while fetching: {e}")
        raise HTTPException(status_code=500,detail=INTERNAL_SERVER_ERROR_MESSAGE)

# ---------------- GET /authors/{id} ----------------

@router.get("/authors/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    logger.info("GET /authors/author_id called")
    try:
        response = get_author_with_books_and_balance(author_id, db)
        logger.info("Reposne from buisness logic")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Database error while fetching author details: {e}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MESSAGE)

# ---------------- GET /authors/{id}/sales ----------------

@router.get("/authors/{author_id}/sales")
def get_author_sales(author_id: int, db: Session = Depends(get_db)):
    try:
        return get_sales_for_author(author_id, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching sales for author_id={author_id} {e}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MESSAGE)

# ---------------- POST /withdrawals ----------------

@router.post("/withdrawals", status_code=status.HTTP_201_CREATED)
def post_withdrawal(payload: WithdrawalRequest, db: Session = Depends(get_db)):
    logger.info("POST /withdrawals called")
    try:
        author_id = payload.author_id
        amount = payload.amount

        logger.info(f"POST /withdrawals called for author_id={author_id}")
        response = create_withdrawal(author_id, amount, db)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error creating withdrawal for author_id={author_id}: {e}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MESSAGE)

# ---------------- GET /authors/{id}/withdrawals ----------------

@router.get("/authors/{author_id}/withdrawals")
def get_withdrawals(author_id: int, db: Session = Depends(get_db)):
    try:
        
        logger.info(f"GET /authors/{author_id}/withdrawals called")
        withdrawals = get_author_withdrawals(author_id, db)
        logger.info(f"Returning {len(withdrawals)} withdrawals for author_id={author_id}")
        return withdrawals
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in GET /authors/{author_id}/withdrawals: {e}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_MESSAGE)
