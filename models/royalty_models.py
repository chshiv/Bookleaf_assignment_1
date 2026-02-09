from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    bank = Column(String)
    ifsc = Column(String)
    books = relationship("Book", back_populates="author")
    withdrawals = relationship("Withdrawal", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    royalty_per_sale = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    sale_date = Column(DateTime)
    book_id = Column(Integer, ForeignKey("books.id"))

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="withdrawals")