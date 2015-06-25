# -*- coding: utf-8 -*-

import math 

from GradeServer.resource.otherResources import OtherResources

"""
페이징에 필요한 정보들을 구하는 모듈
"""
def get_page_pointed(pageNum, count, BLOCK = OtherResources().const.BLOCK, LIST = OtherResources().const.LIST):
    
    #Show List
    startList = (pageNum - 1) * LIST
    endList = (pageNum * LIST) if startList + LIST < count - 1 else count
    
    #show Page
    allPage = int(math.ceil(count / float(LIST)))
    #block = pageNum / BLOCK if pageNum < BLOCK else pageNum - BLOCK
    #startPage = block + 1 
    #endPage = block + BLOCK 
    startPage = 1 if pageNum - 3 < 1 else (allPage - BLOCK  +1 if pageNum + 3 > allPage else pageNum - 3)
    endPage = pageNum if pageNum == allPage else (BLOCK if startPage == 1 else pageNum + 2)
    #Minimum Page
    if endPage > allPage:
        endPage = allPage
        
    return {'LIST': LIST,
            'BLOCK': BLOCK,
            'count': count,
            'pageNum': pageNum,
            'startList': startList,
            'endList': endList,
            'startPage': startPage,
            'endPage': endPage,
            'allPage': allPage}
    
    
'''
Page Number Case Record
'''
def get_page_record(recordsSub, pageNum, LIST = OtherResources().const.LIST):
        
    return recordsSub.slice((pageNum - 1) * LIST,
                            pageNum * LIST)
