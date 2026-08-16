"""
Python 控制结构全演示
涵盖: if/elif/else, for, while, break, continue, pass,
      try/except/else/finally, with, match/case, range() 用法
"""

print("=" * 70)
print("一、条件控制: if / elif / else")
print("=" * 70)

score = 85
print(f"成绩 = {score}")

if score >= 90:
    grade = "A (优秀)"
elif score >= 80:
    grade = "B (良好)"
elif score >= 60:
    grade = "C (及格)"
else:
    grade = "D (不及格)"
print(f"  等级: {grade}")

# 嵌套 if
age = 20
has_license = True
print(f"\n年龄={age}, 有驾照={has_license}")
if age >= 18:
    if has_license:
        print("  可以开车")
    else:
        print("  可以考证，但还没有驾照")
else:
    print("  未成年，不能开车")

# 单行 if (三元表达式)
x = 10
result = "正数" if x > 0 else "负数或零"
print(f"\nx={x}, 结果: {result}")

# pass 占位
print("\npass 占位符演示:")
if True:
    pass  # 什么都不做，语法需要


print("\n" + "=" * 70)
print("二、for 循环")
print("=" * 70)

# 基本 for 循环
fruits = ["苹果", "香蕉", "橙子"]
print("遍历列表:")
for fruit in fruits:
    print(f"  - {fruit}")

# 遍历字符串
print("\n遍历字符串 'Python':")
for char in "Python":
    print(f"  {char}")

# 遍历字典
student = {"name": "Alice", "age": 25, "major": "CS"}
print("\n遍历字典 (键值对):")
for key, value in student.items():
    print(f"  {key}: {value}")

# enumerate 带索引遍历
print("\nenumerate 带索引遍历:")
for idx, fruit in enumerate(fruits, start=1):
    print(f"  第{idx}个: {fruit}")

# zip 并行遍历
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
print("\nzip 并行遍历:")
for name, score in zip(names, scores):
    print(f"  {name} 得了 {score} 分")

# for...else (循环正常结束时执行 else)
print("\nfor...else 演示:")
for i in range(3):
    print(f"  循环 {i}")
else:
    print("  循环正常结束 (未被 break 打断)")


print("\n" + "=" * 70)
print("三、while 循环")
print("=" * 70)

# 基本 while
print("基本 while 循环 (1~5):")
i = 1
while i <= 5:
    print(f"  i = {i}")
    i += 1

# while...else
print("\nwhile...else 演示:")
count = 0
while count < 3:
    print(f"  count = {count}")
    count += 1
else:
    print("  while 条件变为 False, 执行 else")

# 无限循环 + break
print("\n无限循环 + break (找到第一个能被7整除的数):")
num = 1
while True:
    if num % 7 == 0:
        print(f"  找到: {num}")
        break
    num += 1


print("\n" + "=" * 70)
print("四、break 与 continue")
print("=" * 70)

# break: 跳出整个循环
print("break 演示 (遇到 '停' 就退出):")
items = ["苹果", "香蕉", "停", "橙子", "西瓜"]
for item in items:
    if item == "停":
        print(f"  遇到 '{item}', break 退出循环")
        break
    print(f"  处理: {item}")

# continue: 跳过本次迭代
print("\ncontinue 演示 (跳过偶数):")
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(f"  奇数: {i}")

# break vs continue 对比
print("\nbreak vs continue 对比:")
print("  break: 彻底跳出循环")
print("  continue: 跳过当前迭代，继续下一次")


print("\n" + "=" * 70)
print("五、循环10次的各种写法")
print("=" * 70)

# 写法1: for + range(10) —— 最常用
print("写法1: for i in range(10)  [最常用]")
for i in range(10):
    print(f"  第 {i + 1}/10 次")
    if i >= 2:  # 只演示前3次，避免输出过多
        print("  ... (省略后续7次)")
        break

