# _*_ coding: utf-8 _*_

from fn import _
from operator import add
from functools import partial, reduce

# 列表解析
a_list = [item**2 for item in range(5)]
print(a_list)

# 字典解析
a_dict = {"%d^2" % item: item**2 for item in range(5)}
print(a_dict)

# 生成器
a_generator = (item**2 for item in range(5))
print(a_generator)
print(next(a_generator))
print(next(a_generator))

# iter函数和next函数
a_list_generator = iter(a_list)
print(next(a_list_generator))
print(next(a_list_generator))
print(type(a_list), type(a_list_generator))

# lambda表达式
a_func = lambda x, y: x**y
print(a_func(2, 3))

# map函数
print(map(abs, range(-4, 5)))
print(list(map(abs, range(-4, 5))))
print(list(map(lambda x: x**2, range(5))))
print(list(map(lambda x, y: x**y, range(1, 5), range(1, 5))))

# reduce函数
print(reduce(lambda x, y: x+y, range(10)))
print(reduce(lambda x, y: x+y, range(10), 100))
print(reduce(lambda x, y: x+y, [[1, 2], [3, 4]], [0]))

# filter函数
print(filter(None, range(-4, 5)))
print(list(filter(None, range(-4, 5))))
print(list(filter(lambda x: x > 0, range(-4, 5))))

# all、any函数
print(all([0, 1, 2]))
print(any([0, 1, 2]))

# enumerate函数
for index, item in enumerate(range(5)):
    print("%d: %d" % (index, item))

# zip函数
for a, b in zip([1, 2, 3], ["a", "b", "c"]):
    print(a, b)
a_dict = dict(zip([1, 2, 3], ["a", "b", "c"]))
print(a_dict)

# partial函数
print(int("10010", base=2))
int_base_2 = partial(int, base=2)
print(int_base_2("10010"))

# operator.add函数
print(reduce(lambda x, y: x+y, range(10)))
print(reduce(add, range(10)))

# fn的使用
add_func_1 = (_ + 2)
print(add_func_1(1))
add_func_2 = (_ + _ * _)
print(add_func_2(1, 2, 3))
