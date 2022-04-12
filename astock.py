# coding=utf-8
import pandas as pd
import sys
import datetime
from pandarallel import pandarallel
sys.path.append("..")
from .mysql import mysql
# 股票信息获取模块
class AStock:

    
    def getStockCodeList(db):
        db,cursor = mysql.getDB(db)
        sql = "select ts_code from astock_basic;";
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            df_code = pd.DataFrame(list(result))
            return df_code
         
        except Exception as e:
            print("MySQL getStockCodeList Error:%s" % str(e))  
            return False
    
    
    def getTableDataByCode(table,ts_code,cursor=None):
        if cursor==None:
            db,cursor = Util.getDB()
        sql="select * from "+table+" where ts_code='%s'"%ts_code

        cursor.execute(sql)
        result = cursor.fetchall()
        df_date = pd.DataFrame(list(result))
        df_date=df_date.reset_index(drop=True)
        return df_date
    

    def getStockDailyPriceByCode(ts_code,db,fq=True):
        db,cursor = mysql.getDB(db)
        df_price=AStock.getTableDataByCode('astock_price_daily',ts_code,cursor)
        df_price.drop_duplicates(subset='trade_date',keep='first',inplace=True)

        if(df_price.empty):
            return df_price
        if fq:
            df_adj = AStock.getTableDataByCode('astock_price_adj_factor',ts_code,cursor)
            
            if(df_adj.empty): 
                adj_factor=1
                df=df_price
                df["adj_factor"]=1
            else:
                adj_factor=float(df_adj.tail(1).adj_factor)
                df = pd.merge(df_price,df_adj,how = 'inner',on=['ts_code', 'trade_date'])

            df["open"]=df["open"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["high"]=df["high"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["low"]=df["low"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["close"]=df["close"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["pre_close"]=df["pre_close"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["change"]=df["change"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["pct_chg"]=df["pct_chg"].astype(float)
            df["vol"]=df["vol"].astype(float)
            df['amount']=df['amount'].astype(float)
            df["vwap"]=(df['amount'].astype(float)*1000)/(df['vol'].astype(float)*100+1) 
            df["prev_close"]=df["pre_close"].astype(float)*df["adj_factor"].astype(float)/adj_factor
            df["returns"]=df["pct_chg"].astype(float)
            df["volume"]=df["vol"].astype(float)
            df_price=df
        db.close()
        return df_price
        
    
    def alignStockFactors(df,table,date,filed,conv=0,db='tushare'):
        #print(df)
        df=df.copy()
        ts_code=df['ts_code'][0]
        if(filed=='*'):
            df_factor=mysql.selectToDf("select * from "+table+" where ts_code='"+ts_code+"'",db)
            filed=mysql.selectToDf("select COLUMN_NAME from information_schema.COLUMNS where table_name = '"+table+"'",db)
            filed=filed['COLUMN_NAME'].tolist()
            filed=",".join(filed)
        else:
            df_factor=mysql.selectToDf("select "+date+","+filed+" from "+table+" where ts_code='"+ts_code+"'",db)
        
        if df_factor.empty:
            df_res=df
            for f in filed.split(','):
                df[f]=0
            return df_res

        if conv==1:
            df_factor[date]=df_factor[date].astype(str)
            df_factor['trade_date']=df_factor[date].map(lambda x: x.replace('-',''))
            
            
        df_res=pd.merge(df, df_factor, how='left', on='trade_date', copy=True, indicator=False)
        
        if conv==2: #不填充
            pass
        else:
            df_res=df_res.fillna(method='bfill')
        return df_res