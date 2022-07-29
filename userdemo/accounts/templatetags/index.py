from django import template
register = template.Library()


@register.filter
def index(indexable, i):
    if type(indexable) == str:
        indexable = indexable.strip('][').split(', ')
        
    if i==1:
        return int(indexable[i])
    elif i==0:
        res= indexable[i].split(" ")[1][:5]
        
        return res
    return indexable[i]


