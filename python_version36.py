# _*_ coding: utf-8 _*_

"""
python_version36.py by xianhu
"""

import asyncio
import decimal
from typing import List, Dict

# Formatted string literals
name = "Fred"
print(f"He said his name is {name}.")  # 'He said his name is Fred.'
print("He said his name is {name}.".format(**locals()))

width = 10
precision = 4
value = decimal.Decimal("12.34567")
print(f"result: {value:{width}.{precision}}")  #'result:      12.35'


# variable annotations
def test(a: List[int], b: int) -> int:
    return a[0] + b
print(test([3, 1], 2))

primes: List[int] = []
captain: str

class Starship(object):
    stats: Dict[str, int] = {}


# Underscores in Numeric Literals
a = 1_000_000_000_000_000       # 1000000000000000
b = 0x_FF_FF_FF_FF              # 4294967295

'{:_}'.format(1000000)          # '1_000_000'
'{:_x}'.format(0xFFFFFFFF)      # 'ffff_ffff'


# Asynchronous Generators
async def ticker(delay, to):
    """Yield numbers from 0 to *to* every *delay* seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


# Asynchronous Comprehensions
result = [i async for i in aiter() if i % 2]
result = [await fun() for fun in funcs if await condition()]
