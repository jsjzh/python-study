# -*- coding: utf-8 -*-
"""
Python 数据类型与类型转换演示
"""

# ==================== 一、各种数据类型变量声明 ====================

# 1. 整数类型 (int)
int_positive = 10
int_negative = -5
int_zero = 0
int_binary = 0b1010  # 二进制
int_octal = 0o755    # 八进制
int_hex = 0xFF       # 十六进制

# 2. 浮点数类型 (float)
float_positive = 3.14
float_negative = -0.5
float_scientific = 1.5e3  # 科学计数法，即 1500.0
float_infinity = float('inf')
float_nan = float('nan')

# 3. 复数类型 (complex)
complex_num = 3 + 4j
complex_negative = -1 - 2j

# 4. 布尔类型 (bool)
bool_true = True
bool_false = False
bool_from_int = bool(1)   # bool 是 int 的子类

# 5. 字符串类型 (str)
str_single = 'Hello'
str_double = "World"
str_triple = """多行
字符串"""
str_raw = r'C:\Users\Admin'  # 原始字符串
str_fstring = f"数值: {42}"  # f-string 格式化

# 6. 列表类型 (list) — 有序可变序列
list_int = [1, 2, 3, 4, 5]
list_mixed = [1, 'two', 3.0, True]
list_nested = [[1, 2], [3, 4]]
list_empty = []

# 7. 元组类型 (tuple) — 有序不可变序列
tuple_int = (1, 2, 3)
tuple_mixed = (1, 'hello', 3.14)
tuple_single = (42,)  # 单元素元组必须加逗号
tuple_unpack = 1, 2, 3  # 省略括号也可

# 8. 字典类型 (dict) — 键值对映射
dict_basic = {'name': 'Alice', 'age': 25}
dict_int_keys = {1: 'one', 2: 'two'}
dict_empty = {}

# 9. 集合类型 (set) — 无序不重复
set_int = {1, 2, 3, 4, 5}
set_str = {'apple', 'banana', 'cherry'}
set_from_list = set([1, 2, 2, 3])  # 自动去重

# 10. 不可变集合 (frozenset)
frozenset_int = frozenset([1, 2, 3])
frozenset_str = frozenset({'a', 'b', 'c'})

# 11. 空值类型 (NoneType)
none_value = None

# 12. 字节类型 (bytes) — 不可变二进制序列
bytes_ascii = b'hello'
bytes_utf8 = '你好'.encode('utf-8')
bytes_empty = b''

# 13. 字节数组 (bytearray) — 可变二进制序列
bytearray_ascii = bytearray(b'hello')
bytearray_empty = bytearray()

# 14. 范围类型 (range)
range_ten = range(10)       # 0~9
range_step = range(0, 20, 2)  # 0, 2, 4, ..., 18
range_neg = range(5, 0, -1)   # 5, 4, 3, 2, 1

# 15. 内存视图 (memoryview) — 访问二进制对象内存
memory_view = memoryview(b'abcdef')

# 16. 类型注解变量 (Type Hints)
from typing import Any, Optional, Union

annotated_int: int = 100
annotated_str: str = "类型注解"
annotated_list: list[int] = [1, 2, 3]
annotated_dict: dict[str, int] = {'a': 1}
annotated_optional: Optional[str] = None
annotated_union: Union[int, str] = "可以是 int 或 str"
annotated_any: Any = 3.14


# ==================== 二、打印每个变量的类型 ====================

def print_type(name: str, value) -> None:
    """打印变量的值、类型和 ID"""
    print(f"{name:25s} = {str(value):40s} -> 类型: {type(value).__name__:15s} id: {id(value)}")


print("=" * 90)
print("一、各种数据类型变量及其类型")
print("=" * 90)

