# pylint: disable=too-few-public-methods
"""
Provides the database schema, handles entity creation and record management
"""

from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Expense(Base):
    """
    Represents an expense
    """

    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    description = Column(String)
    value = Column(DECIMAL)
    category_id = Column(Integer, ForeignKey('category.id'))

class Category(Base):
    """
    Represents an expense category
    """

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, unique=True)

class Database:
    """
    Represents and manages the database engine connection
    """

    def __init__(self, uri='sqlite:///expense.db'):
        self.engine = create_engine(uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        """
        Returns the database session
        """

        return self.session()

db = Database()
