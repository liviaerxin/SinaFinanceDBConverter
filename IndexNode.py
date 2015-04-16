'''
@author: siyao
'''

class IndexNode():
    '''
    stock index node
    '''
    def __init__(self,left,right):
        self.left = left
        self.right = right
        self.data = ""
        self.statementType = ""
        self.isLeaf = 0 #leaf node stands for file
         
    def setAttributes(self,left,right):
        self.left = left
        self.right = right
         
    def printAttributes(self):
        print self.data, " : ", self.left," - ", self.right
