import time
import pytz
import pyupbit
import datetime
import pandas as pd
from numpy import NaN, absolute

f = open("upbit.txt")
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    try:
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        target_price = df.iloc[0]["close"] + (df.iloc[0]["high"] - df.iloc[0]["low"]) * k

    except:
        target_price = NaN

    return target_price

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

def get_sort50(tickers):
    """거래량 상위 50개 list 출력"""
    df = pd.DataFrame()
    for ticker in tickers:
        try:
            temp = pyupbit.get_ohlcv(ticker, interval="day", count=1)
            temp["ticker"] = ticker
            df = pd.concat([df, temp])
        except:
            pass
    # 결측치 데이터 삭제
    df.dropna(inplace=True)
    df_sort_top50 = df.sort_values(by='volume', ascending=False).groupby(
        'ticker', sort=False).head(50)
    sort_coin50 = df_sort_top50['ticker'].values.tolist()
    return sort_coin50

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
fee = 0.0005


# 자동매매 시작
KST = pytz.timezone('Asia/Seoul')
tickers = pyupbit.get_tickers(fiat="KRW")
sortedCoin50 = get_sort50(tickers)


while True:
    try:
        now = datetime.datetime.now(KST)
        start_time = datetime.datetime(now.year, now.month, now.day, 9, 00, 00)
        end_time = start_time + datetime.timedelta(days=1)
        start_time = KST.localize(start_time)
        end_time = KST.localize(end_time)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            dicts_targetprice = {}
            for ticker in sortedCoin50:
                dicts_targetprice[ticker] = get_target_price(ticker, 0.5)
            print(dicts_targetprice)
        #     for ticker in sortedCoin50:
        #     time.sleep(0.2)
        #     for ticker in sortedCoin50:
        #         target_price = get_target_price(ticker, 0.5)
        #         current_price = get_current_price(ticker)
        #         if target_price < current_price:
        #             krw = get_balance("KRW")
        #             if krw > 5000:
        #                 upbit.buy_market_order("KRW-BTC", krw*(1-fee))
        # else:
        #     try:
        #         target_price = get_target_price("KRW-BTC", 0.5)
        #         btc = get_balance("BTC")
        #     except:
        #         print("error")
        #     finally:
        #         if btc > 0.00008:
        #             upbit.sell_market_order("KRW-BTC", btc*(1-fee))
        #     time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)