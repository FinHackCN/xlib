import tushare as ts
import pandas as pd
from datetime import datetime 
pro = ts.pro_api()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def getbalance_yearly(ts_code='002624.sz',balance_kv={},priod=5):
    df_all=pd.DataFrame()
    for i in range(0,priod+1):
        year=datetime.now().year-i
        key='Y'+str(year)
        df = pro.balancesheet(ts_code='002624.sz',fields=",".join(balance_kv.keys()),period=str(year)+'1231')
        
        if(df.empty):
            continue
            
        df = df.stack()
        df=pd.DataFrame(df[0])
        df['v']=df[0]
        df.columns=["key",key]
        df['key']=df.index
        df['key']=df.apply(lambda x:balance_kv[x.key] if x.key in balance_kv else x.key ,axis = 1)
        df[key]=df.apply(lambda x:str(round(int(x[key])/100000000,2))+"亿" if isinstance(x[key],float) else x[key],axis = 1)
    
        if df_all.empty:
            df_all=df
        else:
            df_all['Y'+str(year)]=df['Y'+str(year)]
            
    df_all=df_all.style.applymap(markblod).set_caption('<h3>完美世界(002624.sz)-资产负债表</h3>').hide()
        
    return df_all



def markblod(x):
    blod_key=[]     
    return 'color : red;font-weight:700' if x in blod_key else ''

