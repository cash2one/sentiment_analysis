# coding=utf-8  
from django.http import HttpResponse
import sys
import os
cur_dir = os.path.dirname( os.path.abspath(__file__)) or os.getcwd()
sys.path.append(cur_dir)
sys.path.append(cur_dir + "/../../../thrift-api-def/gen-py/algo_bfd")
from thrift import Thrift  
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
from thrift.protocol import TCompactProtocol
import traceback

thrift_api_ip = "localhost"

def api(request,port,domain,func):
    print request.GET.get("arg").encode("utf-8")
    print port,domain,func
    
    
    try:
        transport = TSocket.TSocket(thrift_api_ip, int(port))   
        transport = TTransport.TBufferedTransport(transport)  
        protocol = TBinaryProtocol.TBinaryProtocol(transport) 
        module = __import__(domain)
        client = module.Client(protocol)  
        transport.open()
        ret = getattr(client, func)( request.GET.get("arg").encode("utf-8") )
        transport.close()
        return HttpResponse( ret )        
        
    except:
        return HttpResponse(traceback.format_exc())
        transport.close()
