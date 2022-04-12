import lightgbm as lgb
#from datetime import datetime
<<<<<<< HEAD
from math import e
import numpy as np

def datasplit(df,train_end='2019-01-01',valid_end='2020-01-01'):
    #df=df.dropna()
    df_train=df[df['date']<train_end]
    df_valid=df[df['date']>train_end]
    df_valid=df_valid[df_valid['date']<valid_end]   
    
    df_pred=df[df['date']>=valid_end]
=======


def datasplit(df,train_end='2019-01-01',valid_end='2020-01-01'):
    #df=df.dropna()
    df_train=df[df.date<train_end]
    df_valid=df[df.date>train_end]
    df_valid=df_valid[df_valid.date<valid_end]   
    
    df_pred=df[df.date>=valid_end]
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53
    
    df_train.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)
    df_valid.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)
    df_pred.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)

<<<<<<< HEAD
    return df_train,df_valid,df_pred
    
 
=======


    
    return df_train,df_valid,df_pred
    
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53

def lgbtrain(df_train,df_valid,label='label'):

    df_train=df_train.drop('date', axis=1)   
    df_valid=df_valid.drop('date', axis=1)  
    
    df_train=df_train.drop('symbol', axis=1)   
    df_valid=df_valid.drop('symbol', axis=1)  


<<<<<<< HEAD
    df_valid= df_valid.drop('open', axis=1) 
    df_valid= df_valid.drop('close', axis=1) 
    df_valid= df_valid.drop('high', axis=1) 
    df_valid= df_valid.drop('low', axis=1) 
    df_valid= df_valid.drop('volume', axis=1) 
    df_valid= df_valid.drop('amount', axis=1) 

    df_train= df_train.drop('open', axis=1) 
    df_train= df_train.drop('close', axis=1) 
    df_train= df_train.drop('high', axis=1) 
    df_train= df_train.drop('low', axis=1) 
    df_train= df_train.drop('volume', axis=1) 
    df_train= df_train.drop('amount', axis=1) 


=======
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53
    y_train=df_train[label]
    x_train=df_train.drop(label, axis=1)
    y_valid=df_valid[label]
    x_valid=df_valid.drop(label, axis=1)  
    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_valid = lgb.Dataset(x_valid, y_valid)
 
    
    # 参数设置
    params = {
<<<<<<< HEAD
            'boosting_type': 'gbdt',
            'max_depth': 5,
            'num_leaves': 32,  # 叶子节点数
            'learning_rate': 0.2,  # 学习速率
            'feature_fraction': 0.7,  # 建树的特征选择比例colsample_bytree
            'bagging_fraction': 0.7,  # 建树的样本采样比例subsample
            'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
            'verbose': -1,  # <0 显示致命的, =0 显示错误 (警告), >0 显示信息
            'lambda_l1':300,
            'lambda_l2':300, 
=======
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53
    }
    
    print('Starting training...')
    # 模型训练
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=1000,
                    valid_sets=lgb_valid,
<<<<<<< HEAD
                    early_stopping_rounds=5,
                    # fobj=custom_obj,
                    # feval=custom_eval,  
                    
                    )
=======
                    early_stopping_rounds=5)
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53
    
    print('Saving model...')
    # 模型保存
    gbm.save_model('model.txt')
    # 模型加载
    
    
def lgbpred(df_pred,label='label'):
 

    # df_pred=df_pred.drop('symbol', axis=1)   
    
    gbm = lgb.Booster(model_file='model.txt')
    df_pred=df_pred.drop(label, axis=1)  
    x_pred= df_pred.drop('date', axis=1)   
    x_pred= x_pred.drop('symbol', axis=1)  
<<<<<<< HEAD
    x_pred= x_pred.drop('open', axis=1) 
    x_pred= x_pred.drop('close', axis=1) 
    x_pred= x_pred.drop('high', axis=1) 
    x_pred= x_pred.drop('low', axis=1) 
    x_pred= x_pred.drop('volume', axis=1) 
    x_pred= x_pred.drop('amount', axis=1) 
=======
>>>>>>> 518dc562530751adda57825fe3002a3d3ee48c53
    # 模型预测
    y_pred = gbm.predict(x_pred, num_iteration=gbm.best_iteration)
    df_pred['pred']=y_pred
    return df_pred