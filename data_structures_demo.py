# -*- coding: utf-8 -*-
"""
Python 数据结构增删改查 (CRUD) 全演示
涵盖: list, tuple, dict, set, frozenset, str, bytes, bytearray
"""


def section(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title: str) -> None:
    print(f"\n  --- {title} ---")


# ================================================================
# 一、列表 list (有序、可变、允许重复)
# ================================================================
section("一、列表 list — 有序可变序列")

# 1.1 创建 (Create)
subsection("创建列表")
lst = [1, 2, 3]
print(f"  字面量:   {lst}")
lst2 = list([1, 2, 3])
print(f"  list():  {lst2}")
lst3 = [0] * 5
print(f"  乘法:    {lst3}")
lst4 = [i**2 for i in range(5)]
print(f"  推导式:  {lst4}")

# 1.2 读取 (Read)
subsection("读取元素")
fruits = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']
print(f"  fruits = {fruits}")
print(f"  索引 [0]:      {fruits[0]}")       # 第一个
print(f"  索引 [-1]:     {fruits[-1]}")      # 最后一个
print(f"  切片 [1:3]:    {fruits[1:3]}")     # 第2~3个
print(f"  切片 [:3]:     {fruits[:3]}")      # 前3个
print(f"  切片 [2:]:     {fruits[2:]}")      # 第3个到末尾
print(f"  切片 [::2]:    {fruits[::2]}")     # 步长2
print(f"  切片 [::-1]:   {fruits[::-1]}")    # 反转
print(f"  len():         {len(fruits)}")     # 长度
print(f"  '苹果' in:     {'苹果' in fruits}") # 成员判断
print(f"  index('香蕉'): {fruits.index('香蕉')}") # 查找索引
print(f"  count('苹果'): {fruits.count('苹果')}") # 统计次数

# 遍历
subsection("遍历列表")
for i, fruit in enumerate(fruits):
    print(f"  [{i}] {fruit}")

# 1.3 修改 (Update)
subsection("修改元素")
nums = [10, 20, 30, 40, 50]
print(f"  原始:   {nums}")
nums[0] = 100
print(f"  改[0]:  {nums}")
nums[1:3] = [200, 300]
print(f"  改[1:3]:{nums}")

# 添加元素
subsection("添加元素")
lst = [1, 2]
print(f"  原始:   {lst}")
lst.append(3)
print(f"  append(3):     {lst}")            # 末尾添加
lst.insert(0, 0)
print(f"  insert(0,0):   {lst}")            # 指定位置插入
lst.extend([4, 5])
print(f"  extend([4,5]): {lst}")            # 批量添加
lst += [6]
print(f"  += [6]:        {lst}")            # 拼接

# 1.4 删除 (Delete)
subsection("删除元素")
lst = [1, 2, 3, 4, 5, 3]
print(f"  原始:     {lst}")
del lst[1]
print(f"  del [1]:  {lst}")                 # 按索引删除
lst.remove(3)
print(f"  remove(3):{lst}")                 # 按值删除第一个匹配
popped = lst.pop()
print(f"  pop():    {lst}  (弹出:{popped})") # 弹出末尾
popped2 = lst.pop(0)
print(f"  pop(0):   {lst}  (弹出:{popped2})")# 弹出指定位置
lst.clear()
print(f"  clear():  {lst}")                 # 清空

# 1.5 其他常用操作
subsection("排序/反转/复制")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"  原始:     {nums}")
sorted_nums = sorted(nums)
print(f"  sorted(): {sorted_nums}  (返回新列表)")
nums.sort()
print(f"  .sort():  {nums}  (原地排序)")
nums.sort(reverse=True)
print(f"  降序:     {nums}")
nums.reverse()
print(f"  reverse():{nums}")
print(f"  .copy():  {nums.copy()}")
import copy
deep = copy.deepcopy(nums)
print(f"  deepcopy:{deep}")


# ================================================================
# 二、元组 tuple (有序、不可变、允许重复)
# ================================================================
section("二、元组 tuple — 有序不可变序列")

# 2.1 创建
subsection("创建元组")
t = (1, 2, 3)
print(f"  字面量:     {t}")
t2 = tuple([1, 2, 3])
print(f"  tuple():    {t2}")
t3 = 1, 2, 3
print(f"  省略括号:   {t3}")
t4 = (42,)
print(f"  单元素:     {t4}  (必须加逗号!)")
t5 = ()
print(f"  空元组:     {t5}")

