from sqlalchemy import Column, Integer, String, UniqueConstraint
from models import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AddExtraIncomeColumn(Base):
    __tablename__ = 'budget_month'
    id = Column(Integer, primary_key=True)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('month', 'year', name='_month_year_uc'),)
    categories = relationship('BudgetMonthCategory', backref='budget_month', lazy='dynamic')
    extra_income = Column(String, nullable=True)


    def __repr__(self):
        return f'{self.month} {self.year}'


with engine.connect() as conn:
    conn.execute(AddExtraIncomeColumn.__table__.update().values(extra_income=None))