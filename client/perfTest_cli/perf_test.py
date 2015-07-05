# coding=utf-8  

import sys
sys.path.append('../../thrift-api-def/gen-py') 
from algo_bfd import WeiboService
from thrift import Thrift  
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
from thrift.protocol import TCompactProtocol
import time
import threading
import traceback


def testPerf(ip, port, funcName, content, iterTimes):
    try:
        start = time.time()
        transport = TSocket.TSocket(ip, port)   
        transport = TTransport.TBufferedTransport(transport)  
        protocol = TBinaryProtocol.TBinaryProtocol(transport)  
        client = WeiboService.Client(protocol)  
        transport.open()  
        
           
        for i in range(0,iterTimes):
            getattr(client, funcName)( content )
        print "\n"  
        
        transport.close() 
        end = time.time()
        print 'start, end time:', start, end 
        print 'cost Time:' + str(end - start) 
    except:
        print traceback.print_exc()



    
