# _*_ coding: utf-8 _*_

"""
python_csv.py by xianhu
"""

import csv
import datetime

# 数据
data = [
    [1, "a,bc", 19.353, datetime.datetime(2001, 3, 17)],
    [2, "ei,f", 13.287, datetime.datetime(2011, 4, 27)],
    [3, "q\"ij", 15.852, datetime.datetime(2003, 7, 14)],
    [4, "zh'n", 11.937, datetime.datetime(2012, 1, 9)],
    [5, "i\'op", 12.057, datetime.datetime(2009, 5, 18)],
]

# 写文件
with open("test.csv", "w") as file:
    writer = csv.writer(file, dialect="excel")
    # writer.writerows(data)
    for item in data:
        writer.writerow(item)

# 读文件
with open("test.csv", "r") as file:
    reader = csv.reader(file, dialect="excel")
    for item in reader:
        print(item)

# 读文件
with open("test.csv", "r") as file:
    reader = csv.DictReader(file, fieldnames=["id", "name", "float", "datetime"], dialect="excel")
    data = [item for item in reader]
    print(data)

# 写文件
with open("test.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "float", "datetime"], dialect="excel")
    writer.writeheader()
    for item in data:
        writer.writerow(item)
