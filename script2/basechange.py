import base64
import string
from lib.Interface import GunnerMod
@GunnerMod
def start(str1,string1='',string2=''):
    """
    base64换表
    str1 编码后字符
    string1 表1
    string2 表2
    """
    string1 = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"
    string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    print (base64.b64decode(str1.translate(str.maketrans(string1,string2))))
#str1 = "x2dtJEOmyjacxDemx2eczT5cVS9fVUGvWTuZWjuexjRqy24rV29q"



