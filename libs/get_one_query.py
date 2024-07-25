def first_query(queryset):
    try:
        return queryset[0]
    except:
        return queryset.first()
    
def last_query(queryset):
    try:
        return queryset[-1]
    except:
        return queryset.last()