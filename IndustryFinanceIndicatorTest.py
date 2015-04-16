# -*- coding:utf8 -*-
'''
@author: siyao
'''

import MySQLdb
from SinaFinanceXmlReader import *


class IndustryFinanceIndicatorTest():
    '''
    From MysSQL DB, get the finance indicator and do some simple adding up.
    '''
    def __init__(self):
        pass
    
    def makeSql(self,financeIndicator):
        xmlReader = SinaFinanceXmlReader()
        sina_finance_indicator_dict = xmlReader.readFinanicalIndicator("FinancialIndicators.xml")
        dict = sina_finance_indicator_dict.get(financeIndicator.decode('utf-8'))
        keys = dict.keys()
        sql = ""
        for key in keys:
            attr_string = ""
            attr_list = dict[key]
            for attr in attr_list:
                attr_string = attr_string+","+attr
            
            sql = "select stock_id, date_id"+attr_string+ " from table_sinafinance_"+key+" where stock_id in "
            #print "key:"+key+",value:"+str(dict[key])
        print sql
        return sql
    
    def searchDataFromDB(self, industryName, financeIndicator):
        '''
        search data relate with financeIndicator from DB
        '''
        try:
            self.conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="sinafinancedatabase",charset="utf8")
            self.cursor = self.conn.cursor()          
            self.makeSql(financeIndicator) 
            self.cursor.execute("select Lft,Rgt from table_sinafinance_index where name = '"+industryName+"'")
            
            range = self.cursor.fetchone()
            if(len(range) == 2):
                sql = self.makeSql(financeIndicator)+"(select name from table_sinafinance_index where Lft >= "+str(range[0])+" and Rgt <= "+str(range[1])+")"
                self.cursor.execute(sql)
                data_list = self.cursor.fetchall()
                return data_list
                self.calculateLiquidityRatio(data_list)
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        finally:
            self.cursor.close()
            self.conn.close()
            
    def calculateLiquidityRatio(self,data_list):
        for data in data_list:
            if(data[1]!=0 and data[2]!=0):
                print data[0]+" : "+str(data[1])+" : "+str(data[2])+"  = ratio : "+str(data[1]/data[2])

    def dataSetAsTime(self, datalist):
        '''
        According to the same time(date_id), clustering all data in datalist return a dict with date_id as the key
        '''
        time_dict_set = {}
        time_list = []
        weight = 1.00   #assume each stock has the same weighting factor: 1.00
        for data in datalist:
            if data[1] not in time_list:
                time_list.append(data[1])
                time_dict_set[data[1]] = []
            rate = data[2]/data[3] + 0.01
            ratew = (rate, weight)
            time_dict_set[data[1]].append(ratew)
        return time_dict_set
            
    def addUpAsTime(self, time_dict_set):
        result_dict = {}
        for time, data in time_dict_set.items():
            addupdata = 0
            weightTotal = 0
            for v in data:
                addupdata += v[0] * v[1]
                weightTotal += v[1]
            print "time %s, addupdata %s, weightTotal %s"  % (time,addupdata,weightTotal)
            addupdata = addupdata/weightTotal
            result_dict[time] = addupdata
        return result_dict
            
if __name__ == "__main__":            
    industryName = "交通运输"
    financeIndicator = "资产负债率"
    test = IndustryFinanceIndicatorTest()
    datalist = test.searchDataFromDB(industryName,financeIndicator)
    datatimeset = test.dataSetAsTime(datalist)
    addupdata= test.addUpAsTime(datatimeset)
    print addupdata
    '''
    {20140930L: 0.4629896105749899, 20090630L: 0.5077677046695148, 20120331L: 0.4796105223208817, ...}
    '''
