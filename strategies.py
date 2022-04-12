import backtrader as bt

class Top10Strategy(bt.Strategy):
    def __init__(self,hold_day=10,hold_n=10):
        self.hold_day=hold_day
        self.hold_n=hold_n
        self.holdlist={}
        pass
        
    def next(self):   
        hold_now=0
        #先买    
        for data in self.datas:
            if self.getposition(data).size > 0:
                if self.holdlist[data._name]>self.hold_day:
                    self.order=self.sell(data=data,size=self.getposition(data).size)
                else:
                    self.holdlist[data._name]=self.holdlist[data._name]+1
                    hold_now=hold_now+1
        
        if hold_now>=self.hold_n:
            return
        
        money=self.broker.get_cash()/self.hold_n-hold_now
        for data in self.datas:
            if hold_now<self.hold_n:
                #买入条件
                
                if data.close[0]==0 or data.close[0]==data.open[0]:
                    continue
                
                if(data.signal[0]==1):
                    size=int(money/data.close[0]/100)*100
                    self.order = self.buy(data=data, size=size)                 
                    self.holdlist[data._name]=1
                    hold_now=hold_now+1