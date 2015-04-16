#-*- coding: utf8 -*-
'''
@author: siyao
'''

import os
import MySQLdb
import logging
from IndexNode import *
from SinaFinanceExcelReader import *


class SinaFinanceDBCompiler():
    '''
    Complier to convert the files data to MySQL DB
    '''
    def __init__(self):
        self.excelReader = SinaFinanceExcelReader()
        self.financeData_Init = 0   #20150408 siyao
    def initDataBaseIndex(self,dir,node):
        try:
            self.conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="test",charset="utf8")
            self.cursor = self.conn.cursor()
             
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS sinaFinanceDatabase")
            self.conn.select_db("sinaFinanceDatabase")
            
            self.cursor.execute("DROP TABLE IF EXISTS table_sinafinance_index")
            self.cursor.execute("CREATE TABLE table_sinafinance_index(id int PRIMARY KEY AUTO_INCREMENT,name varchar(100),Lft int,Rgt int) DEFAULT CHARSET=utf8")
            
            if(self.financeData_Init == 0):
                self.createSinaFinanceDataTable()
                self.financeData_Init = 1
            
            self.createIndex(dir, node)
            
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        finally:
            self.cursor.close()
            self.conn.close()
            
    def createSinaFinanceDataTable(self):
        self.type_attr_list = {}   #----siyao---4.10
        xml_config_dict = self.excelReader.sina_finance_data_dict
        for statementType in xml_config_dict: 
            attr_list = ""
            attrs_list = ["stock_id", "date_id"]   #----siyao---4.10
            for item in xml_config_dict[statementType]:
                attr_list = attr_list+","+item+" float"
                attrs_list.append(item)   #----siyao---4.10
            if(len(attr_list) > 0):
                self.cursor.execute("DROP TABLE IF EXISTS table_sinafinance_%s"%(statementType))
                sql = "CREATE TABLE table_sinafinance_"+statementType+" (stock_id varchar(100), date_id int "+attr_list+") DEFAULT CHARSET=utf8"
                print sql
                self.cursor.execute(sql)
            #----siyao---4.10
            self.type_attr_list[statementType] = attrs_list # attrs_list is unicode
            
    def createIndex(self,dir,node):
        list = os.listdir(dir)
        reachBottom = 0
        for i in range(0, len(list)):
            self.filePath = os.path.join(dir, list[i])
            attribute = list[i].decode('gb2312')
            if(attribute != u'金融行业'):
                if os.path.isdir(self.filePath):
                    self.initNewIndexNode(reachBottom,node,attribute)
                    self.createIndex(self.filePath,self.newNode)
                else:
                    stockId = node.data
                    filetype = attribute.strip(".xls")
                    final_list = self.excelReader.init_readData(self.filePath,filetype)
                    if(len(final_list) > 0):
                        self.insertFinanceStatementInfo(filetype,stockId,final_list)
                if(i == len(list)-1):
                    self.ammendParentNode(node)
            reachBottom = 1
            
    def insertFinanceStatementInfo(self,filetype,stockId,final_list):
        inserted_list = []
        attrs_list = self.type_attr_list[filetype]  #--siyao 4.10--
        #print "attrs_list" , attrs_list #
        mappingList = self.excelReader.getMappingList()
        #print "mappinglist" , mappingList #
        for i in range(0, len(final_list[0])):
            inserted_value = []
            index = 0
            inserted_value.append(str(stockId))
            while(index < len(final_list)):
                item = attrs_list[index+1].encode('gbk') #--siyao 4.10--
                re_index = mappingList.index(item)#--siyao 4.10--
                list = final_list[re_index]
                inserted_value.append(list[i])
                index = index + 1
            inserted_list.append(inserted_value)
        self.makeFinanceStatementSql(filetype,inserted_list)
    
    def makeFinanceStatementSql(self,filetype,inserted_list):
        attributes = ""
        for i in range(0, len(inserted_list[0])-1):
            attributes = attributes+",%s"
        sql = "INSERT INTO table_sinafinance_"+filetype+ " VALUES (%s"+attributes+")"
        self.cursor.executemany(sql,inserted_list)
        self.conn.commit()
    
    def ammendParentNode(self,node):
        node.right = self.newNode.right+1
        node.printAttributes()
        self.insertIndex(node)
        self.newNode = node
        
    def initNewIndexNode(self,reachBottom,node,attribute):
        if(reachBottom == 1):
            self.newNode = IndexNode(self.newNode.right,self.newNode.right)
        else:
            self.newNode = IndexNode(node.left,node.left)
        self.newNode.data = attribute
    
    def insertIndex(self,node):
        sql = "INSERT INTO table_sinafinance_index(name,Lft,Rgt) VALUES ('%s',%d,%d)"%(node.data,node.left,node.right)
        #sql = sql.decode('utf-8')
        self.cursor.execute(sql)
        self.conn.commit()
        
if __name__ == "__main__":
    dir = "finance_db/"
    root = IndexNode(1,2)
    root.data = "finance_db"
    compiler = SinaFinanceDBCompiler()
    compiler.initDataBaseIndex(dir,root)
