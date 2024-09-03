import re
mystring = 'http://127.0.0.1:8000/62/fill_values'
'http://127.0.0.1:8000/62/fill_values'
'http://127.0.0.1:8000/62/print/Eye'

s = mystring.split('/')
s = [x for x in s if x.isdigit()][0]
print(s)