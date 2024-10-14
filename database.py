# pylint: disable=too-few-public-methods, broad-exception-caught, no-member
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
        self.__insert_initial_categories()

    def __insert_initial_categories(self):
        """
        Creates records in the categories table
        """
        session = self.get_session()

        predefined_categories = [
            "Salario",
            "Bolsa de Estudos",
            "Network Sharing",
            "Ebay/Vendas",
            "Depositos",
            "Creditos",
            "MB Way",
            "Alimentacao",
            "Combustivel",
            "Via Verde",
            "Seguro",
            "Prestacao Veiculo",
            "Despesas Veiculo",
            "Transportes",
            "Rendas/Estadia",
            "Viagens",
            "Vodafone",
            "Google Drive",
            "Lazer",
            "Roupa",
            "Compras",
            "Saude",
            "Beleza",
            "Levantamentos",
            "Ginasio",
            "Universidade",
            "Outros"
        ]

        try:
            if not session.query(Category).first(): # If just created
                # Insert default categories in db
                categories = [Category(category=cat) for cat in predefined_categories]
                session.add_all(categories)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error inserting predefined categories: {e}")
        finally:
            session.close()

    def get_session(self):
        """
        Returns the database session
        """
        session = sessionmaker(bind=self.engine)
        return session

db = Database()
