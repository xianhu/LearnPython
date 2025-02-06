# _*_ coding: utf-8 _*_

"""
Arrow ---- the best python time package I ever used, by Ningbo Yu.
First you need get arrow package ready by: pip install arrow
Doc reference: https://arrow.readthedocs.io/en/latest/
"""

# Let's begin with import
import arrow
from datetime import datetime

now = arrow.now()  # Get current time with now
print(now)  # Get an arrow object: 2021-11-10T10:41:46.963759+08:00
utc_now = arrow.utcnow()  # Get UTC current time with now
print(utc_now)  # Get an arrow object: 2021-11-10TT10:41:46.963759+00:00
us_pacific_now = arrow.now('US/Pacific')  # Get current time of a specific time zone, pass a timezone to now()
us_pacific_now_other_way = arrow.now('-07:00')  # Same as arrow.now('US/Pacific')


########################################################
# Create arrow object from string, datetime object, int
########################################################
date_str = '2021-10-10'
arrow_obj_0 = arrow.get(date_str)
print(arrow_obj_0)  # Get an arrow object: 2021-10-10T00:00:00+00:00
arrow_obj_1 = arrow.get(date_str, tzinfo='US/Pacific')  # Specify time zone

complex_date_str = 'June was born in May 1980'
# For complex date string, you need to tell arrow how to parse by passing date format to get()
# For date format reference see https://arrow.readthedocs.io/en/latest/ (Search 'Supported Tokens')
arrow_obj_2 = arrow.get(complex_date_str, 'MMMM YYYY')
# Create from a datetime object, if you are addicted to datetime package.
datetime_obj = datetime.utcnow()
arrow_obj_3 = arrow.get(datetime_obj)
print(arrow_obj_3)  # Get an arrow object: 2021-11-10T03:40:35.912181+00:00
# Create from a timestamp
current_timestamp = 1636515897
arrow_obj_4 = arrow.get(current_timestamp)


#######################################################################
# Powerful arrow functions, what makes arrow the best python time package
#######################################################################
arrow_obj = arrow.now()  # Output: <Arrow [2021-11-10T10:41:46.963759+08:00]>
timestamp = arrow_obj.timestamp  # Get the timestamp from an arrow obj
print(timestamp)  # Output: 1636512106
# Convert arrow obj to datetime obj
datetime_obj = arrow_obj.datetime
# Output: datetime.datetime(2021, 11, 10, 10, 41, 46, 963759, tzinfo=tzoffset(None, 28800))

# Shift forward or backward, much more easier to use than datetime package
yesterday = arrow_obj.shift(days=-1)  # Output: <Arrow [2021-11-09T10:41:46.963759+08:00]>
tomorrow = arrow_obj.shift(days=1)  # Output: <Arrow [2021-11-11T10:41:46.963759+08:00]>
a_month_ago = arrow_obj.shift(months=-1)  # Output: <Arrow [2021-10-10T10:41:46.963759+08:00]>
a_month_after = arrow_obj.shift(months=1)  # Output: <Arrow [2021-12-10T10:41:46.963759+08:00]>
# Notes: a negative value means shift backward, a positive one is forward.
# Besides days, months, you can also shift years/weeks/hours/minutes/seconds backward or forward.

# Get general attributes from arrow object
year = arrow_obj.year  # Output: 2021
month = arrow_obj.month  # Output: 11
week = arrow_obj.week  # Output: 45
day = arrow_obj.day  # Output: 10
hour = arrow_obj.hour  # Output: 10
minute = arrow_obj.minute  # Output: 41
second = arrow_obj.second  # Output: 46

# Floor and ceil
# Get the begin of the day
day_begin = arrow_obj.floor('day')  # Output: <Arrow [2021-11-10T00:00:00+08:00]>
day_end = arrow_obj.ceil('day')  # Output: <Arrow [2021-11-10T23:59:59.999999+08:00]>
# You can get the very beginning of the year or month by:
year_begin = arrow_obj.floor('year')
month_begin = arrow_obj.floor('month')
# and where the year and month ends:
year_end = arrow_obj.ceil('year')
month_end = arrow_obj.ceil('month')

# Timezone conversation
# If you want to get all timezones use the codes below:
import pytz
print(pytz.all_timezones)
# Convert UTC to US/Pacific
utc_time = arrow.utcnow()
pacific_time = utc_time.to('US/Pacific')
# Convert UTC to Asia/Shanghai
shanghai_time = utc_time.to('Asia/Shanghai')
# Convert UTC to local
local_time = utc_time.to('local')

