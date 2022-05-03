import pyupbit
import numpy as np
#OHLVC(open, high, low, close, volume)가져오기
df = pyupbit.get_ohlcv("KRW-BTC")
#rarnge = 변동폭 
#target = 매수 목표가, 첫날은 전날 변동을 모르기에 shift1
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005

#ror(수익율), np.where(조건문, 참, 거짓)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
# 누적수익율 = 누적 곱의 계산
df['hpr'] = df['ror'].cumprod()

# drawdown(낙폭)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx") 
