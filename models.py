import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Publisher(Base):

    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))

    books = relationship('Book', back_populates='publisher')

class Book(Base):

    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60))
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.id', ondelete='CASCADE'), nullable=False)

    publisher = relationship(Publisher, back_populates='books')
    stocks = relationship('Stock', back_populates='books')

class Shop(Base):

    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))

    stocks = relationship('Stock', back_populates='shops')

class Stock(Base):

    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.id', ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    books = relationship(Book, back_populates='stocks')
    shops = relationship(Shop, back_populates='stocks')
    sales = relationship('Sale', back_populates='stocks')

class Sale(Base):

    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    date_sale = sq.Column(sq.Date)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stocks = relationship(Stock, back_populates='sales')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

