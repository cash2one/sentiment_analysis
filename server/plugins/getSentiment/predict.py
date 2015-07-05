#coding=utf-8
#__author__=jianfeng.chen@baifendian.com

import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf8')

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append( cur_dir )
sys.path.append(os.path.join(cur_dir + "/../../plugins"))
import re
import math
from getReview.predict import Review

class Sentiment:
    def __init__(self, modelfile = ''):
        self.Review = Review(modelfile)

    def predict(self,Review, content):
        print "content:",content
        dic_content = json.loads(content)
        s = dic_content['body']
        bodyList = re.split(u';|；|,|，|。|\?|？|！|!', s)
        bodyList = [i for i in bodyList if i != ""]
        f_sentiment = []
        for i in bodyList:
            print i
            f_sentiment.append(self.Review.predictPraise(i.strip()))
        print "f_sentiment:", f_sentiment
        length = len(bodyList)
        f_position = []
        for i in range(length):
            cal = pow(float(i-length/2), 2)/pow(length/2, 2)
            f_position.append(cal)
        print "f_position:", f_position
        #f_keyword = findKeyword(bodyList)
        f = []
        for i in range(length):
            f.append(f_sentiment[i] * 0.6 + f_position[i] * 0.4)
        #f = [i*0.6 for i in f_sentiment] + [i*0.4 for i in f_position]
        print "f:", f
        return max(f)

if __name__ == '__main__':
    pr = Sentiment()
    dic = {}
    dic['title'] = 'dasdasda'
    dic['body'] = 'sadasd,dafwe,fdas,daew,dadsa!'
    print pr.predict(dic)
