import backtrader as bt
from backtrader.feeds import PandasData
from datetime import datetime
import pandas as pd
import quantstats as qs
    
class Addmoredata(PandasData):
    lines = ('score','rank','signal',)
    params = (('score',5),('rank',6),('signal',7),)
    
    
def test(preds,strategy,hold_day=10,cash=1000000):
    columns=['high','low','open','close','volume','score','rank','signal']
    cerebro = bt.Cerebro()
    datas=preds.groupby('symbol')
    df_align=pd.DataFrame()
    print("loading datas...")
    
    for symbol,data in datas: 
        newdata=pd.DataFrame()
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data=data.set_index('date') 
        data=data.fillna(0)
        
        for column in columns:
            newdata[column]=data[column]
        data=Addmoredata(dataname=newdata)
        cerebro.adddata(data,name=str(symbol))   
    
    print("runing backtest...")
    
    cerebro.broker.setcash(cash)
    cerebro.addstrategy(strategy,hold_day=hold_day,hold_n=10)
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name = "TimeReturn")
    results = cerebro.run()
    strat = results[0] 
    returns=pd.Series(strat.analyzers.TimeReturn.get_analysis())
    returns=returns.dropna() 
    portvalue = cerebro.broker.getvalue()
    return returns

    
def analysis(returns,bench):
    myReturns=returns+1
    bench['return']=bench['close'].shift(1)/bench['close']
    benchReturns=bench['return']
    benchReturns.fillna(0)
    
    myReturns=myReturns.cumprod()
    benchReturns=benchReturns.cumprod()
    qs.extend_pandas()
    qs.reports.full(myReturns, benchReturns)