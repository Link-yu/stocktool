from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 定义数据库连接信息
DATABASE_URL = "mysql+pymysql://username:password@hostname/dbname"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本映射类
Base = declarative_base()

# 定义StockInfo类
class StockInfo(Base):
    __tablename__ = 'stockinfo'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    stock_code = Column(String(255), nullable=True, comment='证券名称')
    stock_name = Column(String(255), nullable=True, comment='证券代码')

# 初始化数据库（如果表还不存在，将创建表）
Base.metadata.create_all(bind=engine)

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

def delete_stock(session, stock_code):
    stock = session.query(StockInfo).filter(StockInfo.stock_code == stock_code).first()
    if stock:
        session.delete(stock)
        session.commit()
    return stock

# 使用示例
if __name__ == "__main__":
    # 创建一个会话
    session = SessionLocal()

    # 添加一个新的股票信息
    add_stock(session, "000001", "平安银行")

    # 查询一个股票信息
    stock = get_stock_by_code(session, "000001")
    print(stock.stock_name)

    # 更新股票名称
    update_stock_name(session, "000001", "平安银行股份有限公司")

    # 查询所有股票信息
    stocks = get_all_stocks(session)
    for stock in stocks:
        print(stock.stock_code, stock.stock_name)

    # 删除一个股票信息
    delete_stock(session, "000001")

    # 关闭会话
    session.close()
