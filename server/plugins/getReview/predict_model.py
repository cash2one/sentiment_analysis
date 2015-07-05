# -*- coding: UTF-8 -*-
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn import metrics
import numpy as np
import sys,logging,traceback,random,math,string
#import jieba
import os, datetime
try:
    import cPickle as pickle
except:
    import pickle

cur_dir = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()
sys.path.append( cur_dir )
#sys.path.append( cur_dir + "/Nlpir2014")
import nlpir

def prt_debug_msg2(*msg):
    if 1:
        if msg:
            print "[",datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S'),"]",
        for v in msg:
            print v,
        print
        sys.stdout.flush()

def read_data(path):
    label = []
    train = []
    for line in open(path,'r'):
        l_line = line.strip().split()

        label.append(l_line[0])
        s=' '.join(l_line[1:])
        train.append(s)
    return label,train

def content_cut(content):
    #l_words = list(jieba.cut(content))
    str_words = nlpir.segWithTag(str(content))  #return string
    #str_words = nlpir.seg(content)   ## word with nature
    #str_words = str_words.replace('/','')
    #prt_debug_msg2(str_words)
    return str_words
def feature_extract(line):
    pass
def load_model(model_path=''):
    if model_path=='':
        return None,None
    try:
        fp = open(model_path,'r')
        clf = pickle.load(fp)
        count_vect = pickle.load(fp)
        fp.close()
        return clf,count_vect
    except Exception, e:
        logging.error(traceback.print_exc())
        logging.error("load model error: %s", e)

def load_rule(rule_path=''):

    if rule_path=='':
        return None
    try:
        return predict_rule.setBuyRule(rule_path)
    except Exception, e:
        logging.error(traceback.print_exc())
        logging.error("load rule error: %s", e)

def predict_line_base_model(line, clf,count_vect):
    l = content_cut(line)
    X = count_vect.transform([l])
    
    predicted = clf.predict_proba(X).tolist()
    return predicted[0]
    '''
    if len(predicted)==3:
        if predicted[2]>0.6:
            return predicted[2],1

        elif predicted[0]>0.5:
            return predicted[0],-1


        else:
            return predicted[1],0
    else:
        return predicted,0

    
    if len(predicted)==2:
        if predicted[1]>0.8:##0.36 for neutral
            return predicted[1],1
        elif predicted[0]>0.8:###0.64
            return predicted[1],-1
    return 0.5,0
    '''
def predict_line_base_rule(rule_set,line):
    return  predict_rule.getBuy(rule_set,line)

def predict_line(line,clf,count_vect,rule_set):
    #randomly predict
    if clf==None and rule_set==None:
        return random.random()

    #predict base model
    r_model = 0
    if clf!=None:
        l = content_cut(line)
        r_model = predict_line_base_model(l,clf,count_vect)
        prt_debug_msg2('model predict prob:'+str(r_model))
    #predict base rules
    r_rule = 0
    if rule_set!=None:
        r_rule = predict_line_base_rule(rule_set,line)
        prt_debug_msg2('rule predict prob:'+str(r_rule))

    return min(r_model,r_rule)

# def predict(test_path,model_path,thres):
#     #load classifer
#     clf,count_vect = load_model(model_path)
#  
#     #read testing data
#  
#     label,test = read_data(test_path)
#  
#     X_test_counts = count_vect.transform(test)
#     # tfidf_transformer = TfidfTransformer()
#     # X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
#     prt_debug_msg2('length of test data : ' + str(len(test))
#  
#     #predicted
#     #predicted = clf.predict(X_test_counts)
#     predicted = clf.predict_proba(X_test_counts) 
#     predicted = predicted.tolist()
#     predicted = predict_with_threshold(predicted,thres)
#  
#     get_precision_and_recall(label,predicted)
#     #predicted = np.array(predicted)
#     #prt_debug_msg2(label)
#     #predict_rule = np.array(predict_rule)
#     #prt_debug_msg2("The predicted accuracy : "+"%.2f%%" %(100*(np.mean(predicted == label))))

# def debug(model_path):
#     model, vacab = load_model(model_path)
#     for v in vacab.vocabulary_:
#         prt_debug_msg2(v,)
#     prt_debug_msg2('\n',len(vacab.vocabulary_))

if __name__ =='__main__':
    clf,count_vect = load_model('model.goodbad_1223')
    fp = open('result','w')
    prd = []
    test_label = []
    for line in open('test','r'):
        l_line=line.strip().split('\t')
        pred = 1
        if len(l_line)==2:
            try:
                test_label.append(string.atof(l_line[0]))
                predicted,label = predict_line_base_model(l_line[1],clf,count_vect)
                '''
                if predicted>0.8:
                    pred = 1
                elif predicted<0.4:
                    pred = -1
                else:
                    pred = 0
                prd.append(pred)
                '''
                prd.append(label)
                fp.write(str(label)+'\t'+line)
            except:
                continue
    prd = np.array(prd)
    test_label = np.array(test_label)
    #print "The predicted accuracy : "+"%.2f%%" %(100*(np.mean(prd == test_label)))
    fp.close()

