import lightgbm as lgb
#from datetime import datetime


def datasplit(df,train_end='2019-01-01',valid_end='2020-01-01'):
    #df=df.dropna()
    df_train=df[df.date<train_end]
    df_valid=df[df.date>train_end]
    df_valid=df_valid[df_valid.date<valid_end]   
    
    df_pred=df[df.date>=valid_end]
    
    df_train.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)
    df_valid.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)
    df_pred.drop_duplicates(subset=['symbol','date'],keep='first',inplace=True)



    
    return df_train,df_valid,df_pred
    

def lgbtrain(df_train,df_valid,label='label'):

    df_train=df_train.drop('date', axis=1)   
    df_valid=df_valid.drop('date', axis=1)  
    
    df_train=df_train.drop('symbol', axis=1)   
    df_valid=df_valid.drop('symbol', axis=1)  


    y_train=df_train[label]
    x_train=df_train.drop(label, axis=1)
    y_valid=df_valid[label]
    x_valid=df_valid.drop(label, axis=1)  
    lgb_train = lgb.Dataset(x_train, y_train)
    lgb_valid = lgb.Dataset(x_valid, y_valid)
 
    
    # 参数设置
    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }
    
    print('Starting training...')
    # 模型训练
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=1000,
                    valid_sets=lgb_valid,
                    early_stopping_rounds=5)
    
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
    # 模型预测
    y_pred = gbm.predict(x_pred, num_iteration=gbm.best_iteration)
    df_pred['pred']=y_pred
    return df_pred