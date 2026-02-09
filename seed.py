from datetime import datetime
from sqlalchemy.orm import Session
from models.royalty_models import Author, Book, Sale


def seed_data(db: Session):
    # Check if already seeded
    if db.query(Author).count() > 0:
        print("Database already seeded")
        return

    print("Seeding database...")

    # ---------------- Authors ----------------

    authors_data = [
        {
            "id": 1,
            "name": "Priya Sharma",
            "email": "priya@email.com",
            "bank": "1234567890",
            "ifsc": "HDFC0001234"
        },
        {
            "id": 2,
            "name": "Rahul Verma",
            "email": "rahul@email.com",
            "bank": "0987654321",
            "ifsc": "ICIC0005678"
        },
        {
            "id": 3,
            "name": "Anita Desai",
            "email": "anita@email.com",
            "bank": "5678901234",
            "ifsc": "SBIN0009012"
        }
    ]

    for a in authors_data:
        db.add(Author(**a))

    db.commit()


    # ---------------- Books ----------------

    books_data = [
        {"id": 1, "title": "The Silent River", "author_id": 1, "royalty": 45},
        {"id": 2, "title": "Midnight in Mumbai", "author_id": 1, "royalty": 60},
        {"id": 3, "title": "Code & Coffee", "author_id": 2, "royalty": 75},
        {"id": 4, "title": "Startup Diaries", "author_id": 2, "royalty": 50},
        {"id": 5, "title": "Poetry of Pain", "author_id": 2, "royalty": 30},
        {"id": 6, "title": "Garden of Words", "author_id": 3, "royalty": 40},
    ]

    for b in books_data:

        book = Book(
            id=b["id"],
            title=b["title"],
            author_id=b["author_id"],
            royalty_per_sale=b["royalty"]
        )

        db.add(book)

    db.commit()


    # ---------------- Sales ----------------

    sales_data = [
        {"book_id": 1, "qty": 25, "date": "2025-01-05"},
        {"book_id": 1, "qty": 40, "date": "2025-01-12"},
        {"book_id": 2, "qty": 15, "date": "2025-01-08"},
        {"book_id": 3, "qty": 60, "date": "2025-01-03"},
        {"book_id": 3, "qty": 45, "date": "2025-01-15"},
        {"book_id": 4, "qty": 30, "date": "2025-01-10"},
        {"book_id": 5, "qty": 20, "date": "2025-01-18"},
        {"book_id": 6, "qty": 10, "date": "2025-01-20"},
    ]

    for s in sales_data:

        book = db.query(Book).filter(Book.id == s["book_id"]).first()
        if not book:
            continue

        sale = Sale(
            quantity=s["qty"],
            sale_date=datetime.fromisoformat(s["date"]),
            book_id=book.id,
        )

        db.add(sale)

    db.commit()

    print("Seeding completed successfully")
