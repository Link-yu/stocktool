import time
import akshare as ak
from datetime import date

from EmailSender import EmailSender

INDICATOR_THRESHOLD = 0.98848

STOCK_CODE_LIST = [
    {"code": "002594", "name": "比亚迪"},
    {"code": "603319", "name": "湘油泵"},
    {"code": "600570", "name": "恒生电子"}
]

SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
USERNAME = 'kevinyulk@163.com'
PASSWORD = 'SWaYvNdTKZA4eEtJ'
SENDER = 'kevinyulk@163.com'
RECEIVER = 'yulk48789@hundsun.com'

email_sender = EmailSender(SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD)


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


def checkPrice(stock_info):
    price_data = getLastPrice(stock_info["code"])
    last_price = price_data['value'][20]
    avg_price = price_data['value'][21]
    if price_data is None:
        print('不在交易时间')
    else:
        # 确保最新价列存在
        sell_price = avg_price / INDICATOR_THRESHOLD
        buy_price = avg_price * INDICATOR_THRESHOLD
        print("证券 " + stock_info["name"] + "," + "当前价格" + str(last_price) + "," + "均价是" + str(avg_price) + "," + "期望卖出价 " + str(
                sell_price) + "," + "期望买入价 " + str(buy_price))
        if last_price > sell_price:
            msg = stock_info["name"] + "," + "价格" + str(last_price) + "," + "满足指标，现在价格" + str(sell_price)
            email_sender.send_email(SENDER, RECEIVER, stock_info["name"] + "卖出提醒", msg)
            print("满足卖出指标，可以卖出")
        elif last_price < buy_price:
            msg = stock_info["name"] + "," + "价格" + str(last_price) + "," + "满足指标，现在价格" + str(buy_price)
            email_sender.send_email(SENDER, RECEIVER, stock_info["name"] + "买出提醒", msg)
            print("满足买入指标，可以买入")
        else:
            print("不满足买入卖出指标，继续等待")


if __name__ == "__main__":
    while True:
        for stock_info in STOCK_CODE_LIST:
            checkPrice(stock_info)
            print("\n")
        print("等待 1 分钟...")
        print("\n")
        time.sleep(1 * 60)  # 暂停 2 分钟（120 秒）

