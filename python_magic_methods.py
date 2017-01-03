# _*_ coding: utf-8 _*_

"""
python_magic_methods.py by xianhu
"""


# 定义一个能够自动比较大小的People类
class People(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        return

    def __str__(self):
        return self.name + ":" + str(self.age)

    def __lt__(self, other):
        return self.name < other.name if self.name != other.name else self.age < other.age

print("\t".join([str(item) for item in sorted([People("abc", 18), People("abe", 19), People("abe", 12), People("abc", 17)])]))


# Python实现任意深度的赋值 例如a[0] = 'value1'; a[1][2] = 'value2'; a[3][4][5] = 'value3'
class MyDict(dict):

    def __setitem__(self, key, value):          # 该函数不做任何改动 这里只是为了输出
        print("setitem:", key, value, self)
        super().__setitem__(key, value)
        return

    def __getitem__(self, item):                # 主要技巧在该函数
        print("getitem:", item, self)
        # 基本思路: a[1][2]赋值时 需要先取出a[1] 然后给a[1]的[2]赋值
        if item not in self:                    # 如果a[1]不存在
            temp = MyDict()                     # 则需要新建一个dict
            super().__setitem__(item, temp)     # 并使得a[1] = dict
            return temp                         # 返回a[1] 使得a[1][2] = value有效
        return super().__getitem__(item)        # 如果a[1]存在 则直接返回a[1]

# 使用例子:
test = MyDict()
test[0] = 'test'
test[1][2] = 'test1'
test[3][4][5] = 'test2'
print("==========================")
