from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from helpers import engine

Base = declarative_base()

class BudgetMonth(Base):
    __tablename__ = 'budget_month'
    id = Column(Integer, primary_key=True)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('month', 'year', name='_month_year_uc'),)
    categories = relationship('BudgetMonthCategory', backref='budget_month', lazy='dynamic')

    def __repr__(self):
        return f'{self.month} {self.year}'

class BudgetMonthCategory(Base):
    __tablename__ = 'budget_month_category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount_left = Column(String, nullable=False)
    budget_month_id = Column(Integer, ForeignKey('budget_month.id'))
    transactions = relationship('Transaction', backref='budget_month_category', lazy='dynamic')

    def __repr__(self):
        return self.name

class CategoryTemplate(Base):
    __tablename__ = 'budget_category_template'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    amount_budgeted = Column(String, nullable=False)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    budget_category_id = Column(Integer, ForeignKey('budget_month_category.id'))



Base.metadata.create_all(engine)