# from cryptography.fernet import Fernet 
# from collections import defaultdict
# import datetime

def get_valid_name(s):
    s=s.strip()
    l=s.split(" ")
    l=[i.capitalize() for i in l]
    return ' '.join(l)

def get_combination(s):
    # Deep Learning -> [DEEP LEARNING,,deep learning,dEEP lEARING]
    def upperInverse(s):
        l=s.split(" ")
        l=[i[0].lower()+i[1:].upper() for i in l ]
        return " ".join(l)

    l=[s.upper(),s.lower(),upperInverse(s)]
    return l

def remaining_day(a,b):
    print("Inside REMAINING DAYS")
    print(a,b)
    curr_date= str(a).split()[0].split('-')
    fixed_date = str(b).split()[0].split('-')

    year = int(fixed_date[0]) - int(curr_date[0])
    month = int(fixed_date[1]) - int(curr_date[1])
    day = int(fixed_date[2]) - int(curr_date[2])
    print("remaining day",day)
    if day > 0 or month > 0 or year > 0:
        return True
    else :
        return False
def slicing(l,count):
    print(type(l),len(l))
    while len(l) > count:
        print(l)
        l.pop(0)

    return l

# def encryptMsg(s):
    
#     key = Fernet.generate_key()  
#     f = Fernet(key)  
#     token = f.encrypt(bytes(s,encoding='utf8')) 
#     return [ key ,token ] 

# def decryptMsg(l):
#     f = Fernet(l[0])
#     d = f.decrypte(l[1])
    
#     return d.decode() 

# def get_encrypt(msg,id):

#     msg_token = encryptMsg(msg)

#     l=[str(datetime.datetime.now()),id]+msg_token

#     return l

# def get_decrypt(l):
#     # l.sort()    # to arrange message according to time
    
#     d=defaultdict(list)

#     for i in l:
#         msg = decryptMsg(i[2:])
#         date,time=map(str, i[0].split(" "))

#         d[date].append([i[1],msg,time])

#         return d

# l=get_encrypt("hello",'1')
# print(l)
# print(get_decrypt(l))
