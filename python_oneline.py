# _*_ coding: utf-8 _*_

"""
python_oneline.py by xianhu
"""


# 首先来个python之禅
# python -c "import this"
"""
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""


# 一行代码启动一个Web服务
# python -m SimpleHTTPServer 8080
# python3 -m http.server 8080


# 一行代码实现变量值互换
a, b = 1, 2; a, b = b, a


# 一行代码解决FizzBuzz问题: 打印数字1到100, 3的倍数打印“Fizz”来替换这个数, 5的倍数打印“Buzz”, 既是3又是5的倍数的打印“FizzBuzz”
print(' '.join(["fizz"[x % 3 * 4:]+"buzz"[x % 5 * 4:] or str(x) for x in range(1, 101)]))


# 一行代码输出特定字符"Love"拼成的心形
print('\n'.join([''.join([('Love'[(x-y) % len('Love')] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))


# 一行代码输出Mandelbrot图像: Mandelbrot图像中的每个位置都对应于公式N=x+y*i中的一个复数
print('\n'.join([''.join(['*'if abs((lambda a: lambda z, c, n: a(a, z, c, n))(lambda s, z, c, n: z if n == 0 else s(s, z*z+c, c, n-1))(0, 0.02*x+0.05j*y, 40)) < 2 else ' ' for x in range(-80, 20)]) for y in range(-20, 20)]))


# 一行代码打印九九乘法表
print('\n'.join([' '.join(['%s*%s=%-2s' % (y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))


# 一行代码计算出1-100之间的素数(两个版本)
print(' '.join([str(item) for item in filter(lambda x: not [x % i for i in range(2, x) if x % i == 0], range(2, 101))]))
print(' '.join([str(item) for item in filter(lambda x: all(map(lambda p: x % p != 0, range(2, x))), range(2, 101))]))


# 一行代码输出斐波那契数列
print([x[0] for x in [(a[i][0], a.append([a[i][1], a[i][0]+a[i][1]])) for a in ([[1, 1]], ) for i in range(30)]])


# 一行代码实现快排算法
qsort = lambda arr: len(arr) > 1 and qsort(list(filter(lambda x: x <= arr[0], arr[1:]))) + arr[0:1] + qsort(list(filter(lambda x: x > arr[0], arr[1:]))) or arr


# 一行代码解决八皇后问题
[__import__('sys').stdout.write('\n'.join('.' * i + 'Q' + '.' * (8-i-1) for i in vec) + "\n========\n") for vec in __import__('itertools').permutations(range(8)) if 8 == len(set(vec[i]+i for i in range(8))) == len(set(vec[i]-i for i in range(8)))]


# 一行代码实现数组的flatten功能: 将多维数组转化为一维
flatten = lambda x: [y for l in x for y in flatten(l)] if isinstance(x, list) else [x]


# 一行代码实现list, 有点类似与上个功能的反功能
array = lambda x: [x[i:i+3] for i in range(0, len(x), 3)]


# 一行代码实现求解2的1000次方的各位数之和
print(sum(map(int, str(2**1000))))


# 最后推荐一篇文章: [Python One-liner Games](http://arunrocks.com/python-one-liner-games/)
exit()
