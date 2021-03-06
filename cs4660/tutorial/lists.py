"""Lists defines simple list related operations"""

def get_first_item(li):
    """Return the first item from the list"""
    return li[0]

def get_last_item(li):
    """Return the last item from the list"""
    i = len(li)
    return li[i -1]

def get_second_and_third_items(li):
    """Return second and third item from the list"""
    new_li = []
    new_li.append(li[1])
    new_li.append(li[2])
    return new_li

def get_sum(li):
    """Return the sum of the list items"""
    # sum = 0.0
    # for i in range(len(li)):
    #     sum += li[i]
    # return sum
    return sum(li)

def get_avg(li):
    """Returns the average of the list items"""
    # sum = 0
    # size = len(li)
    # for i in range(size):
    #     sum += li[i]
    # return sum/size
    return float(get_sum(li)) / len(li)