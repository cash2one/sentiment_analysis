__author__ = 'fengyi.xu@baifendian.com'

import logging
from set_logger import set_logger

set_logger('logs/algo.log')

import sys
sys.path.append('../../thrift-api-def/gen-py')
from algo_bfd import WeiboService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class algoClient():
    def __init__(self,ip,port):
        try:
            #transport = TSocket.TSocket('localhost', sys.argv[1])
            transport = TSocket.TSocket(ip,port )
            self.transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            self.client = WeiboService.Client(protocol)
            self.transport.open()
            logging.info('algo start')
        except Exception as e:
            logging.error('algo error: %s',e)
    def close(self):
        try:
            self.transport.close()
            logging.info("algo close")
        except Exception as e:
            logging.error("algo close error: %s",e)

if __name__ == '__main__':
    aa = algoClient()
    aa.client.isProduct('adfhadskfj')
    aa.client.shownWant("talfdj")
    aa.close()
