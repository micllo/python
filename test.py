import re

a = 'A234567890'
if re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a):
    print('OK')
else:
    print('Failed')

res = re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a)
print(res)
print(res.group(0))
# print(res.group(1))

