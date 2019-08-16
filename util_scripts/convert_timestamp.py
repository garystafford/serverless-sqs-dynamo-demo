import datetime

ts = 1559040343.1283409

converted = datetime.datetime.fromtimestamp(ts)
print(converted.date())
print(converted.time())
