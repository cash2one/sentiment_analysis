#!usr/bin/python
#coding=utf8
import sys,json
import math
import ConfigParser
import multiprocessing
import logging
import time
from set_logger import set_logger
from algoClient import algoClient
from MySQLClient import MySQLClient
import traceback
reload(sys)
sys.setdefaultencoding('utf8')

class processClient():
    def __init__(self):
        self.worker_number=None
        #method控制select语句查询全部还是非空字段 
        self.method=None
        self.sqlBatchUpate_num=None
        self.sql_select_str=""
        self.sql_update_str=""
        self.host=None
        self.port=None
        self.user=None
        self.passwd=None
        self.DB_name=None
        #table_name表示操作的数据表
        self.table_name=None
        #feild_name表示更新字段列表
        self.field_name=[]
        #servicelist表示服务列表
        self.servicelist=[]
        self.serIp=None
        self.config=ConfigParser.ConfigParser()
        self.serport=None
        #创建ConfigParser实例
    
    def confFileParser(self,configfilename):
        seclist=['default','database','serviceAPI']
        optlist=['worker_number','method','host','port','user','passwd','db_name','table_name','serport']
        self.config.read(configfilename)
        #读取配置文件
        if self.config.get("default","worker_number" ) is not None:
            self.worker_number=int(self.config.get("default","worker_number" ))
        else:
            self.worker_number=20
        if self.config.get("default","sqlbatchupdate_num" ) is not None:
            self.sqlBatchUpdate_num=int(self.config.get("default","sqlbatchupdate_num"     ))
        else:
            self.sqlBatchUpdate_num=10

        if self.config.get("default","method" ) is not None:
            self.method=str(self.config.get("default","method" ))
        else:
            self.method="all"
        if self.config.get("database","host" ) is not None:
            self.host=str(self.config.get("database","host" ))
        else:
            print "请在配置文件中配置数据库服务器IP地址"
            exit(0)
        if self.config.get("database","port" ) is not None:
            self.port=int(self.config.get("database","port" ))
        else:
            print "请在配置文件中配置数据库服务器端口号"
            exit(0)
        if self.config.get("database","user" ) is not None:
            self.user=str(self.config.get("database","user" ))
        else:
            print "请在配置文件中配置用户名"
            exit(0)
        if self.config.get("database","passwd" ) is not None:
            self.passwd=str(self.config.get("database","passwd" ))
        else:
            print "请在配置文件中配置数据库密码"
            exit(0)
        if self.config.get("database","db_name" ) is not None:
            self.DB_name=str(self.config.get("database","db_name" ))
        else:
            print "请在配置文件中配置数据库名"
            exit(0)
        if self.config.get("database","table_name" ) is not None:
            self.table_name=str(self.config.get("database","table_name" ))
        else:
            print "请在配置文件中配置数据表"
            exit(0)
        if self.config.get("default","serport" ) is not None:
            self.serport=int(self.config.get("default","serport" ))
        else:
            print "请在配置文件中配置服务服务端口"
            exit(0)
        if self.config.get("default","serIp" ) is not None:
            self.serIp=self.config.get("default","serIp" )
        else:
            print "请在配置文件中配置服务IP"
            exit(0)
        if self.config.options("serviceAPI") is not None:
            for api in self.config.options("serviceAPI"):
                strlist=str(self.config.get("serviceAPI",api)).split(',')
                self.servicelist.append(strlist[0])
                for i in range(1,len(strlist)):
                    self.field_name.append(strlist[i])
        else:
            print "请在配置文件中配置服务API"
            exit(0)
    
#设置select串
    def set_sql_querry(self,worker_id):
        if self.method and self.table_name and self.worker_number:
            if self.method == 'all':
                self.sql_select_str = 'select id, content from %s where id % %%s = %s' % (self.table_name,self.worker_number,worker_id)
            if self.method == 'null':
                tmpstr=''
                for i in range(0,len(self.field_name)-1):
                    tmpstr=tmpstr+self.field_name[i]+' is not null or '
                tmpstr=tmpstr+self.field_name[len(self.field_name)-1]+' is not null'
                self.sql_select_str = 'select id, content from %s where id % %%s = %s and ( %s )' % (self.table_name,self.worker_number,worker_id,tmpstr)
    def update(self):
        if self.worker_number:
            for i in range(self.worker_number):
                p = multiprocessing.Process(target=self.worker,args=(i,))
                p.start()
   
    
   #数据处理的核心逻辑 
    def worker(self,worker_id,):
        self.set_sql_querry(worker_id)
        if not self.sql_select_str:
            logging.error("set query error")
            return -1
        time.sleep(worker_id)
        db = MySQLClient(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.DB_name)
        algo = algoClient(self.serIp,self.serport)
        print multiprocessing.current_process().name
        
        #执行select语句
        try:
            logging.info("Start select")
            db.cursor.execute(self.sql_select_str)
            res = db.cursor.fetchall()
            logging.info("End select")
        except Exception as e:
            traceback.print_exc()
            logging.error("sql query error %s", e)
            return -1
        
        
        #处理读出的每一条记录
        count=0
        values=[]
        logging.info("Start fetch result")
        
        #loop all the rows fetched
        for i in res:
            
            #query api to get values
            try:
                resultlist=[]
                for j in self.servicelist:
                    resultlist.append(getattr(algo.client,j)(i[1]))
                    logging.info("id: %s \t result: %s", i[0],getattr(algo.client,j)(i[1]))
                resultlist.append(i[0])
                values.append(tuple(resultlist))
                count=count+1
            except Exception as e:
                algo.close()
                algo = algoClient(self.serIp,self.serport)
                traceback.print_exc()
                logging.error("algo error: %s: %s",i[1],e)
                continue
            
            #generate update sql and batch update db
            try:
                tmpstr=''
                for d in range(0,len(self.field_name)-1):
                    tmpstr=tmpstr+self.field_name[d]+' =%s,'
                tmpstr=tmpstr+self.field_name[len(self.field_name)-1]+' =%s'
                self.sql_update_str='update '+self.table_name+' set '+tmpstr+' where id =%s'
                if(count==self.sqlBatchUpdate_num):
                    logging.info("End fetch result")
                    db.cursor.executemany(self.sql_update_str,values)
                    logging.info("Update complete")
                    count=0
                    values=[]
            except Exception as e:
                print "cfs"
                traceback.print_exc() 
                logging.error("sql update error: %s",e)
                continue
        
        if count!=0:
            db.cursor.executemany(self.sql_update_str,values)
            logging.info("Update All comllete")
            
        db.close()
        algo.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "useage: python processCient.py example.cfg"
    else:
        uu = processClient()
        uu.confFileParser(sys.argv[1])
        uu.update()
