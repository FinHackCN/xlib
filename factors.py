import os
import talib as ta
import pandas as pd
import alphalens
import numpy as np
from alphalens.utils import get_clean_factor_and_forward_returns
from alphalens.tears import create_full_tear_sheet
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def analysis(df_all,factor_name,periods=[10]):

    df_all = df_all.replace([np.inf, -np.inf], np.nan) 
    df_all=df_all.fillna(0)   
    df_all=df_all[df_all.close>0]

    df_all.reset_index(drop=True)
    df_all['date']=pd.to_datetime(df_all['date'])
    price = df_all.pivot_table(index='date', columns='symbol', values='close')    
    df_all.index=df_all['date']
    price.index = pd.to_datetime(price.index)
    assets = df_all.set_index([df_all.index,df_all['symbol']], drop=True,append=False, inplace=False)
    assets=assets[~assets.index.duplicated()]



 
    
    ret = get_clean_factor_and_forward_returns(assets[factor_name],price,periods=[10],quantiles=None,bins=10,max_loss=1,groupby=None)
    sheet=alphalens.tears.create_full_tear_sheet(ret)
    
    

def getTA(df):
        ## Overlap Studies Functions
        df['UPPER'], df['MIDDLE'], df['LOWER'] = ta.BBANDS(df.close, timeperiod=90, nbdevup=2, nbdevdn=2, matype=0)
        df['DEMA']         = ta.DEMA(df.close, 90)
        df['EMA90']        = ta.EMA(df.close, 90)
        df['HT-TRENDLINE'] = ta.HT_TRENDLINE(df.close)
        df['MA90']         = ta.MA(df.close, 90)
        df['MAMA'], df['FAMA'] = ta.MAMA(df.close)
        df['MAVP']         = ta.MAVP(df.close, df.EMA90)
        df['MIDPOINT']     = ta.MIDPOINT(df.close, 90)
        df['MIDPRICE']     = ta.MIDPRICE(df.high, df.low, 90)
        df['SAR']          = ta.SAR(df.high, df.low, acceleration=0, maximum=0)
        df['SAREXT']       = ta.SAREXT(df.high, df.low, 0, 0, 0)
        df['SMA']          = ta.SMA(df.close, 90)
        df['T3']           = ta.T3(df.close, 90)
        df['TEMA']         = ta.TEMA(df.close, 90)
        df['TRIMA']        = ta.TRIMA(df.close, 90)
        df['WMA']          = ta.WMA(df.close, 90)
    
        ## Momentum Indicator Funnctions
        df['ADX']          = ta.ADX(df.high, df.low, df.close, 90)
        df['ADXR']         = ta.ADXR(df.high, df.low, df.close, 90)
        df['APO']          = ta.APO(df.close, 30, 90)
        df['AROONDOWN'], df['ARRONUP'] = ta.AROON(df.high, df.low, 90)
        df['AROONOSC']     = ta.AROONOSC(df.high, df.low, 90)
        df['BOP']          = ta.BOP(df.open, df.high, df.low, df.close)
        df['CCI']          = ta.CCI(df.high, df.low, df.close, 90)
        df['CMO']          = ta.CMO(df.close, 90)
        df['DX']           = ta.DX(df.high, df.low, df.close, 90)
        df['MACD'], df['MACDSIGNAL'], df['MACDHIST'] = ta.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACDX'], df['MACDSIGNALX'], df['MACDHISTX'] = ta.MACDEXT(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACDFIX'], df['MACDSIGNALFIX'], df['MACDHISTFIX'] = ta.MACDFIX(df.close, 90)
        df['MFI']          = ta.MFI(df.high, df.low, df.close, df.volume, 90)
        df['MINUS-DI']     = ta.MINUS_DI(df.high, df.low, df.close, 90)
        df['MINUS-DM']     = ta.MINUS_DM(df.high, df.low, 90)
        df['MOM']          = ta.MOM(df.close, 90)
        df['PLUS-DI']      = ta.PLUS_DI(df.high, df.low, df.close, 90)
        df['PLUS-DM']      = ta.PLUS_DM(df.high, df.low, 90)
        df['PPO']          = ta.PPO(df.close, 30, 90)
        df['ROC']          = ta.ROC(df.close, 90)
        df['ROCR']         = ta.ROCR(df.close, 90)
        df['ROCR100']      = ta.ROCR100(df.close, 90)
        df['RSI']          = ta.RSI(df.close,90)
        df['SLOWK'], df['SLOWD'] = ta.STOCH(df.high, df.low, df.close)
        df['FASTK'], df['FASTD'] = ta.STOCHF(df.high, df.low, df.close)
        df['FASTK-RSI'], df['FASTD-RSI'] = ta.STOCHRSI(df.close, 90)
        df['TRIX']         = ta.TRIX(df.close, 90)
        df['ULTOSC']       = ta.ULTOSC(df.high, df.low, df.close)
        df['WILLR']        = ta.WILLR(df.high, df.low, df.close, 90)
    
        ## Volume Indicator Functions
        df['AD']           = ta.AD(df.high, df.low, df.close, df.volume)
        df['ADOSC']        = ta.ADOSC(df.high, df.low, df.close, df.volume)
        df['OBV']          = ta.OBV(df.close, df.volume)
    
        ## Volatility Indicator Functions
        df['ATR']          = ta.ATR(df.high, df.low, df.close, 90)
        df['NATR']         = ta.NATR(df.high, df.low, df.close, 90)
        df['TRANGE']       = ta.TRANGE(df.high, df.low, df.close)
    
        ## Price Transform Functions
        df['AVGPRICE']     = ta.AVGPRICE(df.open, df.high, df.low, df.close)
        df['MEDPRICE']     = ta.MEDPRICE(df.high, df.low)
        df['TYPPRICE']     = ta.TYPPRICE(df.high, df.low, df.close)
        df['WCLPRICE']     = ta.WCLPRICE(df.high, df.low, df.close)
    
        ## Cycle Indicator Functions
        df['HT-DCPERIOD']  = ta.HT_DCPERIOD(df.close)
        df['HT-DCPHASE']   = ta.HT_DCPHASE(df.close)
        df['INPHASE'], df['QUADRATURE'] = ta.HT_PHASOR(df.close)
        df['SINE'] , df['LEADSINE'] = ta.HT_SINE(df.close)
        df['HT-TRENDMODE'] = ta.HT_TRENDMODE(df.close)
    
        ## Beta
        df['BETA']         = ta.BETA(df.high, df.low, 90)
        df['CORREL']       = ta.CORREL(df.high, df.low, 90)
        df['LINEARREG']    = ta.LINEARREG(df.close, 90)
        df['LINEARREG-ANGLE'] = ta.LINEARREG_ANGLE(df.close, 90)
        df['LINEARREG-INTERCEPT'] = ta.LINEARREG_INTERCEPT(df.close, 90)
        df['LINEARREG-SLOPE'] = ta.LINEARREG_SLOPE(df.close, 90)
        df['STDDEV']       = ta.STDDEV(df.close, 90, 1)
        df['TSF']          = ta.TSF(df.close, 90)
        df['VAR']          = ta.VAR(df.close, 90, 1)
    
        ## Math Transform Functions
        df['ACOS']         = ta.ACOS(df.close)
        df['ASIN']         = ta.ASIN(df.close)
        df['ATAN']         = ta.ATAN(df.close)
        df['CEIL']         = ta.CEIL(df.close)
        df['COS']          = ta.COS(df.close)
        df['COSH']         = ta.COSH(df.close)
        df['EXP']          = ta.EXP(df.close)
        df['FLOOR']        = ta.FLOOR(df.close)
        df['LN']           = ta.LN(df.close)  # Log
        df['LOG10']        = ta.LOG10(df.close)  # Log
        df['SIN']          = ta.SIN(df.close)
        df['SINH']         = ta.SINH(df.close)
        df['SQRT']         = ta.SQRT(df.close)
        df['TAN']          = ta.TAN(df.close)
        df['TANH']         = ta.TANH(df.close)
    
        ## Math Operator Functions
        df['ADD']          = ta.ADD(df.high, df.low)
        df['DIV']          = ta.DIV(df.high, df.low)
        df['MAX']          = ta.MAX(df.close, 90)
        df['MAXINDEX']     = ta.MAXINDEX(df.close, 90)
        df['MIN']          = ta.MIN(df.close, 90)
        df['MININDEX']     = ta.MININDEX(df.close, 90)
        df['MINIDX'], df['MAXIDX'] = ta.MINMAXINDEX(df.close, 90)
        df['MULT']         = ta.MULT(df.high, df.low)
        df['SUB']          = ta.SUB(df.high, df.low)
        df['SUM']          = ta.SUM(df.close, 90)
        df = df.replace([np.inf, -np.inf], np.nan) 
        df=df.fillna(0)
        return df
    