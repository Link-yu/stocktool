import time
import akshare as ak
from datetime import date
from datetime import datetime
from EmailSender import EmailSender
from DingTalkBot import DingTalkBot
from StockInfo import StockInfo
from StockService import StockService

INDICATOR_THRESHOLD = 0.98848

TU_SHARE_TOKEN = "2070e90dd4ee659292dfce6564bffd929d529eebf4364157fbd004d9"

STOCK_CODE_LIST = [
    {"code": "002594", "name": "比亚迪"},
    {"code": "603319", "name": "湘油泵"},
    {"code": "600570", "name": "恒生电子"},
    {"code": "600900", "name": "长江电力"}
]

SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
USERNAME = 'kevinyulk@163.com'
PASSWORD = 'SWaYvNdTKZA4eEtJ'
SENDER = 'kevinyulk@163.com'
RECEIVER = 'yulk48789@hundsun.com'
WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=56e3ea829d8f663fd0f31e057abd089c3f4f92fadfb49f740bdc29e804524033'

email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD)
dingding_robot = DingTalkBot(WEBHOOK_URL)
stock_info = StockInfo()

# 定义数据库连接信息
DATABASE_URL = "mysql+pymysql://root:12345678@127.0.0.1:3306/microsoftrewards"
stock_service = StockService(DATABASE_URL)

def getLastPrice1(code):
    last_price_data = ak.stock_zh_a_hist_pre_min_em(symbol=code, start_time="09:00:00", end_time="15:40:00")
    return last_price_data


def getStockMin(code):
    current_date = date.today().strftime('%Y-%m-%d')
    start_date = current_date + " 09:30:00"
    end_date = current_date + " 15:00:00"
    data = ak.stock_zh_a_hist_min_em(symbol=code, start_date=start_date, end_date=end_date, period="1", adjust="")
    return data


# 获取分时行情信息
def getLastPrice(code):
    stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=code)
    return stock_bid_ask_em_df

# 获取当日成交额
def getDealBalance(code):
    stock_sh = ak.stock_zh_a_spot_em()
    stock_sh_main_board = stock_sh[stock_sh['所属市场'] == '上交所']
    sse_turnover = stock_sh_main_board['成交额'].sum() / 10 ** 8  # 换

def checkPrice(stock_info):
    price_data = getLastPrice(stock_info["code"])
    last_price = price_data['value'][20]
    avg_price = price_data['value'][21]
    stock_service.update_last_price(stock_info["code"], last_price)
    if price_data is None:
        print('不在交易时间')
    else:
        # 确保最新价列存在
        sell_price = avg_price / INDICATOR_THRESHOLD
        buy_price = avg_price * INDICATOR_THRESHOLD
        print("证券 " + stock_info["name"] + "," + "当前价格" + str(last_price) + "," + "均价是" + str(
            avg_price) + "," + "期望卖出价 " + str(
            sell_price) + "," + "期望买入价 " + str(buy_price))
        if last_price > sell_price:
            msg = stock_info["name"] + "," + "价格" + str(last_price) + ", " + "满足指标, 卖出价格" + str(sell_price)
            # email_sender.send_email(SENDER, RECEIVER, stock_info["name"] + "卖出提醒", msg)
            dingding_robot.send_text("股票卖出提醒: " + msg)
            print("满足卖出指标，可以卖出")
        elif last_price < buy_price:
            msg = stock_info["name"] + "," + "价格" + str(last_price) + ", " + "满足指标, 买入价格" + str(buy_price)
            # email_sender.send_email(SENDER, RECEIVER, stock_info["name"] + "买入提醒", msg)
            dingding_robot.send_text("股票买入提醒: " + msg)
            print("满足买入指标，可以买入")
        else:
            print("不满足买入卖出指标，继续等待")


if __name__ == "__main__":
    while True:
        now = datetime.now().time()
        start_time1 = datetime.strptime("09:30:00", "%H:%M:%S").time()
        end_time1 = datetime.strptime("11:30:00", "%H:%M:%S").time()
        start_time2 = datetime.strptime("13:00:00", "%H:%M:%S").time()
        end_time2 = datetime.strptime("15:00:00", "%H:%M:%S").time()

        if now < start_time1 or (end_time1 < now < start_time2):
            print(str(now) + "不在交易时间")
            time.sleep(1 * 60)
            continue
        for stock_info in STOCK_CODE_LIST:
            checkPrice(stock_info)
            print("\n")
        print("等待 1 分钟...")
        print("\n")
        time.sleep(1 * 60)  # 暂停 2 分钟（120 秒）

