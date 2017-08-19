import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from twmovieapi import user

me = user.User()
print(me.mail)
print(me.phone)
print(me.name)
print(me.preference)
