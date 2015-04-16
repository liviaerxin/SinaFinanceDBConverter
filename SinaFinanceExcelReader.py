#-*- coding: utf8 -*-

'''
@author: siyao
'''

import os
from SinaFinanceXmlReader import *


class SinaFinanceExcelReader():
    '''
    Read data from excel file to list or dict
    '''
    reader_dict = None
    xmlReader = None
    mapping_list = []
    
    def __init__(self):
        self.init_xml_config()
    
    def getAttributeList(self,filetype):
        attribute_list = self.sina_finance_data_dict[filetype]
        return attribute_list
    
    def getMappingList(self):
        return self.mapping_list
    
    def splitExcelItems(self,fileType,line):
        items = line.split("\t")
        if(len(items) > 0):
            firstItem = self.xmlReader.removeDotTitle(items[0])
            if(self.xmlReader.compareEqualString(fileType, firstItem) == 1):
                self.mapping_list.append(firstItem)
                return items[1:len(items)-2]
        return
                
    def getDateFromExcel(self,line):
        dates = line.split("\t")
        dates_list = []
        if(len(dates) > 0):
            for i in range(1, len(dates)-2):
                dates_list.append(dates[i])
            return dates_list
        return dates_list
    
    def init_readData(self,filePath,filetype):
        self.mapping_list = []
        xml_AttributeList = self.getAttributeList(filetype)
        final_list = []
        if(len(xml_AttributeList)> 0):
            f = open(filePath, 'rb')
            lines = f.readlines()
            count = 0
            for line in lines:
                #line = line.decode('gb2312').encode('utf8') ##### 20150408
                if(count == 0):
                    dates_list = self.getDateFromExcel(line)
                    final_list.append(dates_list)
                    count = count + 1
                    self.mapping_list.append("date_id")
                else:
                    item_list = self.splitExcelItems(filetype,line)
                    if(item_list != None and len(dates_list) == len(item_list)):
                        final_list.append(item_list)
        return final_list
            
    def init_xml_config(self):
        self.xmlReader = SinaFinanceXmlReader()
        self.xmlReader.readFinanceData("SinaFinanceData.xml")
        self.sina_finance_data_dict = self.xmlReader.get_Finance_data()
        
if __name__ == "__main__":
    dir = "finance_db/玻璃行业/sh600176/BalanceSheet.xls"
    dir = dir.decode('utf8').encode('cp936')
    excelReader = SinaFinanceExcelReader()
    filetype = "BalanceSheet"
    final_list = excelReader.init_readData(dir,filetype)
    print final_list[1]
    mapping_list = excelReader.getMappingList()
    ll="存货"
    print mapping_list
    print mapping_list.index(ll.decode('utf8').encode('gbk'))
