#coding=utf-8
'''
@author: siyao
'''

from  xml.dom import  minidom

class SinaFinanceXmlReader():
    '''
    Parse the XML to dict
    '''
    sina_finance_data_dict = {}
    sina_finance_indicator_dict = {}
    
    def __init__(self):
        pass
    
    def readFinanceData(self,fileName):
        self.fileName = fileName
        self.doc = minidom.parse(self.fileName)
        return self.get_Finance_data()
        
    def readFinanicalIndicator(self,fileName):
        self.fileName = fileName
        self.doc = minidom.parse(self.fileName)
        return self.get_Indicator_data()
        
    def get_attrvalue(self,node, attrname):
        return node.getAttribute(attrname) if node else ''

    def get_nodevalue(self,node, index=0):
        return node.childNodes[index].nodeValue if node else ''

    def get_xmlnode(self,node, name):
        return node.getElementsByTagName(name) if node else []
        
    def get_Finance_data(self):
        root = self.doc.documentElement
        statement_nodes = self.get_xmlnode(root,'Statement')
        for node in statement_nodes:
            statementName = self.get_attrvalue(node,'id')
            attributeList = self.get_xmlnode(node,'attribute')
            attributeValueList = []
            for attribute in attributeList:
                print attribute.childNodes
                attributeValue = self.get_nodevalue(attribute)
                attributeValueList.append(attributeValue)
            self.sina_finance_data_dict[statementName] = attributeValueList
        return self.sina_finance_data_dict

    def get_Indicator_data(self):
        root = self.doc.documentElement
        indicator_nodes = self.get_xmlnode(root,'Indicator')
        for node in indicator_nodes:
            indicatorName = self.get_attrvalue(node,'id')
            attributeList = self.get_xmlnode(node,'Statement')
            indicator_dict = {}
            self.sina_finance_indicator_dict[indicatorName] = indicator_dict
            for attribute in attributeList:
                statementName = self.get_attrvalue(attribute,'id')
                attributeValue = self.get_nodevalue(attribute)
                if(indicator_dict.get(statementName) == None):
                    attribute_list = []
                    attribute_list.append(attributeValue)
                    indicator_dict[statementName] = attribute_list
                else:
                    list = indicator_dict.get('balancesheet')
                    list.append(attributeValue)
        return self.sina_finance_indicator_dict
    
    def removeDotTitle(self,inputString):
        inputString = inputString.strip("\r\n")  ##### 20150408 siyao
        regex = u"、".encode("gb2312")  ##### 20150408 siyao
        if(regex in inputString):
            return inputString.split(regex)[1]
        else:
            return inputString 
    
    def compareEqualString(self,fileType,inputString):
        attributeList = self.sina_finance_data_dict[fileType]
        inputString = inputString.decode("gb2312") # string to unicode
        for attribute in attributeList:
            if(attribute == inputString):
                return 1
        return 0

if __name__ == "__main__":
    xmlReader = SinaFinanceXmlReader()
    print xmlReader.readFinanceData("SinaFinanceData.xml")
    print xmlReader.readFinanicalIndicator("FinancialIndicators.xml")
