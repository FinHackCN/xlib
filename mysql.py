import configparser
import os
import pymysql
from sqlalchemy import create_engine
import pandas as pd
from .config import config

class mysql:
    @staticmethod
    def getDB(connection='default'):
        dbcfg=config.getConfig('db',connection)
        db = pymysql.connect(
            host=dbcfg['host'],
            port=int(dbcfg['port']), 
            user=dbcfg['user'], 
            password=dbcfg['password'], 
            db=dbcfg['db'], 
            charset=dbcfg['charset'],
            cursorclass=pymysql.cursors.DictCursor)
        return db,db.cursor() 
        
    def getDBEngine(connection='default'):
        dbcfg=config.getConfig('db',connection)
        engine=create_engine('mysql+pymysql://'+dbcfg['user']+':'+dbcfg['password']+'@'+dbcfg['host']+':'+dbcfg['port']+'/'+dbcfg['db']+'?charset='+dbcfg['charset'],encoding='utf-8')  
        return engine
    
    def toSql(df,table,connection='default'):
        engine=config.getDBEngine(connection)
        res = df.to_sql(table, engine, index=False, if_exists='append', chunksize=5000)
        
    def selectToList(sql,connection='default'):
        result_list=[]
        db,cursor = mysql.getDB(connection)
        try:
           cursor.execute(sql)
           results = cursor.fetchall()
           for row in results:
                result_list.append(row)
        except Exception as e:
           print(sql+"MySQL Error:%s" % str(e))
        db.close()  
        return result_list
        
    def delete(sql,connection='default'):
        db,cursor = mysql.getDB(connection)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
           print(sql+"MySQL Error:%s" % str(e))
        db.close()  
        
        
    def sqlexec(sql,connection='default'):
        db,cursor = mysql.getDB(connection)
        print("Run Sql:"+sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
           print(sql+"MySQL Error:%s" % str(e))
        db.close()          
        
    def selectToDf(sql,connection='default'):
        db,cursor = mysql.getDB(connection)
        results=pd.DataFrame()
        
        try:
           cursor.execute(sql)
           results = cursor.fetchall()
           results= pd.DataFrame(list(results))
        except Exception as e:
           print(sql+"MySQL Error:%s" % str(e))
        db.close()  
        return results  
        
    def truncateTable(table,connection='default'):
        db,cursor = mysql.getDB(connection)
        try:
            sql=" truncate table "+table
            cursor.execute(sql)
        except Exception as e:
            print(sql+"MySQL Error:%s" % str(e))
        db.close()  
        return True