# Replace
# If you want to replace any part(year/month/day/hour/minute/second/tzinfo) with any other value, using replace:
# Replace hour and day
present = arrow.now()
replace_d_h = present.replace(day=6, hour=6)
# Replace month and second
replace_m_s = present.replace(month=1, second=10)
# Replace the timezone without changing other attributes
replace_tz = present.replace(tzinfo='US/Pacific')

# Convert arrow obj to string
present.format('YYYY-MM-DD HH:mm:ss ZZ')  # Output: 2021-11-10 10:50:13 +08:00
present.format('YYYY-MM-DD HH:mm:ss')  # Output: 2021-11-10 10:50:13
present.format('YYYY-MM-DD')  # Output: 2021-11-10
# Just pass the format to format function to get any format you want

# Ranges & Spans
print(arrow.now().span('hour'))
# Output: (<Arrow [2021-11-11T10:00:00+08:00]>, <Arrow [2021-11-11T10:59:59.999999+08:00]>)
print(arrow.now().span('day'))
# Output: (<Arrow [2021-11-11T00:00:00+08:00]>, <Arrow [2021-11-11T23:59:59.999999+08:00]>)
print(arrow.now().span('week'))
# Output: (<Arrow [2021-11-08T00:00:00+08:00]>, <Arrow [2021-11-14T23:59:59.999999+08:00]>)
print(arrow.now().span('month'))
# Output: (<Arrow [2021-11-01T00:00:00+08:00]>, <Arrow [2021-11-30T23:59:59.999999+08:00]>)
print(arrow.now().span('year'))
# Output: (<Arrow [2021-01-01T00:00:00+08:00]>, <Arrow [2021-12-31T23:59:59.999999+08:00]>)

# Using range to generate dates in a specific date range
# To get dates between 2020-10-05 and 2020-10-12
begin = arrow.get('2020-10-05')
end = arrow.get('2020-10-12')
day_range = arrow.Arrow.range('day', begin, end)
print(list(day_range))
"""
Output: 
[
<Arrow [2020-10-05T00:00:00+00:00]>, <Arrow [2020-10-06T00:00:00+00:00]>, 
<Arrow [2020-10-07T00:00:00+00:00]>, <Arrow [2020-10-08T00:00:00+00:00]>, <Arrow [2020-10-09T00:00:00+00:00]>, 
<Arrow [2020-10-10T00:00:00+00:00]>, <Arrow [2020-10-11T00:00:00+00:00]>, <Arrow [2020-10-12T00:00:00+00:00]>
]
"""
# You can get second/minute/hour/week/month/year range in the same way
week_range = arrow.Arrow.range('week', begin, end)
print(list(week_range))
"""
Output:
[<Arrow [2020-10-05T00:00:00+00:00]>, <Arrow [2020-10-12T00:00:00+00:00]>]
"""
# Using span_range to generate span in a specific date range
day_span = arrow.Arrow.span_range('day', begin, end)
print(list(day_span))
"""
Output:
[
(<Arrow [2020-10-05T00:00:00+00:00]>, <Arrow [2020-10-05T23:59:59.999999+00:00]>),
 (<Arrow [2020-10-06T00:00:00+00:00]>, <Arrow [2020-10-06T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-07T00:00:00+00:00]>, <Arrow [2020-10-07T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-08T00:00:00+00:00]>, <Arrow [2020-10-08T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-09T00:00:00+00:00]>, <Arrow [2020-10-09T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-10T00:00:00+00:00]>, <Arrow [2020-10-10T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-11T00:00:00+00:00]>, <Arrow [2020-10-11T23:59:59.999999+00:00]>), 
 (<Arrow [2020-10-12T00:00:00+00:00]>, <Arrow [2020-10-12T23:59:59.999999+00:00]>)
]
"""
week_span = arrow.Arrow.span_range('week', begin, end)
print(list(week_span))
"""
Output:
[
(<Arrow [2020-10-05T00:00:00+00:00]>, <Arrow [2020-10-11T23:59:59.999999+00:00]>), 
(<Arrow [2020-10-12T00:00:00+00:00]>, <Arrow [2020-10-18T23:59:59.999999+00:00]>)
]
"""
month_span = arrow.Arrow.span_range('month', begin, end)
print(list(month_span))
"""
Output:
[(<Arrow [2020-10-01T00:00:00+00:00]>, <Arrow [2020-10-31T23:59:59.999999+00:00]>)]
"""