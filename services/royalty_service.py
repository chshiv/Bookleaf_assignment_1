from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.royalty_models import Author, Book, Sale, Withdrawal
from utils.logger import get_logger

logger = get_logger("AuthorService")

def get_all_authors_with_balance(db: Session):
    logger.info("Fetching all authors")
    authors = db.query(Author).all()

    logger.info(f"Total authors found: {len(authors)}")

    if not authors:
        logger.info("No authors found in database")
        return {
            "detail": "No author found",
            "data": []
        }

    result = []
    for author in authors:

        logger.info(f"Calculating balance for author_id={author.id}")

        total_earnings = (
            db.query(
                func.sum(Sale.quantity * Book.royalty_per_sale)
            )
            .join(Book, Sale.book_id == Book.id)
            .filter(Book.author_id == author.id)
            .scalar()
        )

        total_earnings = total_earnings or 0.0

        logger.info(f"Author {author.id} earnings calculated: {total_earnings}")

        # Calculate Withdrawals

        total_withdrawn = (
            db.query(func.sum(Withdrawal.amount))
            .filter(Withdrawal.author_id == author.id)
            .scalar()
        )

        total_withdrawn = total_withdrawn or 0.0

        logger.info(f"Author {author.id} withdrawn amount: {total_withdrawn}")

        # Current Balance

        current_balance = total_earnings - total_withdrawn

        logger.info(
            f"Author {author.id} balance: {current_balance}"
        )

        result.append({
            "id": author.id,
            "name": author.name,
            "total_earnings": round(total_earnings, 2),
            "current_balance": round(current_balance, 2)
        })

    logger.info("Finished processing authors")

    return {
        "detail": "Authors fetched successfully",
        "data": result
    }


def get_author_with_books_and_balance(author_id: int, db: Session):
    logger.info(f"Fetching author_id={author_id}")
    # ---------- Author ----------
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        logger.warning(f"Author not found: {author_id}")
        raise HTTPException(status_code=404, detail="Author not found")

    # ---------- Earnings ----------
    total_earnings = (
        db.query(func.sum(Sale.quantity * Book.royalty_per_sale))
        .join(Book, Sale.book_id == Book.id)
        .filter(Book.author_id == author_id)
        .scalar()
    ) or 0.0

    # ---------- Withdrawals ----------
    total_withdrawals = (
        db.query(func.sum(Withdrawal.amount))
        .filter(Withdrawal.author_id == author_id)
        .scalar()
    ) or 0.0

    current_balance = total_earnings - total_withdrawals

    # ---------- Books ----------
    books = (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .all()
    )

    # ---------- Sales aggregation (ONE query) ----------
    sales_summary = (
        db.query(
            Sale.book_id,
            func.sum(Sale.quantity).label("total_sold")
        )
        .join(Book, Sale.book_id == Book.id)
        .filter(Book.author_id == author_id)
        .group_by(Sale.book_id)
        .all()
    )

    sales_map = {
        sale.book_id: sale.total_sold
        for sale in sales_summary
    }

    books_data = []

    for book in books:
        total_sold = sales_map.get(book.id, 0)
        total_royalty = total_sold * book.royalty_per_sale

        books_data.append({
            "id": book.id,
            "title": book.title,
            "royalty_per_sale": round(book.royalty_per_sale, 2),
            "total_sold": total_sold,
            "total_royalty": round(total_royalty, 2)
        })

    logger.info(f"Author {author_id} fetched successfully")

    return {
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "total_books": len(books_data),
        "total_earnings": round(total_earnings, 2),
        "current_balance": round(current_balance, 2),
        "books": books_data
    }


def get_sales_for_author(author_id: int, db: Session):
    logger.info(f"Fetching sales for author_id={author_id}")

    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        logger.warning(f"Author not found: {author_id}")
        raise HTTPException(status_code=404, detail="Author not found")

    sales = (
        db.query(
            Sale.id,
            Book.title.label("book_title"),
            Sale.quantity,
            (Sale.quantity * Book.royalty_per_sale).label("royalty_earned"),
            Sale.sale_date
        )
        .join(Book, Sale.book_id == Book.id)
        .filter(Book.author_id == author_id)
        .order_by(Sale.sale_date.desc())
        .all()
    )

    sales_list = [
        {
            "book_title": s.book_title,
            "quantity": s.quantity,
            "royalty_earned": round(s.royalty_earned, 2),
            "sale_date": s.sale_date.isoformat()
        }
        for s in sales
    ]

    if not sales_list:
        logger.info(f"No sales found for author_id={author_id}")
        return {
            "detail": "No sales found for this author",
            "data": []
        }

    logger.info(f"Fetched {len(sales_list)} sales for author_id={author_id}")
    return {
        "detail": "Sales fetched successfully",
        "data": sales_list
    }

def create_withdrawal(author_id: int, amount: int, db: Session):
    logger.info(f"Creating withdrawal: author_id={author_id}, amount={amount}")

    # ---------- Check if author exists ----------
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        logger.warning(f"Author not found: {author_id}")
        raise HTTPException(status_code=404, detail="Author not found")
    
    # ---------- Calculate total earnings ----------
    total_earnings = (
        db.query(func.sum(Sale.quantity * Book.royalty_per_sale))
        .join(Book, Sale.book_id == Book.id)
        .filter(Book.author_id == author_id)
        .scalar()
    ) or 0.0

    # ---------- Calculate total withdrawals ----------
    total_withdrawn = (
        db.query(func.sum(Withdrawal.amount))
        .filter(Withdrawal.author_id == author_id)
        .scalar()
    ) or 0.0

    current_balance = total_earnings - total_withdrawn

    logger.info(f"Author {author_id} current_balance={current_balance}")

    if amount > current_balance:
        logger.warning(f"Withdrawal amount exceeds balance: {amount} > {current_balance}")
        raise HTTPException(status_code=400, detail="Withdrawal amount exceeds current balance")

    # ---------- Create withdrawal ----------
    withdrawal = Withdrawal(
        author_id=author_id,
        amount=amount,
        status="pending"
    )
    
    db.add(withdrawal)
    db.commit()
    db.refresh(withdrawal)

    new_balance = current_balance - amount

    logger.info(f"Withdrawal created successfully for author_id={author_id}, new_balance={new_balance}")

    return {
        "id": withdrawal.id,
        "author_id": author_id,
        "amount": round(amount, 2),
        "status": withdrawal.status,
        "new_balance": round(new_balance, 2),
        "created_at": withdrawal.created_at.isoformat()
    }


def get_author_withdrawals(author_id: int, db: Session):
    """
    Fetch all withdrawals for a specific author, sorted by newest first.
    Handles author existence check and logs all steps.
    """
    logger.info(f"Fetching withdrawals for author_id={author_id}")

    # ---------- Check if author exists ----------
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        logger.warning(f"Author not found: {author_id}")
        raise HTTPException(status_code=404, detail="Author not found")

    # ---------- Fetch withdrawals ----------
    withdrawals = (
        db.query(Withdrawal)
        .filter(Withdrawal.author_id == author_id)
        .order_by(Withdrawal.created_at.desc())
        .all()
    )

    if not withdrawals:
        logger.info(f"No withdrawals found for author_id={author_id}")
        return {
            "detail": "No withdrawals found for this author",
            "data": []
        }

    logger.info(f"Found {len(withdrawals)} withdrawals for author_id={author_id}")
    return {
        "detail": "Withdrawals fetched successfully",
        "data": withdrawals
    }