# 2.2 读取
subsection("读取元素 (与列表相同)")
t = ('a', 'b', 'c', 'd', 'e')
print(f"  t = {t}")
print(f"  t[0]:     {t[0]}")
print(f"  t[-1]:    {t[-1]}")
print(f"  t[1:4]:   {t[1:4]}")
print(f"  len(t):   {len(t)}")
print(f"  'b' in t: {'b' in t}")
print(f"  t.index('c'): {t.index('c')}")
print(f"  t.count('a'): {t.count('a')}")

# 遍历
for item in t:
    print(f"  {item}", end=" ")
print()

# 2.3 修改/删除 — 元组不可变，只能整体替换
subsection("修改/删除 (元组不可变，只能重建)")
t = (1, 2, 3)
print(f"  原始:     {t}")
t = t + (4,)
print(f"  拼接:     {t}  (创建新元组)")
t = (0,) + t[1:]
print(f"  改首个:   {t}")
t = tuple(x for x in t if x != 2)
print(f"  去掉2:    {t}")

# 元组解包
subsection("元组解包")
point = (3, 4)
x, y = point
print(f"  解包: x={x}, y={y}")
a, *b, c = (1, 2, 3, 4, 5)
print(f"  星号解包: a={a}, b={b}, c={c}")

# 作为函数返回值
def get_coords():
    return 10, 20, 30
result = get_coords()
print(f"  返回多值: {result}")


# ================================================================
# 三、字典 dict (无序→有序(python3.7+), 可变, 键唯一)
# ================================================================
section("三、字典 dict — 键值对映射")

# 3.1 创建
subsection("创建字典")
d = {'name': 'Alice', 'age': 25}
print(f"  字面量:   {d}")
d2 = dict(name='Bob', age=30)
print(f"  dict():   {d2}")
d3 = dict([('a', 1), ('b', 2)])
print(f"  列表转:   {d3}")
d4 = {k: v for k, v in [('x', 10), ('y', 20)]}
print(f"  推导式:   {d4}")
d5 = {}
print(f"  空字典:   {d5}")

# 3.2 读取
subsection("读取元素")
student = {'name': 'Alice', 'age': 25, 'scores': [90, 85, 92]}
print(f"  student = {student}")
print(f"  d['name']:       {student['name']}")   # 直接键访问
print(f"  d.get('age'):    {student.get('age')}") # get 方法
print(f"  d.get('phone'):  {student.get('phone')}") # 不存在返回 None
print(f"  d.get('phone','无'): {student.get('phone', '无')}") # 默认值
print(f"  'name' in d:     {'name' in student}")  # 检查键
print(f"  'Alice' in d:    {'Alice' in student}") # 只检查键不检查值

# 遍历
subsection("遍历字典")
print(f"  遍历键:   ", end="")
for key in student:
    print(key, end=" ")
print()
print(f"  .keys():  {list(student.keys())}")
print(f"  .values():{list(student.values())}")
print(f"  .items(): ", end="")
for k, v in student.items():
    print(f"{k}={v}", end="  ")
print()

# 3.3 修改
subsection("修改元素")
d = {'a': 1, 'b': 2, 'c': 3}
print(f"  原始:         {d}")
d['a'] = 100
print(f"  改值:         {d}")
d['d'] = 4
print(f"  加新键:       {d}")
d.update({'e': 5, 'f': 6})
print(f"  update():     {d}")
d.update(g=7)
print(f"  update(k=v):  {d}")
d.setdefault('h', 8)
print(f"  setdefault(): {d}  (键不存在才添加)")
d.setdefault('a', 999)
print(f"  setdefault存在: {d}  (已存在不修改)")

# 3.4 删除
subsection("删除元素")
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print(f"  原始:       {d}")
del d['a']
print(f"  del['a']:   {d}")
val = d.pop('b')
print(f"  pop('b'):   {d}  (弹出值:{val})")
val2 = d.pop('z', '默认')
print(f"  pop不存在:  {d}  (默认:{val2})")
d.setdefault('c', None)
print(f"  setdefault: {d}")
d.clear()
print(f"  clear():    {d}")

