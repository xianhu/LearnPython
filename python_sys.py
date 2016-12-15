# _*_ coding: utf-8 _*_
import sys
"""sys模块详细"""

sys.argv            # 获得脚本的参数

sys.path            # 查找扩展模块(Python源模块, 编译模块,或者二进制扩展)目录 

sys.builtin_module_names    # 查找内建模块

sys.modules                 # 查找已导入的模块
sys.modules.keys()

sys.platform                # 返回当前平台 出现如： "win32" "linux2" "darwin"等

sys.stdout                  # stdout 是一个类文件对象；调用它的 write 函数可以打印出你给定的任何字符串 stdout 和 stderr 都是类文件对象，但是它们都是只写的。
它们都没有 read 方法，只有 write 方法
sys.stdout.write("hello")
sys.stderr
sys.stdin 

sys.exit(1)



__import__("module_name")   # 查找模块输出模块路径
