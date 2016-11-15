# _*_ coding: utf-8 _*_

import time
import calendar
import datetime


# time模块中的三种时间形式
print("time stamp:", time.time())               # 时间戳
print("local time:", time.localtime())          # struct_time类型的本地时间
print("utc time:", time.gmtime())               # struct_time类型的utc时间

# time模块中，三种时间形式之间的转换
time_stamp = time.time()                        # 时间戳
local_time = time.localtime(time_stamp)         # 时间戳转struct_time类型的本地时间
utc_time = time.gmtime(time_stamp)              # 时间戳转struct_time类型的utc时间

time_stamp_1 = time.mktime(local_time)          # struct_time类型的本地时间转时间戳
time_stamp_2 = calendar.timegm(utc_time)        # struct_time类型的utc时间转时间戳
print(time_stamp, time_stamp_1, time_stamp_2)


# time模块中，三种时间形式和字符串之间的转换
print(time.ctime(time_stamp))           # 时间戳转字符串(本地时间字符串)

print(time.asctime(local_time))         # struct_time类型的本地时间转字符串
print(time.asctime(utc_time))           # struct_time类型的utc时间转字符串

print(time.strftime("%Y-%m-%d, %H:%M:%S, %w", local_time))      # struct_time类型的本地时间转字符串：自定义格式
print(time.strftime("%Y-%m-%d, %H:%M:%S, %w", utc_time))        # struct_time类型的utc时间转字符串：自定义格式

struct_time = time.strptime("2016-11-15, 15:32:12, 2", "%Y-%m-%d, %H:%M:%S, %w")       # 字符串转struct_time类型


# datetime模块中datetime类的用法
a_datetime_local = datetime.datetime.now()                      # 获取datetime.datetime类型的本地时间
a_datetime_utc = datetime.datetime.utcnow()                     # 获取datetime.datetime类型的utc时间

print(a_datetime_local.strftime("%Y-%m-%d, %H:%M:%S, %w"))      # datetime.datetime类型转字符串
print(a_datetime_utc.strftime("%Y-%m-%d, %H:%M:%S, %w"))        # datetime.datetime类型转字符串

a_datetime = datetime.datetime.strptime("2016-11-15, 15:32:12, 2", "%Y-%m-%d, %H:%M:%S, %w")    # 字符串转datetime.datetime格式


# datetime.datetime类和时间戳、struct_time类型之间的转换
time_stamp = a_datetime_local.timestamp()                           # datetime类型转时间戳
print(time_stamp)

a_datetime_local = datetime.datetime.fromtimestamp(time.time())     # 时间戳转datetime.datetime类型的本地时间
a_datetime_utc = datetime.datetime.utcfromtimestamp(time.time())    # 时间戳转datetime.datetime类型的utc时间
print(a_datetime_local, a_datetime_utc)

print(a_datetime_local.timetuple())                 # datetime类型转struct_time类型
print(a_datetime_utc.utctimetuple())                # datetime类型转struct_time类型
