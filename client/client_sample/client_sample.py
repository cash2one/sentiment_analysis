# coding=utf-8  

import sys
sys.path.append('../../thrift-api-def/gen-py') 
from algo_bfd import WeiboService
from thrift import Thrift  
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
from thrift.protocol import TCompactProtocol
import traceback
import json
def pythonServerExe(ip, port, content): 
    try:
        print "IP PORT:" , ip, port 
        transport = TSocket.TSocket(ip, port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = WeiboService.Client(protocol)  
        transport.open()  

        print "getReview"
        print client.getReview(content)
        print "\n"

        print "getSentiment"
        print client.getSentiment(content)
        print "\n"

        transport.close() 
    except Exception as e:
        print "error",e
        traceback.print_exc()

def usage():
    print "usage:"
    print "python client_sample.py ip port stringContent"  


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        dic = {}
        dic['title'] = "国新办发白皮书斥达赖:所谓大藏区纯属虚构"
        dic["body"] = '''以上可见，十四世达赖集团谋求建立“大藏区”，既有违历史，也违背现实，完全脱离中国国情。“大藏区”无视青藏高原数千年来多民族杂居共处的事实，把各民族共同开发青藏高原的历史歪曲为单一民族的历史，在中国各民族之间制造矛盾和分歧，图谋建立排斥其他民族的纯而又纯的“大藏区”，是典型的极端民族主义和种族主主义表现。'''
        str = json.dumps(dic, ensure_ascii = False)
        pythonServerExe( sys.argv[1], int(sys.argv[2]),  str)
