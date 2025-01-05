import re

#-- 基本正则表达式语法
'''
.：匹配除换行符以外的任意字符。
^：匹配字符串的开始。
$：匹配字符串的结束。
*：匹配前一个字符0次或多次。
+：匹配前一个字符1次或多次。
?：匹配前一个字符0次或1次。
{m}：匹配前一个字符m次。
{m,n}：匹配前一个字符至少m次，至多n次。
[abc]：匹配字符集合中的任意一个字符（例如a、b或c）。
[^abc]：匹配不在字符集合中的任意字符。
|：表示“或”关系，匹配符号前后的任意一个表达式。
()：用于分组，可以提取匹配的部分。
\d：匹配任意数字，等价于[0-9]。
\D：匹配任意非数字字符，等价于[^0-9]。
\w：匹配任意字母数字字符，包括下划线，等价于[a-zA-Z0-9_]。
\W：匹配任意非字母数字字符，等价于[^a-zA-Z0-9_]。
\s：匹配任意空白字符，包括空格、制表符、换行符等。
\S：匹配任意非空白字符。
'''

#-- re 模块的主要函数
re.match(pattern, string, flags=0)                # 尝试从字符串的起始位置匹配正则表达式，如果匹配成功，返回一个匹配对象；否则返回None。
re.search(pattern, string, flags=0)               # 扫描整个字符串，返回第一个成功匹配的对象；否则返回None。
re.findall(pattern, string, flags=0)              # 在字符串中找到所有与正则表达式匹配的非重叠匹配项，并返回一个列表。
re.finditer(pattern, string, flags=0)             # 与findall类似，但返回的是一个迭代器，每个迭代元素都是一个匹配对象。
re.sub(pattern, repl, string, count=0, flags=0)   # 使用repl替换string中所有与pattern匹配的子串，count表示替换的最大次数。
re.subn(pattern, repl, string, count=0, flags=0)  # 功能与sub相同，但返回一个元组，包含替换后的字符串和替换的总次数。
re.split(pattern, string, maxsplit=0, flags=0)    # 根据正则表达式的模式分割字符串，maxsplit表示分割的最大次数。
re.escape(string)                                 # 对字符串中的非字母数字字符进行转义，使其可以安全地用于正则表达式中。

#-- 示例代码1
# 匹配字符串的开始  
match_obj = re.match(r'^Hello', 'Hello World')  
if match_obj:  
    print("Match found:", match_obj.group())  
else:  
    print("No match")  
  
# 搜索字符串  
search_obj = re.search(r'World', 'Hello World')  
if search_obj:  
    print("Search found:", search_obj.group())  
else:  
    print("No search match")  
  
# 查找所有匹配项  
findall_result = re.findall(r'\d+', 'There are 42 apples and 33 oranges')  
print("Findall result:", findall_result)  
  
# 替换匹配项  
sub_result = re.sub(r'\d+', 'many', 'There are 42 apples and 33 oranges')  
print("Sub result:", sub_result)  
  
# 分割字符串  
split_result = re.split(r'\s+', 'Hello World this is Python')  
print("Split result:", split_result)  
  
# 转义字符串  
escaped_string = re.escape('Hello? World!')  
print("Escaped string:", escaped_string)

#-- 标志位（flags）
re.IGNORECASE                # 忽略大小写。
re.MULTILINE                 # 多行模式，改变^和$的行为。
re.DOTALL                    # 让.匹配包括换行符在内的所有字符。
re.VERBOSE                   # 允许正则表达式包含空白和注释，使其更易于阅读。

#-- 示例代码2
pattern = re.compile(r'''  
    \d+  # 匹配一个或多个数字  
    \.   # 匹配小数点  
    \d+  # 匹配一个或多个数字  
''', re.VERBOSE)  
  
match_obj = pattern.match('123.456')  
if match_obj:  
    print("Match found:", match_obj.group())  
else:  
    print("No match")