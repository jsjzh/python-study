"""
Python 全运算符演示
涵盖: 算术、比较、赋值、逻辑、位、成员、身份、海象、序列、矩阵等运算符
"""


def demo(title: str, a, b):
    """格式化输出二元运算演示"""
    print(f"  {a} {title} {b} = ", end="")


print("=" * 70)
print("一、算术运算符")
print("=" * 70)

a, b = 17, 5
print(f"操作数: a = {a}, b = {b}")
print(f"  a + b  = {a + b}")  # 加法
print(f"  a - b  = {a - b}")  # 减法
print(f"  a * b  = {a * b}")  # 乘法
print(f"  a / b  = {a / b}")  # 除法（结果为 float）
print(f"  a // b = {a // b}")  # 整除（向下取整）
print(f"  a % b  = {a % b}")  # 取余
print(f"  a ** b = {a**b}")  # 幂运算
print(f"  +a     = {+a}")  # 正号
print(f"  -a     = {-a}")  # 负号
print(f"  ~a     = {~a}")  # 按位取反

# 浮点运算
x, y = 3.5, 2.1
print(f"\n浮点数: x = {x}, y = {y}")
print(f"  x + y  = {x + y}")
print(f"  x - y  = {x - y}")
print(f"  x * y  = {x * y}")
print(f"  x / y  = {x / y}")
print(f"  x // y = {x // y}")
print(f"  x % y  = {x % y}")

# 复数运算
c1, c2 = 3 + 4j, 1 - 2j
print(f"\n复数: c1 = {c1}, c2 = {c2}")
print(f"  c1 + c2 = {c1 + c2}")
print(f"  c1 - c2 = {c1 - c2}")
print(f"  c1 * c2 = {c1 * c2}")
print(f"  c1 / c2 = {c1 / c2}")


print("\n" + "=" * 70)
print("二、比较运算符")
print("=" * 70)

a, b = 10, 20
print(f"操作数: a = {a}, b = {b}")
print(f"  a == b  = {a == b}")  # 等于
print(f"  a != b  = {a != b}")  # 不等于
print(f"  a >  b  = {a > b}")  # 大于
print(f"  a <  b  = {a < b}")  # 小于
print(f"  a >= b  = {a >= b}")  # 大于等于
print(f"  a <= b  = {a <= b}")  # 小于等于

# 链式比较
x = 15
print(f"\n链式比较: x = {x}")
print(f"  10 < x < 20  = {10 < x < 20}")  # Python 独有写法
print(f"  10 < x <= 15 = {10 < x <= 15}")

# 字符串比较（按字典序）
print("\n字符串比较:")
print(f"  'abc' < 'abd' = {'abc' < 'abd'}")
print(f"  'ABC' < 'abc' = {'ABC' < 'abc'}")  # 小写字母 ASCII 更大


print("\n" + "=" * 70)
print("三、赋值运算符")
print("=" * 70)

x = 10
print(f"初始 x = {x}")
x += 5
print(f"  x += 5  -> x = {x}")  # 加赋值
x -= 3
print(f"  x -= 3  -> x = {x}")  # 减赋值
x *= 2
print(f"  x *= 2  -> x = {x}")  # 乘赋值
x /= 4
print(f"  x /= 4  -> x = {x}")  # 除赋值
x //= 2
print(f"  x //= 2 -> x = {x}")  # 整除赋值
x %= 3
print(f"  x %= 3  -> x = {x}")  # 取余赋值
x **= 2
print(f"  x **= 2 -> x = {x}")  # 幂赋值

# 位运算赋值
x = 0b1100  # 12
print(f"\n位运算赋值 (x = {x} = 0b1100):")
x &= 0b1010
print(f"  x &= 0b1010  -> {x} (0b{x:04b})")  # 与赋值
x |= 0b0101
print(f"  x |= 0b0101  -> {x} (0b{x:04b})")  # 或赋值
x ^= 0b1111
print(f"  x ^= 0b1111  -> {x} (0b{x:04b})")  # 异或赋值
x <<= 2
print(f"  x <<= 2      -> {x} (0b{x:04b})")  # 左移赋值
x >>= 1
print(f"  x >>= 1      -> {x} (0b{x:04b})")  # 右移赋值


print("\n" + "=" * 70)
print("四、逻辑运算符")
print("=" * 70)

p, q = True, False
print(f"操作数: p = {p}, q = {q}")
print(f"  p and q = {p and q}")  # 与
print(f"  p or  q = {p or q}")  # 或
print(f"  not p   = {not p}")  # 非
print(f"  not q   = {not q}")

# 短路求值演示
print("\n短路求值:")
print("  False and 1/0 = ", end="")
try:
    result = False and 1 / 0
    print(f"{result}  (未触发除零错误)")
except ZeroDivisionError:
    print("ZeroDivisionError!")

print("  True or 1/0   = ", end="")
try:
    result = True or 1 / 0
    print(f"{result}  (未触发除零错误)")
except ZeroDivisionError:
    print("ZeroDivisionError!")

