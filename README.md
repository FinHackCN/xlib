# xlib-quant
* 一个简单的量化研究框架，具备基本的数据获取、因子分析、机器学习、回测及结果分析功能。
* 框架具体思路与内容请参考公众号FinHack炼金术《从零开始卷量化(25)-脱离Qlib，手撸一个属于自己的量化投资框架！ 》
* 当且该框架并不稳定，预计本系列文章全部更新完(预计65篇，5月底前更新完)后会出一个稳定版的分支。
# 公众号
![扫码_搜索联合传播样式-标准色版](https://user-images.githubusercontent.com/6196607/162598983-b11b756a-f4fd-4062-9d77-e414e2f072e1.jpg)
# 框架整体思路
<img width="300" alt="image" src="https://user-images.githubusercontent.com/6196607/162599136-2a8286c8-b205-4f43-a894-61c771356920.png">

# 一把梭代码 
    import pandas as pd
    from xlib import data
    from xlib import factors
    from xlib import model
    from xlib.strategies import Top10Strategy
    from xlib import backtest
    
    df=data.get_all_index_data()
    bench=data.get_index_data(index="000300",start_date="20200101",end_date="20220330",renew=False)
    
    df=factors.getTA(df)
    df['label']=df.groupby('symbol')['close'].shift(10)
    df['label']=df['close']/df['label']
    
    df_train,df_valid,df_pred=model.datasplit(df,train_end='2019-01-01',valid_end='2020-01-01')
    model.lgbtrain(df_train,df_valid,label='label')  
    preds=model.lgbpred(df_pred,label='label') 
    preds['score']=preds['pred']
    preds['rank']=preds.groupby('date')['pred'].rank()
    preds['signal']=preds.apply(lambda x: 1 if x['rank']<=10 else 0 ,axis=1)
    
    returns=backtest.test(preds,Top10Strategy)
    backtest.analysis(returns,bench)
    
    
# 结果演示 
<img width="600" alt="image" src="https://user-images.githubusercontent.com/6196607/162584205-8bb34525-4ff0-47c2-8b29-5674af881f29.png">
<img width="600" alt="image" src="https://user-images.githubusercontent.com/6196607/162584222-3ff3f10e-5a07-4621-a9c3-c903a0e8b34f.png">


![image](https://user-images.githubusercontent.com/6196607/162584080-840c668f-524b-4729-9942-cc546456155f.png)
![image](https://user-images.githubusercontent.com/6196607/162584099-dbd51d9a-8e2e-4d5e-abc4-867964d279bc.png)
![image](https://user-images.githubusercontent.com/6196607/162584104-4687f9d6-98a7-4298-abfe-349865ecdd3e.png)
![image](https://user-images.githubusercontent.com/6196607/162584110-ace4df23-ff76-445d-9361-354730f30a89.png)

![image](https://user-images.githubusercontent.com/6196607/162584104-4687f9d6-98a7-4298-abfe-349865ecdd3e.png)
![image](https://user-images.githubusercontent.com/6196607/162584113-f948f488-fb78-4eb7-9bff-8e669c169c7e.png)
![image](https://user-images.githubusercontent.com/6196607/162584140-a63a8134-a432-469b-939f-083dcac43f3c.png)
![image](https://user-images.githubusercontent.com/6196607/162584155-528b7ece-8f97-4b74-bc7e-045d60c7338e.png)
![image](https://user-images.githubusercontent.com/6196607/162584146-f023ec48-6168-4ad5-9f0d-3e36b3fa241f.png)
![image](https://user-images.githubusercontent.com/6196607/162584131-7bf6e0b0-9fc9-40c2-81e1-94ca51a934ff.png)
![image](https://user-images.githubusercontent.com/6196607/162584067-90f96c9c-42b0-43e1-aba6-f81347303866.png)
![image](https://user-images.githubusercontent.com/6196607/162584119-1cdead27-64ae-4ca4-9aab-d154c19a6fbe.png)
![image](https://user-images.githubusercontent.com/6196607/162584127-0294e2c1-cf8c-40a9-a866-0ecad3d2c6ad.png)