# 写法2: while 计数
print("\n写法2: while 计数")
count = 0
while count < 10:
    print(f"  第 {count + 1}/10 次")
    count += 1
    if count >= 3:
        print("  ... (省略后续7次)")
        break

# 写法3: for + range(1, 11) 从1开始
print("\n写法3: for i in range(1, 11)  [从1到10]")
for i in range(1, 11):
    print(f"  第 {i}/10 次")
    if i >= 3:
        print("  ... (省略后续7次)")
        break


print("\n" + "=" * 70)
print("六、range() 函数的所有用法")
print("=" * 70)

# 语法: range(stop) / range(start, stop) / range(start, stop, step)

print("1. 一个参数 range(stop): 0 到 stop-1")
print(f"  range(5)    = {list(range(5))}")
print(f"  range(10)   = {list(range(10))}")
print(f"  range(0)    = {list(range(0))}   (空)")

print("\n2. 两个参数 range(start, stop): start 到 stop-1")
print(f"  range(3, 8) = {list(range(3, 8))}")
print(f"  range(1, 6) = {list(range(1, 6))}   (常用于从1开始)")
print(f"  range(-3, 3)= {list(range(-3, 3))}  (负数也可以)")

print("\n3. 三个参数 range(start, stop, step): 带步长")
print(f"  range(0, 10, 2)  = {list(range(0, 10, 2))}   (步长2)")
print(f"  range(0, 20, 3)  = {list(range(0, 20, 3))}   (步长3)")
print(f"  range(5, 0, -1)  = {list(range(5, 0, -1))}   (负数步长，倒序)")
print(f"  range(10, 0, -2) = {list(range(10, 0, -2))}  (倒序步长2)")

print("\n4. range 在 for 循环中的常见用途")
print("  4a. 循环指定次数: for _ in range(10)")
print("  4b. 生成索引:     for i in range(len(lst))")
lst = ["a", "b", "c"]
for i in range(len(lst)):
    print(f"    index={i}, value={lst[i]}")

print("  4c. 遍历偶数:     for i in range(0, 10, 2)")
print("  4d. 遍历奇数:     for i in range(1, 10, 2)")
print("  4e. 倒序遍历:     for i in range(len(lst)-1, -1, -1)")
for i in range(len(lst) - 1, -1, -1):
    print(f"    index={i}, value={lst[i]}")

print("\n5. range 转换为其他类型")
print(f"  list(range(5))       = {list(range(5))}")
print(f"  tuple(range(3, 7))   = {tuple(range(3, 7))}")
print(f"  set(range(1, 6, 2))  = {set(range(1, 6, 2))}")

print("\n6. range 的特性 (Python 3)")
r = range(0, 100, 7)
print("  range 是惰性的, 不实际存储所有数字:")
print(f"    range(0, 100, 7) 的长度 = {len(r)}")
print(f"    判断 42 in range(0, 100, 7): {42 in r}")
print(f"    判断 43 in range(0, 100, 7): {43 in r}")
print(f"    range 支持索引: range(10)[3] = {range(10)[3]}")
print(f"    range 支持切片: range(10)[2:6] = {list(range(10)[2:6])}")

print("\n7. range 不能做什么")
print("  ❌ range(1, 10, 0)  -> step 不能为 0, 会报 ValueError")
print("  ❌ range(1.5, 5)    -> 参数必须是整数")


print("\n" + "=" * 70)
print("七、try / except / else / finally 异常处理")
print("=" * 70)

# 基本 try/except
print("1. 基本异常捕获:")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  捕获到除零错误!")

# 捕获多个异常
print("\n2. 捕获多种异常:")
try:
    num = int(input("请输入一个数字: ")) if False else int("abc")
except ValueError as e:
    print(f"  捕获 ValueError: {e}")
except TypeError:
    print("  捕获 TypeError")

# try/except/else
print("\n3. try/except/else (无异常时执行 else):")
try:
    val = 42
except Exception:
    print("  有异常")