variables = [
    # 整数
    ("int_positive", int_positive),
    ("int_negative", int_negative),
    ("int_zero", int_zero),
    ("int_binary", int_binary),
    ("int_octal", int_octal),
    ("int_hex", int_hex),
    # 浮点数
    ("float_positive", float_positive),
    ("float_negative", float_negative),
    ("float_scientific", float_scientific),
    ("float_infinity", float_infinity),
    ("float_nan", float_nan),
    # 复数
    ("complex_num", complex_num),
    ("complex_negative", complex_negative),
    # 布尔
    ("bool_true", bool_true),
    ("bool_false", bool_false),
    ("bool_from_int", bool_from_int),
    # 字符串
    ("str_single", str_single),
    ("str_double", str_double),
    ("str_triple", str_triple),
    ("str_raw", str_raw),
    ("str_fstring", str_fstring),
    # 列表
    ("list_int", list_int),
    ("list_mixed", list_mixed),
    ("list_nested", list_nested),
    ("list_empty", list_empty),
    # 元组
    ("tuple_int", tuple_int),
    ("tuple_mixed", tuple_mixed),
    ("tuple_single", tuple_single),
    ("tuple_unpack", tuple_unpack),
    # 字典
    ("dict_basic", dict_basic),
    ("dict_int_keys", dict_int_keys),
    ("dict_empty", dict_empty),
    # 集合
    ("set_int", set_int),
    ("set_str", set_str),
    ("set_from_list", set_from_list),
    # 不可变集合
    ("frozenset_int", frozenset_int),
    ("frozenset_str", frozenset_str),
    # 空值
    ("none_value", none_value),
    # 字节
    ("bytes_ascii", bytes_ascii),
    ("bytes_utf8", bytes_utf8),
    ("bytes_empty", bytes_empty),
    # 字节数组
    ("bytearray_ascii", bytearray_ascii),
    ("bytearray_empty", bytearray_empty),
    # 范围
    ("range_ten", range_ten),
    ("range_step", range_step),
    ("range_neg", range_neg),
    # 内存视图
    ("memory_view", memory_view),
    # 类型注解
    ("annotated_int", annotated_int),
    ("annotated_str", annotated_str),
    ("annotated_list", annotated_list),
    ("annotated_dict", annotated_dict),
    ("annotated_optional", annotated_optional),
    ("annotated_union", annotated_union),
    ("annotated_any", annotated_any),
]

for name, value in variables:
    print_type(name, value)


# ==================== 三、类型转换案例 ====================

print()
print("=" * 90)
print("二、类型转换案例")
print("=" * 90)

# ---------- 1. 其他类型 -> 整数 int ----------
print("\n--- 1. 转换为 int ---")
print(f"float(3.9)   -> int: {int(3.9)}")          # 截断小数部分
print(f"float(-2.7)  -> int: {int(-2.7)}")         # 向零截断
print(f"str('123')   -> int: {int('123')}")
print(f"str('0xFF')  -> int: {int('0xFF', 16)}")   # 指定进制
print(f"str('1010',2)-> int: {int('1010', 2)}")    # 二进制字符串
print(f"bool(True)   -> int: {int(True)}")          # True -> 1
print(f"bool(False)  -> int: {int(False)}")         # False -> 0
print(f"bytes(b'42') -> int: {int(b'42')}")

# ---------- 2. 其他类型 -> 浮点数 float ----------
print("\n--- 2. 转换为 float ---")
print(f"int(42)      -> float: {float(42)}")
print(f"str('3.14')  -> float: {float('3.14')}")
print(f"str('1e3')   -> float: {float('1e3')}")     # 科学计数法
print(f"bool(True)   -> float: {float(True)}")
print(f"int('inf')   -> float: {float('inf')}")

# ---------- 3. 其他类型 -> 复数 complex ----------
print("\n--- 3. 转换为 complex ---")
print(f"int(5)       -> complex: {complex(5)}")        # 5+0j
print(f"float(3.5)   -> complex: {complex(3.5)}")      # 3.5+0j
print(f"str('2+3j')  -> complex: {complex('2+3j')}")
print(f"complex(1,2) -> complex: {complex(1, 2)}")     # 1+2j

# ---------- 4. 其他类型 -> 字符串 str ----------
print("\n--- 4. 转换为 str ---")
print(f"int(42)           -> str: {str(42)}")
print(f"float(3.14)       -> str: {str(3.14)}")
print(f"bool(True)        -> str: {str(True)}")
print(f"list([1,2,3])     -> str: {str([1, 2, 3])}")
print(f"tuple((1,2))      -> str: {str((1, 2))}")
print(f"dict({{'a':1}})   -> str: {str({'a': 1})}")
print(f"bytes(b'hello')   -> str: {str(b'hello')}")          # 默认 utf-8
chinese_bytes = '你好'.encode('utf-8')
print(f"bytes.decode()    -> str: {chinese_bytes.decode('utf-8')}")  # 显式解码

# ---------- 5. 其他类型 -> 列表 list ----------
print("\n--- 5. 转换为 list ---")
print(f"tuple((1,2,3))       -> list: {list((1, 2, 3))}")
print(f"str('abc')           -> list: {list('abc')}")       # 拆分为字符
print(f"set({{1,2,3}})       -> list: {list({1, 2, 3})}")
print(f"range(5)             -> list: {list(range(5))}")
print(f"bytes(b'hello')      -> list: {list(b'hello')}")   # 得到字节值列表

# ---------- 6. 其他类型 -> 元组 tuple ----------
print("\n--- 6. 转换为 tuple ---")
print(f"list([1,2,3])   -> tuple: {tuple([1, 2, 3])}")
print(f"str('abc')      -> tuple: {tuple('abc')}")
print(f"set({{1,2,3}})  -> tuple: {tuple({1, 2, 3})}")
print(f"range(5)        -> tuple: {tuple(range(5))}")

