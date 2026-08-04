# -*- coding: utf-8 -*-
"""
三、魔法方法 (Magic Methods / Dunder Methods)
以双下划线开头和结尾的特殊方法，让自定义类支持 Python 内置操作
"""


def demo():
    print("\n" + "=" * 70)
    print("三、魔法方法 (Magic Methods / Dunder)")
    print("=" * 70)

    # ========== 1. 构造与销毁 ==========
    print("\n--- 1. 构造与销毁 ---")

    class Lifecycle:
        def __init__(self, name):
            self.name = name
            print(f"  [{self.name}] __init__ 创建")

        def __new__(cls, name):
            """__new__ 在 __init__ 之前调用，创建并返回实例"""
            print(f"  [{name}] __new__ 分配内存")
            return super().__new__(cls)

        def __del__(self):
            """析构函数：实例被销毁时调用 (不保证调用，不推荐依赖)"""
            print(f"  [{self.name}] __del__ 销毁")

    obj = Lifecycle("测试对象")
    del obj  # 触发 __del__

    # ========== 2. 字符串表示 ==========
    print("\n--- 2. 字符串表示: __repr__ vs __str__ ---")

    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            """开发时用：明确、无歧义"""
            return f"Vector({self.x}, {self.y})"

        def __str__(self):
            """用户友好：print() 和 str() 使用"""
            return f"向量 ({self.x}, {self.y})"

    v = Vector(3, 4)
    print(f"  repr(v) = {repr(v)}")
    print(f"  str(v)  = {str(v)}")
    print(f"  print(v) = ", end="")
    print(v)

    # ========== 3. 比较运算 ==========
    print("\n--- 3. 比较运算 ---")

    class Student:
        def __init__(self, name, score):
            self.name = name
            self.score = score

        def __eq__(self, other):
            """== 比较"""
            if not isinstance(other, Student):
                return NotImplemented
            return self.score == other.score

        def __lt__(self, other):
            """< 比较"""
            if not isinstance(other, Student):
                return NotImplemented
            return self.score < other.score

        def __le__(self, other):
            """<= 比较"""
            return self == other or self < other

        def __gt__(self, other):
            return not self <= other

        def __ge__(self, other):
            return not self < other

        def __hash__(self):
            """使对象可哈希 (用于 set/dict 键)"""
            return hash(self.score)

        def __repr__(self):
            return f"Student({self.name}, {self.score})"

    s1 = Student("Alice", 95)
    s2 = Student("Bob", 87)
    s3 = Student("Alice", 95)

    print(f"  s1 == s2: {s1 == s2}")
    print(f"  s1 == s3: {s1 == s3}")
    print(f"  s1 <  s2: {s1 < s2}")
    print(f"  s1 >  s2: {s1 > s2}")
    print(f"  sorted([s1,s2]): {sorted([s1, s2])}")

    # ========== 4. 算术运算 ==========
    print("\n--- 4. 算术运算 ---")

    class Complex:
        def __init__(self, real, imag):
            self.real = real
            self.imag = imag

        def __add__(self, other):
            """+ 运算"""
            if not isinstance(other, Complex):
                return NotImplemented
            return Complex(self.real + other.real, self.imag + other.imag)

        def __sub__(self, other):
            """- 运算"""
            return Complex(self.real - other.real, self.imag - other.imag)

        def __mul__(self, other):
            """* 运算"""
            if not isinstance(other, Complex):
                return NotImplemented
            real = self.real * other.real - self.imag * other.imag
            imag = self.real * other.imag + self.imag * other.real
            return Complex(real, imag)

        def __abs__(self):
            """abs() 绝对值"""
            return (self.real ** 2 + self.imag ** 2) ** 0.5

        def __repr__(self):
            sign = "+" if self.imag >= 0 else "-"
            return f"Complex({self.real} {sign} {abs(self.imag)}j)"

        def __str__(self):
            return self.__repr__()

    c1 = Complex(3, 4)
    c2 = Complex(1, -2)
    print(f"  c1 + c2 = {c1 + c2}")
    print(f"  c1 - c2 = {c1 - c2}")
    print(f"  c1 * c2 = {c1 * c2}")
    print(f"  abs(c1) = {abs(c1):.2f}")

    # ========== 5. 容器协议 (索引、切片、长度) ==========
    print("\n--- 5. 容器协议 ---")

    class Stack:
        def __init__(self, *items):
            self._items = list(items)

        def __len__(self):
            """len() 长度"""
            return len(self._items)

        def __getitem__(self, index):
            """索引/切片读取"""
            if isinstance(index, slice):
                return Stack(*self._items[index])
            return self._items[index]

        def __setitem__(self, index, value):
            """索引赋值"""
            self._items[index] = value

        def __delitem__(self, index):
            """删除索引"""
            del self._items[index]

        def __contains__(self, item):
            """in 成员判断"""
            return item in self._items

        def __iter__(self):
            """迭代"""
            return iter(self._items)

        def __next__(self):
            """作为迭代器时使用"""
            pass  # 配合 __iter__ 使用

        def __repr__(self):
            return f"Stack({self._items})"

    stack = Stack(10, 20, 30, 40, 50)
    print(f"  len(stack) = {len(stack)}")
    print(f"  stack[0]   = {stack[0]}")
    print(f"  stack[1:4] = {stack[1:4]}")
    stack[0] = 100
    print(f"  stack[0]=100后: {stack}")
    print(f"  30 in stack: {30 in stack}")
    print(f"  遍历: ", end="")
    for item in stack:
        print(item, end=" ")
    print()

    # ========== 6. 调用协议 ==========
    print("\n--- 6. 调用协议: __call__ ---")

    class Multiplier:
        def __init__(self, factor):
            self.factor = factor

        def __call__(self, x):
            """使实例可以像函数一样调用"""
            return x * self.factor

    double = Multiplier(2)
    triple = Multiplier(3)
    print(f"  double(5)  = {double(5)}")
    print(f"  triple(7)  = {triple(7)}")

    # 作为工厂
    def make_validator(min_val, max_val):
        def validator(value):
            return min_val <= value <= max_val
        return validator

    age_check = make_validator(0, 150)
    print(f"  age_check(25)  = {age_check(25)}")
    print(f"  age_check(-1)  = {age_check(-1)}")

    # ========== 7. 上下文管理器 ==========
    print("\n--- 7. 上下文管理器: __enter__ / __exit__ ---")

    class DatabaseConnection:
        def __init__(self, url):
            self.url = url
            self.connected = False

        def __enter__(self):
            """进入 with 块时调用"""
            self.connected = True
            print(f"    连接到数据库: {self.url}")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """退出 with 块时调用 (即使有异常)"""
            self.connected = False
            if exc_type:
                print(f"    发生错误: {exc_val}")
            print(f"    关闭连接")
            return False  # False: 不抑制异常; True: 抑制异常

        def query(self, sql):
            if not self.connected:
                raise RuntimeError("未连接数据库")
            print(f"    执行查询: {sql}")

    print("  正常使用:")
    with DatabaseConnection("localhost:5432") as db:
        db.query("SELECT * FROM users")

    print("\n  发生异常时:")
    try:
        with DatabaseConnection("localhost:5432") as db:
            db.query("SELECT * FROM users")
            raise ValueError("模拟错误")
    except ValueError:
        pass  # 预期的异常，演示用

    # ========== 8. 属性访问 ==========
    print("\n--- 8. 属性访问: __getattr__ / __setattr__ ---")

    class DynamicAttr:
        def __init__(self):
            self._data = {}

        def __getattr__(self, name):
            """访问不存在的属性时调用"""
            if name.startswith('_'):
                raise AttributeError(name)
            return self._data.get(name, f"<{name} 未定义>")

        def __setattr__(self, name, value):
            """设置属性时调用"""
            if name.startswith('_') or name in ('_data',):
                super().__setattr__(name, value)
            else:
                self._data[name] = value

        def __delattr__(self, name):
            """删除属性时调用"""
            if name in self._data:
                del self._data[name]

    obj = DynamicAttr()
    obj.name = "动态属性"
    obj.age = 25
    print(f"  obj.name = {obj.name}")
    print(f"  obj.age  = {obj.age}")
    print(f"  obj.email = {obj.email}")  # 不存在时调用 __getattr__

    # ========== 9. 所有魔法方法速查表 ==========
    print("\n--- 9. 魔法方法速查表 ---")
    table = """
  ┌──────────────────────┬──────────────────────────────┐
  │  魔法方法             │  触发时机                     │
  ├──────────────────────┼──────────────────────────────┤
  │  __init__(self)      │  实例创建后初始化             │
  │  __new__(cls)        │  实例创建时分配内存           │
  │  __del__(self)       │  实例被垃圾回收               │
  │  __repr__(self)      │  repr()、交互式显示           │
  │  __str__(self)       │  str()、print()               │
  │  __eq__(self,other)  │  == 比较                     │
  │  __lt__(self,other)  │  < 比较                      │
  │  __hash__(self)      │  hash()、set/dict 键          │
  │  __add__(self,other) │  + 运算                      │
  │  __sub__(self,other) │  - 运算                      │
  │  __mul__(self,other) │  * 运算                      │
  │  __len__(self)       │  len()                       │
  │  __getitem__(self,i) │  索引/切片读取                │
  │  __setitem__(self,i) │  索引/切片赋值                │
  │  __delitem__(self,i) │  索引/切片删除                │
  │  __contains__(self,v)│  in 判断                     │
  │  __iter__(self)      │  迭代开始                     │
  │  __next__(self)      │  迭代下一步                   │
  │  __call__(self,...)  │  实例作为函数调用             │
  │  __enter__(self)     │  with 语句进入                │
  │  __exit__(self,...)  │  with 语句退出                │
  │  __getattr__(self,n) │  访问不存在的属性             │
  │  __setattr__(self,n) │  设置属性                     │
  │  __delattr__(self,n) │  删除属性                     │
  │  __bool__(self)      │  bool() 判断                  │
  │  __int__(self)       │  int() 转换                   │
  │  __float__(self)     │  float() 转换                 │
  │  __complex__(self)   │  complex() 转换               │
  │  __bytes__(self)     │  bytes() 转换                 │
  └──────────────────────┴──────────────────────────────┘
"""
    print(table)


if __name__ == "__main__":
    demo()
