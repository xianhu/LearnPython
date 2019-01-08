# _*_ coding: utf-8 _*_

"""
app4数据
"""

import pandas as pd
from collections import OrderedDict

# 全局变量
data = OrderedDict([
    ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
    ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
    ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
    ("Humidity", [10, 20, 30, 40, 50, 60]),
    ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
])
df_data = pd.DataFrame(data)

election_data = OrderedDict([
    (
        "Date", [
            "July 12th, 2013 - July 25th, 2013",
            "July 12th, 2013 - August 25th, 2013",
            "July 12th, 2014 - August 25th, 2014",
        ]
    ),
    (
        "Election Polling Organization", ["The New York Times", "Pew Research", "The Washington Post"]
    ),
    (
        "Rep", [1, -20, 3.512]
    ),
    (
        "Dem", [10, 20, 30]),
    (
        "Ind", [2, 10924, 3912]
    ),
    (
        "Region", [
            "Northern New York State to the Southern Appalachian Mountains",
            "Canada",
            "Southern Vermont",
        ]
    ),
])
df_election = pd.DataFrame(election_data)

# 行数增加到30行
df_large = pd.DataFrame(OrderedDict([(name, col_data * 10) for (name, col_data) in election_data.items()]))

# 每一列增加长度
df_long = pd.DataFrame(OrderedDict([(name, [item * 3 for item in col_data]) for (name, col_data) in election_data.items()]))