else:
    print(f"  没有异常, val = {val}")

# try/except/finally
print("\n4. try/except/finally (无论如何都执行):")
try:
    f = None
    raise ValueError("模拟错误")
except ValueError as e:
    print(f"  捕获: {e}")
finally:
    print("  finally 块总是会执行 (常用于清理资源)")

# raise 抛出异常
print("\n5. raise 主动抛出异常:")
try:
    age = -5
    if age < 0:
        raise ValueError("年龄不能为负数")
except ValueError as e:
    print(f"  主动抛出并捕获: {e}")


print("\n" + "=" * 70)
print("八、with 语句 (上下文管理器)")
print("=" * 70)

# with 自动管理资源 (文件操作示例)
print("1. with open() 自动关闭文件:")
with open("temp_demo.txt", "w", encoding="utf-8") as f:
    f.write("Hello, with 语句!\n")
    f.write("自动关闭文件，无需手动 f.close()")
print("  文件已写入并自动关闭")

with open("temp_demo.txt", encoding="utf-8") as f:
    content = f.read()
print(f"  读取内容: {content.strip()}")

# 使用后清理文件
import os

os.remove("temp_demo.txt")
print("  临时文件已清理")

# 多个 with
print("\n2. 同时管理多个资源:")
with open("temp_a.txt", "w") as fa, open("temp_b.txt", "w") as fb:
    fa.write("A 文件")
    fb.write("B 文件")
print("  两个文件都已创建并关闭")

os.remove("temp_a.txt")
os.remove("temp_b.txt")


print("\n" + "=" * 70)
print("九、match / case 模式匹配 (Python 3.10+)")
print("=" * 70)

command = "quit"
print(f"command = '{command}'")

match command:
    case "start":
        print("  启动程序")
    case "stop":
        print("  停止程序")
    case "quit" | "exit":  # 多条件
        print("  退出程序")
    case _:  # 默认分支
        print(f"  未知命令: {command}")

# 带条件的模式匹配
print("\n带条件 (guard) 的模式匹配:")
x = 15
match x:
    case n if n < 0:
        print(f"  {n} 是负数")
    case n if n == 0:
        print(f"  {n} 是零")
    case n if 0 < n < 10:
        print(f"  {n} 是单位数")
    case n if n >= 10:
        print(f"  {n} 是两位数或更大")


print("\n" + "=" * 70)
print("十、控制结构组合实战: FizzBuzz")
print("=" * 70)

print("打印 1~15, 3的倍数说Fizz, 5的倍数说Buzz, 都满足说FizzBuzz:")
for i in range(1, 16):
    if i % 3 == 0 and i % 5 == 0:
        print(f"  {i:2d}: FizzBuzz")
    elif i % 3 == 0:
        print(f"  {i:2d}: Fizz")
    elif i % 5 == 0:
        print(f"  {i:2d}: Buzz")
    else:
        print(f"  {i:2d}: {i}")


print("\n" + "=" * 70)
print("十一、控制结构选择指南")
print("=" * 70)
print("""
┌─────────────────────────────────────────────────────────┐
│  需求                  │  推荐控制结构                  │
├─────────────────────────────────────────────────────────┤
│ 条件判断 (1次)         │  if / elif / else              │
│ 条件判断 (0~N次)       │  while 循环                    │
│ 遍历已知集合           │  for 循环                      │
│ 提前退出循环           │  break                         │
│ 跳过某次循环           │  continue                      │
│ 占位/空实现            │  pass                          │
│ 异常处理               │  try / except / finally        │
│ 资源自动管理           │  with                          │
│ 多值匹配 (3.10+)       │  match / case                  │
│ 循环固定次数           │  for _ in range(N)             │
│ 循环10次               │  for _ in range(10)            │
└─────────────────────────────────────────────────────────┘
""")

print("=" * 70)
print("演示完成！所有 Python 控制结构已覆盖。")
print("=" * 70)
