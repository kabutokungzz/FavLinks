import math

def pagination_cal(index_first, index_last , query):
    totalCount = query.count() or 0
    query = query[int(index_first):int(index_last)] #LIMIT FIRSTH : LAST

    try:
        pagesCount = (int(totalCount) / int(index_last)) or 0 
    except ZeroDivisionError:
        pagesCount = 0
    pagesCount = math.ceil(pagesCount)
    
    page_size = (int(index_last) - int(index_first))
    # pageNow = (int(index_first) // int(page_size)) + 1
    
    return totalCount, pagesCount, page_size, query