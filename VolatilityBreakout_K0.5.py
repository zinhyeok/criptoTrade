import time
import pytz
import pyupbit
import datetime


f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
    return current_price

# 로그인
tickers = pyupbit.get_tickers(fiat="KRW")
KST = pytz.timezone('Asia/Seoul')
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
fee = 0.0005
# 자동매매 시작
target_price = get_target_price("KRW-BTC", 0.5)

while True:
    try:
        now = datetime.datetime.now(KST)
        start_time = datetime.datetime(now.year, now.month, now.day, 9, 00, 00)
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*(1-fee))
        else:
            try:
                target_price = get_target_price("KRW-BTC", 0.5)
                btc = get_balance("BTC")
            except:
                print("error")
            finally:
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*(1-fee))
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)