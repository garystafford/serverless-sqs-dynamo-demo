# Reference: https://docs.python.org/2/library/time.html#time.strftime

import datetime

ts = 1559040343.1283409
converted = datetime.datetime.fromtimestamp(ts)
print(converted)
print(converted.date().strftime('%Y-%m-%d'))
print(converted.time().strftime('%H:%M:%S'))

ts = '1559040343.1283409'
converted = datetime.datetime.fromtimestamp(float(ts))
print(converted)
print(converted.date().strftime('%Y-%m-%d'))
print(converted.time().strftime('%H:%M:%S'))
