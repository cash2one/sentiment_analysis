#!usr/bin/python
# coding=utf8
import sys,os,logging,traceback
reload(sys)
sys.setdefaultencoding('utf8')

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append( cur_dir )

import predict_model

class Review:
    def __init__(self,modelfile=''):
        print 'modelfile:',modelfile
        self.model,self.count_vec = predict_model.load_model(modelfile)
        # self.rule_set = predict.load_rule(rulefile)


    def predictPraise(self,content):
        print "Review Content:", content
        predicted=predict_model.predict_line_base_model(content,self.model,self.count_vec)
        if len(predicted)==2:
            return predicted[1]
        else:
            return 0.5

if __name__ == '__main__':
    pr = Review('./model.goodbad_1223')
    print pr.predictPraise('我就知道特斯拉和华为合作，会很不错的。')





