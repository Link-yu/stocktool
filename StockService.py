from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import StockInfo  # 导入包含StockInfo类和相关函数的模块


class StockService:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_all_stocks(self):
        session = self.SessionLocal()
        try:
            stocks = StockInfo.get_all_stocks(session)
            return stocks
        finally:
            session.close()

    def print_all_stocks(self):
        stocks = self.get_all_stocks()
        for stock in stocks:
            print(stock.stock_code, stock.stock_name, stock.last_price)

    def update_last_price(self, stock_code, new_last_price):
        session = self.SessionLocal()
        try:
            StockInfo.update_last_prince(session, stock_code, new_last_price)
        finally:
            session.close()