# ---------- 7. 其他类型 -> 集合 set ----------
print("\n--- 7. 转换为 set ---")
print(f"list([1,2,2,3])   -> set: {set([1, 2, 2, 3])}")   # 自动去重
print(f"tuple((1,1,2,3))  -> set: {set((1, 1, 2, 3))}")
print(f"str('hello')      -> set: {set('hello')}")        # 字符去重

# ---------- 8. 其他类型 -> 不可变集合 frozenset ----------
print("\n--- 8. 转换为 frozenset ---")
print(f"list([1,2,3])      -> frozenset: {frozenset([1, 2, 3])}")
print(f"set({{'a','b'}})   -> frozenset: {frozenset({'a', 'b'})}")

# ---------- 9. 其他类型 -> 字典 dict ----------
print("\n--- 9. 转换为 dict ---")
print(f"list of pairs -> dict: {dict([('a', 1), ('b', 2)])}")
print(f"tuple of pairs -> dict: {dict((('x', 10), ('y', 20)))}")
print(f"keys + values  -> dict: {dict(zip(['k1', 'k2'], [100, 200]))}")

# ---------- 10. 其他类型 -> 布尔 bool ----------
print("\n--- 10. 转换为 bool ---")
print(f"int(0)         -> bool: {bool(0)}")
print(f"int(1)         -> bool: {bool(1)}")
print(f"float(0.0)     -> bool: {bool(0.0)}")
print(f"float(3.14)    -> bool: {bool(3.14)}")
print(f"str('')        -> bool: {bool('')}")         # 空字符串 False
print(f"str('hello')   -> bool: {bool('hello')}")
print(f"list([])       -> bool: {bool([])}")         # 空列表 False
print(f"list([1])      -> bool: {bool([1])}")
print(f"dict({{}})      -> bool: {bool({})}")         # 空字典 False
print(f"set({{}})       -> bool: {bool(set())}")      # 空集合 False
print(f"None           -> bool: {bool(None)}")

# ---------- 11. 其他类型 -> 字节 bytes ----------
print("\n--- 11. 转换为 bytes ---")
print(f"str -> bytes (encode): {'你好'.encode('utf-8')}")
print(f"list of ints -> bytes: {bytes([72, 101, 108, 108, 111])}")
print(f"bytes -> bytes: {bytes(b'hello')}")

# ---------- 12. 其他类型 -> 字节数组 bytearray ----------
print("\n--- 12. 转换为 bytearray ---")
print(f"str -> bytearray: {bytearray('abc', 'utf-8')}")
print(f"bytes -> bytearray: {bytearray(b'hello')}")
print(f"list of ints -> bytearray: {bytearray([65, 66, 67])}")

# ---------- 13. 其他类型 -> range ----------
print("\n--- 13. 创建 range ---")
print(f"range(5)          -> list: {list(range(5))}")
print(f"range(1, 6)       -> list: {list(range(1, 6))}")
print(f"range(0, 10, 3)   -> list: {list(range(0, 10, 3))}")
print(f"range(5, 0, -1)   -> list: {list(range(5, 0, -1))}")


# ==================== 四、类型转换常见坑点 ====================

print()
print("=" * 90)
print("三、类型转换常见坑点")
print("=" * 90)

# 坑1: float -> int 截断而非四舍五入
print(f"\n【坑1】float 转 int 是截断，不是四舍五入:")
print(f"  int(3.9) = {int(3.9)}  (期望 4，但实际截断为 3)")
print(f"  正确的四舍五入应使用 round(): round(3.9) = {round(3.9)}")

# 坑2: 字符串转 int 必须是合法数字
print(f"\n【坑2】非法字符串无法转 int:")
try:
    int('hello')
except ValueError as e:
    print(f"  int('hello') 报错: {e}")

# 坑3: 布尔型是 int 的子类
print(f"\n【坑3】bool 是 int 子类，True == 1, False == 0:")
print(f"  True == 1: {True == 1}")
print(f"  False == 0: {False == 0}")
print(f"  True + True + True = {True + True + True}")

# 坑4: list 与 tuple 互转保留元素
print(f"\n【坑4】list <-> tuple 互转:")
original_list = [1, 2, 3]
converted_tuple = tuple(original_list)
converted_list_back = list(converted_tuple)
print(f"  list -> tuple -> list 保持不变: {converted_list_back}")

# 坑5: set 转换自动去重且打乱顺序
print(f"\n【坑5】set 转换会去重且顺序不确定:")
dup_list = [3, 1, 2, 1, 3, 2]
print(f"  原列表: {dup_list}")
print(f"  set 后: {set(dup_list)}  (去重，顺序可能变化)")
print(f"  再转 list: {list(set(dup_list))}")

# 坑6: bytes 与 str 的编码/解码
print(f"\n【坑6】bytes <-> str 需要指定编码:")
s = "你好世界"
b = s.encode('utf-8')
print(f"  str -> bytes: {b}")
print(f"  bytes -> str: {b.decode('utf-8')}")

print("\n" + "=" * 90)
print("演示完成！")
print("=" * 90)
