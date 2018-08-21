##tradeBotβ版

###必要なライブラリーのインス

from coinex.coinex import CoinEx
import requests
import json
import pandas as pd
import numpy as np
import time
import datetime



##自分の公開鍵と秘密鍵をセット

public=''
SecretKey=''

coinex = CoinEx(public, SecretKey)

##価格を取得する関数


##CETの価格を取得する関数

def get_cet_price():
    
    ##URLにアクセス
    
    tick=requests.get('https://api.coinex.com/v1/market/ticker?market=CETBCH')
    
    ##jsonの見れるようにする
    cet_tick=json.loads(tick.text)
    data=cet_tick['data']
    ticker=data['ticker']
    cet_price=ticker['open']
        
    return cet_price




##上の関数で作ったリストをデータフレームにする


cetprice_list=[]
sma5_list=[]
sma25_list=[]
signal=True
cet_amount=1



##ライブラリーの読込とTwitterAPI鍵の設定

from requests_oauthlib import OAuth1Session
import json

CK = ''                             # Consumer Key
CS = ''     # Consumer Secret
AT = '' # Access Token
AS = ''         # Accesss Token Secert


# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)





##BOT本体

for i in range(1440):
    
    
    ##CETの価格を取得する
    a=get_cet_price()
    cetprice_list.append(a)
    Cet_PriceData=pd.Series(cetprice_list)
    
    
    ##5分・25分の二つの移動平均を計算する
    sma25=Cet_PriceData.rolling(5).mean()
    sma75=Cet_PriceData.rolling(25).mean()
    
    
    
    ##最新の移動平均を抽出する
    new=len(sma25)
    new2=len(sma75)
    
    
    ##注文の状態を確認
    order=coinex.order_pending('CETBCH')
    
    
    
    ##注文があるかどうかを確認
    if order['has_next']:
        print("注文が残っています")
    
    
    else:
        if signal:
            if sma25[new-1]<sma75[new2-1]:
                buy=coinex.order_market('CETBCH', 'buy', 0.05) ##買い注文の発注
                cet_amount=buy['deal_amount']
                signal=False
                d = datetime.datetime.today()
                balance=coinex.balance()
                bch=balance['BCH']
                tweet='@tos'+'\r\n'+str(d.strftime("%Y-%m-%d %H:%M:%S"))+'CETを買いました'+str(bch['available'])
                params = {"status":tweet}
                req = twitter.post(url, params = params)
                print(d.strftime("%Y-%m-%d %H:%M:%S"),'CETを買いました',bch['available'])
        else:
            if sma25[new-1]>sma75[new2-1]:
                coinex.order_market('CETBCH', 'sell',cet_amount)
                signal=True
                d = datetime.datetime.today()
                balance=coinex.balance()
                bch=balance['BCH']
                tweet='@tos'+'\r\n'+str(d.strftime("%Y-%m-%d %H:%M:%S"))+'CETを売りました'+str(bch['available'])
                params = {"status":tweet}
                req = twitter.post(url, params = params)
                print(d.strftime("%Y-%m-%d %H:%M:%S"),'CETを売りました',bch['available'])
                
        time.sleep(60)

            
            