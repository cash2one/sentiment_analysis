#coding = utf-8
__author__ = "jianfeng.chen@baifendian.com"

import sys
import logging
from MySQLClient import MySQLClient
from matchRule import matchRule
import time

class Update():

    def __init__(self):
        self.type = None;   #define data type
        self.dataNum = None;    #define running model(All||marked||5000)
        self.typeContent = None;    #define table type
        self.sql_select_rule = None;    #sql select rule
        self.sql_select_content = None;     #sql select content

    def set_type(self, type):
        #data type : table types
        typelist = {'product':'isproduct', 'service':'isservice', 'marketing':'ismarketing', 'transport':'istransport', 'likebuy':'likebuy', 'good':'isgoodpraise', 'bad':'isbadpraise'};
        if type not in typelist:
            logging.error("type input error");
            return False;
        self.type = type;
        self.typeContent = 'content_' + typelist[type];

    def set_dataNum(self, dataNum):
        #set running model
        self.dataNum = dataNum;
        
    def set_sql_query_rule(self):
        #set select rule
        self.sql_select_rule = 'select id, rule_content from content_rule where type = \'%s\' ORDER BY rule_content' %(self.type);

    def set_sql_query_content(self):
        #set select content
        if(self.dataNum == 'marked'):
            self.sql_select_content = 'select id, content from %s where has_marked = 1' %(self.typeContent);
        elif(self.dataNum == 'All'):
            self.sql_select_content = 'select id, content from %s' %(self.typeContent);
        else:
            num = int(self.dataNum);
            self.sql_select_content = 'select id, content from %s LIMIT %s' %(self.typeContent, num);
        
    def update(self):
        p = multiprocessing.Process(target=self.match);
        p.start();
        #p.join();

    #rule match content
    def match(self):
        self.set_sql_query_rule();
        self.set_sql_query_content();
        if not self.sql_select_rule:
            logging.error("set rule query error");
            return -1;
        if not self.sql_select_content:
            logging.error("set content query error");
            return -1;
        
        dbRule = MySQLClient();
        #print (multiprocessing.current_process().name);
        try:
            #print self.sql_select_rule;
            dbRule.cursor.execute(self.sql_select_rule);
            logging.error("select rule done!");
            ruleRow = dbRule.cursor.fetchall();
        except Exception as e:
            logging.error("sql query error %s", e);
            return -1;

        dbContent = MySQLClient();
        #print (multiprocessing.current_process().name);
        try:
            dbContent.cursor.execute('update ' + self.typeContent + ' set data_rule_id = null and key_word = null where data_rule_id is not null');
            logging.error("update all done!");
            dbContent.cursor.execute(self.sql_select_content);
            logging.error("select content done!");
            contentRow = dbContent.cursor.fetchall();
        except Exception as e:
            logging.error("sql query error %s", e);
            return -1;
        
        logging.error("sql connection done!");

        count = 0;
        values = [];
        for i in contentRow:
            for j in ruleRow:
                #print i[1];
                #print j[1];
                flag, result = matchRule(i[1], j[1]);
                if(flag == True):
                    try:
                        strResult = ",".join(result);
                        logging.error("sql update strResult %s", i[0]);
                        values.append((j[0], strResult, i[0]));
                        #logging.error("sql update strResult %s", values);
                        count = count + 1;
                        #sql_update = 'update %s set data_rule_id = %s, key_word = \'%s\' where id = %s' %(self.typeContent, j[0], strResult, i[0]);
                        #print sql_update;
                        #dbContent.cursor.execute(sql_update);
                        break;
                    except Exception as e:
                        logging.error("sql update error %s", e);
                        return -1;
            if(count == 100):
                print count;
                print values;
                logging.error("sql update strResult %s", values);
                try:
                    update_sql = 'update ' + self.typeContent + ' set data_rule_id = %s, key_word = %s where id = %s'
                    #dbContent.cursor.executemany('update content_isproduct set data_rule_id=%s, key_word=%s where id=%s', values);
                    dbContent.cursor.executemany(update_sql, values);
                    count = 0;
                    values = [];
                except Exception as e:
                    logging.error("sql executemany error %s", e);
                    return -1;
        if(count != 0):
                print count;
                print values;
                logging.error("sql update strResult %s", values);
                try:
                    update_sql = 'update ' + self.typeContent + ' set data_rule_id = %s, key_word = %s where id = %s';
                    logging.error(update_sql);
                    dbContent.cursor.executemany(update_sql, values);
                    #dbContent.cursor.executemany('update content_isproduct_copy set data_rule_id=%s, key_word=%s where id=%s', values);
                    count = 0;
                    values = [];
                except Exception as e:
                    logging.error("sql executemany error %s", e);
                    return -1;
        dbRule.close();
        dbContent.close();

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print len(sys.argv);
        print ("input error!");
        print "Usage: type All|marked|int_number.";
    else:
        time1 = time.time();
        uu = Update();
        #judge type = argv[1] validity
        runModel_flag = True;
        if(uu.set_type(sys.argv[1]) == False):
            runModel_flag = False;
            print "Usage: The first parameter is product|service|transport|likebuy|marketing|good|bad";

        #judge dataNum = argv[2] validity   
        try:
            i = int(sys.argv[2]);
            print i;
        except Exception as e:
            if(sys.argv[2] != "marked" and sys.argv[2] != "All"):
                runModel_flag = False;
                print "Usage:  The second parameter is  All|marked|int_number";
                logging.error("input error!");
    
        if(runModel_flag == True):
            uu.set_dataNum(sys.argv[2]);
            print (uu.type);
            print (uu.typeContent);
            uu.match(); #rule match content
            time2 = time.time();
            print time2 - time1;
            logging.error('time is %s', time2 - time1);
    
