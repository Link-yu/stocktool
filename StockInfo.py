from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

# 创建基本映射类
Base = declarative_base()


# 定义StockInfo类
class StockInfo(Base):
    __tablename__ = 'stockinfo'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    stock_code = Column(String(255), nullable=True, comment='证券名称')
    stock_name = Column(String(255), nullable=True, comment='证券代码')
    last_price = Column(Float, nullable=True, comment='最新价')
    curr_date = Column(Date, nullable=True, comment='日期')


# 查询方法
def get_stock_by_code(session, stock_code):
    return session.query(StockInfo).filter(StockInfo.stock_code == stock_code).first()


def get_all_stocks(session):
    return session.query(StockInfo).all()


def add_stock(session, stock_code, stock_name):
    new_stock = StockInfo(stock_code=stock_code, stock_name=stock_name)
    session.add(new_stock)
    session.commit()
    return new_stock


def update_stock_name(session, stock_code, new_stock_name):
    stock = session.query(StockInfo).filter(StockInfo.stock_code == stock_code).first()
    if stock:
        stock.stock_name = new_stock_name
        session.commit()
    return stock


def update_last_prince(session, stock_code, new_last_price):
    stock = session.query(StockInfo).filter(StockInfo.stock_code == stock_code).first()
    if stock:
        stock.last_price = new_last_price
        stock.curr_date = date.today()
        session.commit()
    return stock


def delete_stock(session, stock_code):
    stock = session.query(StockInfo).filter(StockInfo.stock_code == stock_code).first()
    if stock:
        session.delete(stock)
        session.commit()
    return stock
