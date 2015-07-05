#coding = utf-8
__author__ = 'fengyi.xu@baifendian.com'
import MySQLdb
import logging
import time
from set_logger import set_logger

set_logger('logs/mysql.log')
class MySQLClient():
    def __init__(self,host = '192.168.24.45', port = 3306,user = 'bfdroot', passwd = 'qianfendian', db = 'weibo', charset = 'utf8'):
        while True:
            try:
                self.conn = MySQLdb.connect(host,user,passwd,db,port,charset)
                self.conn.autocommit(True)
                self.cursor = self.conn.cursor()
                self.cursor.execute("SET NAMES utf8")
                logging.info('mysql established')
                break
            except Exception as e:
                logging.error('mysql error: %s', e)
                time.sleep(10)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info('mysql closed')
        except Exception as e:
            logging.error('mysql close error %s: ',e)

