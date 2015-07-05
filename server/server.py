# coding=utf-8  
import sys,os
cur_dir = os.path.dirname( os.path.abspath(__file__)) or os.getcwd()
sys.path.append(cur_dir)
sys.path.append(cur_dir  + '/../thrift-api-def/gen-py')
sys.path.append(cur_dir + '/plugins')
sys.path.append(cur_dir + '/utils')
sys.path.append(cur_dir + '/utils/log')

from getReview.predict import Review
from getSentiment.predict import Sentiment
#import clean

import socket
from set_logger import set_logger
import logging
import json
from algo_bfd import WeiboService  
from thrift.transport import TSocket
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol
from thrift.server import TProcessPoolServer

reviewModel = os.path.join( os.path.dirname(__file__), './plugins/getReview/model.goodbad_1223')

#main service of the thrift api
class PythonServiceServer:
     def __init__(self):
         self.Review = Review(reviewModel)
         self.Sentiment = Sentiment(reviewModel)

     #return positive(1), negative(-1) or neutral(0) sentiment
     def getSentiment(self, content):
        func = "getSentiment"
        try:
            res = self.Sentiment.predict(self.Review, str(content.strip()))
            print res
        except Exception as e:
            logging.error("Error: host: %s \t func: %s \t content: %s \t ",self.host, func, content)
            res = 0
        #logging.info("host: %s \t func: %s \t content: %s \t result: %s ",self.host, func, content, res)
        return res

     #return the degree various from 0 to 1 about bad review to good review
     def getReview(self, content):
        func = "getReview"
        try:
            content = "".join(content.split("\n"))
            res = self.Review.predictPraise(str(content.strip()))
        except Exception as e:
            logging.error("Error: host: %s \t func: %s \t content: %s \t ",self.host, func, content)
            res = 0
        #logging.info("host: %s \t func: %s \t content: %s \t result: %s ",self.host, func, content, res)
        return res
     
##add usage:
def usage():
    print "Usage:"
    print "python server.py port processNum."

if( len(sys.argv) != 3 ):
    usage()
else:
    set_logger('logs/server.log')
    handler = PythonServiceServer()
    processor = WeiboService.Processor(handler)
    transport = TSocket.TServerSocket('0.0.0.0',int(sys.argv[1]))
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)
    server.setNumWorkers(int(sys.argv[2]))

    print "Starting python server..."
    server.serve()
    print "done!"