# and / or 返回操作数本身
print("\nand/or 返回值特性:")
print(f"  3 and 5  = {3 and 5}")  # 返回最后一个真值
print(f"  0 and 5  = {0 and 5}")  # 返回第一个假值
print(f"  3 or  5  = {3 or 5}")  # 返回第一个真值
print(f"  0 or  5  = {0 or 5}")  # 返回最后一个假值


print("\n" + "=" * 70)
print("五、位运算符")
print("=" * 70)

a, b = 0b1100, 0b1010  # 12, 10
print(f"操作数: a = {a} (0b{a:04b}), b = {b} (0b{b:04b})")
print(f"  a & b  = {a & b}  (0b{a & b:04b})")  # 按位与
print(f"  a | b  = {a | b}  (0b{a | b:04b})")  # 按位或
print(f"  a ^ b  = {a ^ b}  (0b{a ^ b:04b})")  # 按位异或
print(f"  ~a     = {~a}")  # 按位取反
print(f"  a << 2 = {a << 2}  (0b{a << 2:06b})")  # 左移
print(f"  a >> 1 = {a >> 1}  (0b{a >> 1:04b})")  # 右移

# 负数位运算
x = -1
print(f"\n负数位运算: x = {x}")
print(f"  ~x      = {~x}")
print(f"  x << 2  = {x << 2}")
print(f"  x >> 1  = {x >> 1}")


print("\n" + "=" * 70)
print("六、成员运算符")
print("=" * 70)

lst = [1, 2, 3, 4, 5]
print(f"列表: lst = {lst}")
print(f"  3 in lst     = {3 in lst}")
print(f"  9 in lst     = {9 in lst}")
print(f"  3 not in lst = {3 not in lst}")
print(f"  9 not in lst = {9 not in lst}")

# 字符串成员
s = "Hello, Python!"
print(f"\n字符串: s = '{s}'")
print(f"  'Python' in s     = {'Python' in s}")
print(f"  'Java' not in s   = {'Java' not in s}")

# 字典成员（检查键）
d = {"name": "Alice", "age": 25}
print(f"\n字典: d = {d}")
print(f"  'name' in d    = {'name' in d}")  # 检查键
print(f"  'Alice' in d   = {'Alice' in d}")  # 只检查键，不检查值


print("\n" + "=" * 70)
print("七、身份运算符")
print("=" * 70)

a = [1, 2, 3]
b = [1, 2, 3]
c = a
print(f"a = {a}, b = {b}, c = a")
print(f"  a is b     = {a is b}")  # 不同对象，值相同 -> False
print(f"  a is c     = {a is c}")  # 同一对象 -> True
print(f"  a == b     = {a == b}")  # 值相等 -> True
print(f"  a is not b = {a is not b}")
print(f"  c is not b = {c is not b}")

# None 的判断
x = None
print(f"\nx = {x}")
print(f"  x is None     = {x is None}")  # 推荐写法
print(f"  x is not None = {x is not None}")

# 小整数缓存（-5~256）
print("\n小整数缓存:")
a256, b256 = 256, 256
a257, b257 = 257, 257
neg5a, neg5b = -5, -5
neg6a, neg6b = -6, -6
print(f"  a=256, b=256; a is b = {a256 is b256}")  # True
print(f"  a=257, b=257; a is b = {a257 is b257}")  # False (通常)
print(f"  a=-5,  b=-5;  a is b = {neg5a is neg5b}")  # True
print(f"  a=-6,  b=-6;  a is b = {neg6a is neg6b}")  # False (通常)


print("\n" + "=" * 70)
print("八、海象运算符 (Walrus Operator) := )")
print("=" * 70)

# 基本用法
print("基本赋值表达式:")
n = (x := 10)
print(f"  n = (x := 10)  -> n={n}, x={x}")

# 在 if 中使用
print("\n在 if 中使用 (避免重复调用):")
import re

text = "Python 3.8 引入了海象运算符"
if match := re.search(r"\d+\.\d+", text):
    print(f"  找到版本号: {match.group()}")

# 在 while 循环中使用
print("\n在 while 循环中使用:")
data = [1, 2, 3, 4, 5, 0, 6, 7]
idx = 0
results = []
while (val := data[idx]) != 0:
    results.append(val)
    idx += 1
print(f"  处理到 0 停止, 结果: {results}")

# 在列表推导式中使用
print("\n在列表推导式中使用 (复用计算结果):")
import math

nums = [1, 4, 9, 16, 25]
result = [sqrt for n in nums if (sqrt := math.sqrt(n)) > 3]
print(f"  平方数列表 {nums}, 平方根 > 3 的: {result}")


print("\n" + "=" * 70)
print("九、三元条件运算符")
print("=" * 70)

score = 85
print(f"score = {score}")
grade = "优秀" if score >= 90 else "良好" if score >= 80 else "及格" if score >= 60 else "不及格"
print(f"  成绩等级: {grade}")

# 嵌套三元
a, b = 10, 20
max_val = a if a > b else b
print(f"\na = {a}, b = {b}")
print(f"  max(a, b) = {max_val}")

# 三元在表达式中
x = 5
print(f"\nx = {x}")
print(f"  x 的绝对值: {-x if x < 0 else x}")


