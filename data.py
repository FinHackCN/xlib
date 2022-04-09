import os
import akshare as ak
import pandas as pd


def get_index_data(index="000300",start_date="20150101",end_date="20220330",renew=False):
    idx_cache_file=os.path.dirname(os.path.realpath(__file__))+'/cache/'+"i_"+index+"_"+start_date+"_"+end_date+".csv"
    if renew or not os.path.exists(idx_cache_file):
        idx_data = ak.index_zh_a_hist(symbol=index, period="daily", start_date=start_date, end_date=end_date)    
        idx_data.rename(columns={'日期':'date', '开盘':'open', '收盘':'close', 
                           '最高':'high', '最低':'low', '成交量':'volume',
                           '成交额':'amount', '振幅':'swing', '涨跌幅':'chg_pct',
                           '涨跌额':'chg_amount', '换手率':'turnover',
                          }, inplace = True)
        #idx_data['date'] = pd.to_datetime(idx_data['date'], format='%Y-%m-%d')
        idx_data.drop_duplicates(subset=['date'],keep='first',inplace=True)
        idx_data.to_csv(idx_cache_file)
    else:
        idx_data=pd.read_csv(idx_cache_file,index_col=0)
    idx_data['date'] = pd.to_datetime(idx_data['date'], format='%Y-%m-%d')
    idx_data=idx_data.set_index('date')
    return idx_data

def get_all_index_data(index="000300",start_date="20150101",end_date="20220330",renew=False):
    idx_cache_file=os.path.dirname(os.path.realpath(__file__))+'/cache/'+"i_"+index+"_"+start_date+"_"+end_date+".csv"
    if renew or not os.path.exists(idx_cache_file):
        idx_data = ak.index_zh_a_hist(symbol=index, period="daily", start_date=start_date, end_date=end_date)    
        idx_data.rename(columns={'日期':'date', '开盘':'open', '收盘':'close', 
                           '最高':'high', '最低':'low', '成交量':'volume',
                           '成交额':'amount', '振幅':'swing', '涨跌幅':'chg_pct',
                           '涨跌额':'chg_amount', '换手率':'turnover',
                          }, inplace = True)
        #idx_data['date'] = pd.to_datetime(idx_data['date'], format='%Y-%m-%d')
        idx_data.drop_duplicates(subset=['date'],keep='first',inplace=True)
        idx_data.to_csv(idx_cache_file)
    else:
        idx_data=pd.read_csv(idx_cache_file,index_col=0)

    
    df_align=idx_data['date']

    all_index_data=pd.DataFrame()
    index_stock_cons_df = ak.index_stock_cons(symbol=index)
    idx_all_cache_file=os.path.dirname(os.path.realpath(__file__))+'/cache/'+"i_all_"+index+"_"+start_date+"_"+end_date+".csv"
    if renew or not os.path.exists(idx_all_cache_file):
        symbol_list=index_stock_cons_df['品种代码'].tolist()
        for symbol in symbol_list:
            cache_file=os.path.dirname(os.path.realpath(__file__))+'/cache/'+symbol+"_"+start_date+"_"+end_date+".csv"
            exists=os.path.exists(cache_file)
            if(renew or not exists):
                df=ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, adjust="qfq")
                df.rename(columns={'日期':'date', '开盘':'open', '收盘':'close', 
                                  '最高':'high', '最低':'low', '成交量':'volume',
                                  '成交额':'amount', '振幅':'swing', '涨跌幅':'chg_pct',
                                  '涨跌额':'chg_amount', '换手率':'turnover',
                                  }, inplace = True)
                #df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
                df['factor']=1
                
                
                df.drop_duplicates(subset=['date'],keep='first',inplace=True)
                df=pd.merge(df_align,df,on=['date'],how='outer', validate="one_to_many")
                df['symbol']='x'+str(symbol)
                df=df.fillna(0)
                df.to_csv(cache_file)
                
                print(len(df))

            else:
                df=pd.read_csv(cache_file,index_col=0)

            if all_index_data.empty:
                all_index_data=df
            else:
                 all_index_data=all_index_data.append(df)
        all_index_data=all_index_data.reset_index(drop=True)
        all_index_data.to_csv(idx_all_cache_file)
    else:
        all_index_data=pd.read_csv(idx_all_cache_file,index_col=0)
    return  all_index_data
    

