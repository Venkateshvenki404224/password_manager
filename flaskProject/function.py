import random
import re
import string
from re import *
from flask import session


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex,email):
        return True

def generatescreat(length=15):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))


generatescreat()