# 3.5 字典合并 (Python 3.5+)
subsection("字典合并")
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
merged = {**d1, **d2}
print(f"  {{**d1, **d2}}: {merged}")
merged2 = d1 | d2  # Python 3.9+
print(f"  d1 | d2:        {merged2}")
d1_copy = d1.copy()
d1_copy |= d2
print(f"  d1 |= d2:       {d1_copy}")

# 3.6 有序字典 (Python 3.7+ dict 已保证有序)
subsection("有序字典 (Python 3.7+)")
d = {'z': 3, 'a': 1, 'm': 2}
print(f"  插入顺序: {list(d.keys())}")  # 保持插入顺序
# 按 key 排序
sorted_by_key = dict(sorted(d.items()))
print(f"  按key排序: {list(sorted_by_key.keys())}")
# 按 value 排序
sorted_by_val = dict(sorted(d.items(), key=lambda x: x[1]))
print(f"  按val排序: {list(sorted_by_val.keys())}")


# ================================================================
# 四、集合 set (无序、可变、不重复)
# ================================================================
section("四、集合 set — 无序不重复集合")

# 4.1 创建
subsection("创建集合")
s = {1, 2, 3}
print(f"  字面量:   {s}")
s2 = set([1, 2, 2, 3])
print(f"  set():    {s2}  (自动去重)")
s3 = set('hello')
print(f"  字符串转: {s3}")
s4 = set()
print(f"  空集合:   {s4}  (注意: {{}} 是空字典!)")

# 4.2 读取
subsection("读取 (集合无序，无索引)")
s = {1, 2, 3, 4, 5}
print(f"  s = {s}")
print(f"  遍历:     ", end="")
for item in s:
    print(item, end=" ")
print()
print(f"  len(s):   {len(s)}")
print(f"  3 in s:   {3 in s}")
print(f"  9 in s:   {9 in s}")

# 集合运算
subsection("集合运算")
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"  A = {a}, B = {b}")
print(f"  A | B  并集: {a | b}")
print(f"  A & B  交集: {a & b}")
print(f"  A - B  差集: {a - b}  (A中不在B的)")
print(f"  A ^ B 对称差: {a ^ b}  (只在A或只在B的)")
print(f"  A <= B 子集: {a <= {1,2,3,4,5}}")
print(f"  A >= B 超集: {a >= {3,4}}")
print(f"  A.isdisjoint({{7,8}}): {a.isdisjoint({7, 8})}")

# 4.3 修改
subsection("添加元素")
s = {1, 2}
print(f"  原始:     {s}")
s.add(3)
print(f"  add(3):   {s}")
s.update([4, 5])
print(f"  update(): {s}")
s |= {6}
print(f"  |= {{6}}: {s}")

# 4.4 删除
subsection("删除元素")
s = {1, 2, 3, 4, 5}
print(f"  原始:       {s}")
s.remove(3)
print(f"  remove(3):  {s}  (不存在会报错)")
s.discard(99)
print(f"  discard(99):{s}  (不存在不报错)")
popped = s.pop()
print(f"  pop():      {s}  (弹出:{popped})")
s.clear()
print(f"  clear():    {s}")

# 4.5 集合的实际应用
subsection("实际应用: 去重")
lst = [1, 2, 2, 3, 3, 3, 1]
unique = list(set(lst))
print(f"  去重: {lst} -> {unique}  (注意: 顺序可能变)")
unique_ordered = list(dict.fromkeys(lst))
print(f"  保序去重:   {unique_ordered}")


# ================================================================
# 五、不可变集合 frozenset (无序、不可变、不重复)
# ================================================================
section("五、frozenset — 不可变集合")

# 5.1 创建
subsection("创建 frozenset")
fs = frozenset([1, 2, 3])
print(f"  frozenset([1,2,3]): {fs}")
fs2 = frozenset({1, 2, 2, 3})
print(f"  frozenset({{1,2,2,3}}): {fs2}")
fs3 = frozenset('abc')
print(f"  frozenset('abc'):    {fs3}")

# 5.2 读取 (与 set 相同，但不能修改)
subsection("读取")
fs = frozenset([1, 2, 3, 4])
print(f"  len:       {len(fs)}")
print(f"  3 in fs:   {3 in fs}")
print(f"  遍历:      ", end="")
for item in fs:
    print(item, end=" ")
print()