print("\n" + "=" * 70)
print("十、序列/字符串运算符")
print("=" * 70)

# 字符串拼接与重复
print("字符串:")
print(f"  'Hello' + ' ' + 'World' = {'Hello' + ' ' + 'World'}")
print(f"  'Ha' * 3                = {'Ha' * 3}")

# 列表拼接与重复
la, lb = [1, 2], [3, 4]
print("\n列表:")
print(f"  [1,2] + [3,4] = {la + lb}")
print(f"  [0] * 4       = {[0] * 4}")

# 索引与切片
s = "Python"
print(f"\n字符串索引/切片: s = '{s}'")
print(f"  s[0]    = {s[0]}")  # 正向索引
print(f"  s[-1]   = {s[-1]}")  # 负向索引
print(f"  s[1:4]  = {s[1:4]}")  # 切片 [start:end]
print(f"  s[:3]   = {s[:3]}")  # 省略起始
print(f"  s[2:]   = {s[2:]}")  # 省略结束
print(f"  s[::2]  = {s[::2]}")  # 步长 2
print(f"  s[::-1] = {s[::-1]}")  # 反转

# 列表切片
lst = [0, 1, 2, 3, 4, 5]
print(f"\n列表切片: lst = {lst}")
print(f"  lst[1:4]    = {lst[1:4]}")
print(f"  lst[::2]    = {lst[::2]}")
print(f"  lst[::-1]   = {lst[::-1]}")

# 成员测试 (再强调)
print("\n序列成员测试:")
print(f"  'yt' in 'Python' = {'yt' in 'Python'}")


print("\n" + "=" * 70)
print("十一、矩阵乘法运算符 @")
print("=" * 70)

import numpy as np

# 二维矩阵
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(f"矩阵 A = \n{A}")
print(f"矩阵 B = \n{B}")
C = A @ B
print(f"A @ B (矩阵乘法) = \n{C}")

# 一维矩阵(向量)点积
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print(f"\n向量 v1 = {v1}")
print(f"向量 v2 = {v2}")
print(f"v1 @ v2 (点积) = {v1 @ v2}  (等于 1*4 + 2*5 + 3*6 = 32)")


print("\n" + "=" * 70)
print("十二、运算符优先级速查（从高到低）")
print("=" * 70)

print("""
优先级  运算符                  示例
─────────────────────────────────────────────────────────────
1 (最高)  ()  []  .             括号、索引、属性
2        **                   幂运算
3        +x  -x  ~x           单目正/负/取反
4        *  /  //  %          乘/除/整除/取余
5        +  -                 加/减
6        <<  >>               位移动
7        &                    按位与
8        ^                    按位异或
9        |                    按位或
10       ==  !=  >  <  >=  <=  比较
11       is  is not  in  not in 身份/成员
12       not                  逻辑非
13       and                  逻辑与
14       or                   逻辑或
15       if/else              条件表达式
16       :=                   海象运算符
17 (最低) =  +=  -=  ...      赋值运算符
""")

print("\n优先级演示:")
a, b, c = 2, 3, 4
result1 = a + b * c  # 先乘后加
result2 = (a + b) * c  # 用括号改变优先级
print(f"  a + b * c = {a} + {b} * {c} = {result1}")
print(f"  (a + b) * c = ({a} + {b}) * {c} = {result2}")

print(f"\n  2 ** 3 ** 2 = {2**3**2}   (指数右结合: 3**2=9, 2**9=512)")
print(f"  -2 ** 2 = {-(2**2)}    (指数优先级高于负号: -(2**2)=-4)")
print(f"  (-2) ** 2 = {(-2) ** 2}")


print("\n" + "=" * 70)
print("十三、其他特殊运算符")
print("=" * 70)

# 赋值解包
print("解包赋值:")
a, b, c = 1, 2, 3
print(f"  a, b, c = 1, 2, 3  -> a={a}, b={b}, c={c}")

# 交换变量
a, b = 10, 20
print("\n交换变量:")
print(f"  交换前: a={a}, b={b}")
a, b = b, a
print(f"  交换后: a={a}, b={b}")

# 星号解包
first, *rest = [1, 2, 3, 4, 5]
print("\n星号解包:")
print("  first, *rest = [1,2,3,4,5]")
print(f"    first = {first}, rest = {rest}")

*init, last = [1, 2, 3, 4, 5]
print("  *init, last = [1,2,3,4,5]")
print(f"    init = {init}, last = {last}")

first, *mid, last = [1, 2, 3, 4, 5]
print("  first, *mid, last = [1,2,3,4,5]")
print(f"    first = {first}, mid = {mid}, last = {last}")

# 字典解包合并
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
merged = {**d1, **d2}
print("\n字典解包合并:")
print(f"  {{**d1, **d2}} = {merged}")

# 集合解包合并
s1 = {1, 2}
s2 = {3, 4}
merged_set = {*s1, *s2}
print(f"  {{*s1, *s2}} = {merged_set}")


print("\n" + "=" * 70)
print("演示完成！涵盖所有 Python 运算符。")
print("=" * 70)
