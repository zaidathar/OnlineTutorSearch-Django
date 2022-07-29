from django import template
register = template.Library()

@register.filter

def listindex(l,i):
    print("Inside list index")
    print(l)
    if type(l) == str:
        l = l.strip('][').split(', ')
        print(l)
        return l[i].replace("'","")
    elif type(l)== list:
        return l[i]