# 集合运算依然可用
a = frozenset([1, 2, 3])
b = frozenset([3, 4, 5])
print(f"  并集: {a | b}")
print(f"  交集: {a & b}")

# 5.3 不能修改
subsection("不可修改 (会报错)")
print(f"  ❌ fs.add(5)   -> AttributeError!")
print(f"  ❌ fs.remove(1) -> AttributeError!")

# 5.4 作为字典的键或集合的元素
subsection("特殊用途: 可哈希，能当键")
d = {frozenset({1, 2}): 'A', frozenset({3}): 'B'}
print(f"  作为 dict 键: {d}")
s = {frozenset({1, 2}), frozenset({3})}
print(f"  作为 set 元素: {s}")


# ================================================================
# 六、字符串 str (有序、不可变、Unicode)
# ================================================================
section("六、字符串 str — 有序不可变序列")

# 6.1 创建
subsection("创建字符串")
s1 = 'Hello'
s2 = "World"
s3 = """多行
字符串"""
s4 = f"f-string: {42}"
s5 = r'原始字符串: C:\Users\Admin'
print(f"  单引号:   {s1}")
print(f"  双引号:   {s2}")
print(f"  三引号:   {s3}")
print(f"  f-string: {s4}")
print(f"  raw:      {s5}")

# 6.2 读取
subsection("读取/索引/切片")
s = "Python"
print(f"  s = '{s}'")
print(f"  s[0]:     {s[0]}")
print(f"  s[-1]:    {s[-1]}")
print(f"  s[1:4]:   {s[1:4]}")
print(f"  s[::-1]:  {s[::-1]}")
print(f"  len(s):   {len(s)}")

# 常用方法
subsection("常用方法")
s = "Hello, World!"
print(f"  upper():       {s.upper()}")
print(f"  lower():       {s.lower()}")
print(f"  title():       {s.title()}")
print(f"  capitalize():  {s.capitalize()}")
print(f"  split():       {s.split()}")
print(f"  split(','):    {s.split(',')}")
print(f"  join(['a','b']): {'-'.join(['a', 'b'])}")
print(f"  replace('World','Python'): {s.replace('World', 'Python')}")
print(f"  'World' in s:  {'World' in s}")
print(f"  startswith('He'): {s.startswith('He')}")
print(f"  endswith('!'): {s.endswith('!')}")
print(f"  find('World'): {s.find('World')}")
print(f"  count('l'):    {s.count('l')}")
print(f"  strip():       '{s.strip()}'")
print(f"  center(20):    '{s.center(20)}'")
print(f"  isdigit():     {'123'.isdigit()}")
print(f"  isalpha():     {'abc'.isalpha()}")
print(f"  isalnum():     {'abc123'.isalnum()}")

# 6.3 修改 (不可变，只能创建新字符串)
subsection("修改 (不可变，返回新字符串)")
s = "Hello"
print(f"  原始:         '{s}'")
s2 = s + " World"
print(f"  + 拼接:       '{s2}'")
s3 = s.replace('l', 'L')
print(f"  replace():    '{s3}'")
s4 = s.upper()
print(f"  upper():      '{s4}'")
# 索引修改需要整体重建
s5 = s[:1] + 'a' + s[2:]
print(f"  改第2字符:    '{s5}'")

# f-string 格式化
subsection("f-string 格式化")
name, age = "Alice", 25
print(f"  基本:         {name} 今年 {age} 岁")
print(f"  表达式:       明年 {age + 1} 岁")
print(f"  格式化:       {3.14159:.2f}")
print(f"  对齐:         {'left':<10}|{'right':>10}|{'center':^10}|")


# ================================================================
# 七、字节 bytes (不可变二进制序列)
# ================================================================
section("七、bytes — 不可变二进制序列")

# 7.1 创建
subsection("创建 bytes")
b1 = b'hello'
print(f"  b'hello':       {b1}")
b2 = bytes('你好', 'utf-8')
print(f"  bytes(str,'utf-8'): {b2}")
b3 = bytes([72, 101, 108, 108, 111])
print(f"  bytes([ints]):  {b3}")
b4 = bytes(5)
print(f"  bytes(5):       {b4}  (5个零字节)")

# 7.2 读取
subsection("读取 bytes")
b = b'hello'
print(f"  b = {b}")
print(f"  b[0]:        {b[0]}  (返回整数)")
print(f"  b[1:4]:      {b[1:4]}")
print(f"  len(b):      {len(b)}")
print(f"  遍历:        ", end="")
for byte in b:
    print(byte, end=" ")
print()

# bytes <-> str 转换
subsection("bytes <-> str 转换")
s = "你好世界"
b = s.encode('utf-8')
print(f"  str -> bytes:   '{s}'.encode() -> {b}")
s2 = b.decode('utf-8')
print(f"  bytes -> str:   {b}.decode() -> '{s2}'")

# 7.3 常用方法
subsection("常用方法 (类似字符串)")
b = b'Hello World'
print(f"  upper():      {b.upper()}")
print(f"  lower():      {b.lower()}")
print(f"  split(b' '):  {b.split(b' ')}")
print(f"  replace():    {b.replace(b'World', b'Python')}")
print(f"  find(b'W'):   {b.find(b'W')}")


# ================================================================
# 八、bytearray (可变二进制序列)
# ================================================================
section("八、bytearray — 可变二进制序列")

# 8.1 创建
subsection("创建 bytearray")
ba1 = bytearray(b'hello')
print(f"  bytearray(b'hello'): {ba1}")
ba2 = bytearray('hello', 'utf-8')
print(f"  bytearray(str):      {ba2}")
ba3 = bytearray([72, 101])
print(f"  bytearray([ints]):   {ba3}")
ba4 = bytearray(5)
print(f"  bytearray(5):        {ba4}")

# 8.2 读取 (与 bytes 相同)
subsection("读取")
ba = bytearray(b'hello')
print(f"  ba = {ba}")
print(f"  ba[0]:    {ba[0]}")
print(f"  ba[1:4]:  {ba[1:4]}")
print(f"  len(ba):  {len(ba)}")

# 8.3 修改 (这是它与 bytes 的核心区别!)
subsection("修改 (可变!)")
ba = bytearray(b'hello')
print(f"  原始:              {ba}")
ba[0] = 74  # 'J'
print(f"  改字节[0]:         {ba}")
ba[1:3] = b'EL'
print(f"  改切片[1:3]:       {ba}")
ba.append(33)  # '!'
print(f"  append(33):        {ba}")
ba.extend(b' PY')
print(f"  extend(b' PY'):    {ba}")
ba.insert(5, 32)  # 空格
print(f"  insert(5, 32):     {ba}")
ba.pop(5)
print(f"  pop(5):            {ba}")
ba.remove(33)
print(f"  remove(33):        {ba}")
ba.reverse()
print(f"  reverse():         {ba}")

# 8.4 与 bytes 互转
subsection("与 bytes 互转")
ba = bytearray(b'test')
b = bytes(ba)
print(f"  bytearray -> bytes: {b}")
ba2 = bytearray(b)
print(f"  bytes -> bytearray: {ba2}")


# ================================================================
# 九、数据结构选择指南
# ================================================================
section("九、数据结构选择指南")
print("""
┌──────────────┬────────────┬──────────┬───────────────────────────────┐
│  需求         │  推荐结构   │  是否可变 │  特点                         │
├──────────────┼────────────┼──────────┼───────────────────────────────┤
│ 有序可变集合  │  list      │  ✅      │  通过索引快速访问 O(1)         │
│ 有序不可变    │  tuple     │  ❌      │  可哈希，可当字典键            │
│ 键值对映射    │  dict      │  ✅      │  按键查找 O(1)                 │
│ 无序去重集合  │  set       │  ✅      │  成员判断 O(1)，支持集合运算   │
│ 不可变集合    │  frozenset │  ❌      │  可哈希，可当字典键            │
│ 文本数据     │  str       │  ❌      │  Unicode，丰富的字符串方法     │
│ 二进制数据    │  bytes     │  ❌      │  网络传输、文件读取            │
│ 可变二进制    │  bytearray │  ✅      │  需要修改的二进制数据          │
│ 固定长度序列  │  tuple     │  ❌      │  保证不被修改                  │
│ 频繁查找      │  dict/set  │  ✅      │  O(1) 查找速度                │
│ 频繁插入删除  │  list      │  ✅      │  支持多种增删方法              │
└──────────────┴────────────┴──────────┴───────────────────────────────┘
""")

print("=" * 70)
print("演示完成！所有 Python 数据结构的增删改查已覆盖。")
print("=" * 70)
