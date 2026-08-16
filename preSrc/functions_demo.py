"""
Python 函数全演示
涵盖: 函数定义/调用、各种参数写法、lambda匿名函数、闭包、局部/全局变量、递归等
"""

from collections.abc import Callable

print("=" * 70)
print("一、函数基础: 定义与调用")
print("=" * 70)


def greet():
    """最简单的函数: 无参数，无返回值"""
    print("  Hello, World!")


greet()


def say_hello(name: str) -> None:
    """带参数的函数"""
    print(f"  你好, {name}!")


say_hello("小明")


def add(a: int, b: int) -> int:
    """带参数和返回值的函数"""
    return a + b


result = add(3, 5)
print(f"  add(3, 5) = {result}")


def get_user_info() -> tuple:
    """返回多个值 (用 tuple)"""
    name = "Alice"
    age = 25
    city = "北京"
    return name, age, city


info = get_user_info()
print(f"  单变量接收: {info}")
name, age, city = get_user_info()
print(f"  解包接收: name={name}, age={age}, city={city}")


def is_even(n: int) -> bool:
    """返回布尔值"""
    return n % 2 == 0


print(f"  is_even(4) = {is_even(4)}")
print(f"  is_even(7) = {is_even(7)}")


print("\n" + "=" * 70)
print("二、函数参数的所有写法")
print("=" * 70)

# 1. 位置参数 (Positional Arguments)
print("1. 位置参数: 按顺序传递，顺序必须一致")


def divide(a: float, b: float) -> float:
    return a / b


print(f"  divide(10, 2) = {divide(10, 2)}")
print(f"  divide(2, 10)  = {divide(2, 10)}   (顺序变了结果就变)")

# 2. 关键字参数 (Keyword Arguments)
print("\n2. 关键字参数: 通过参数名传递，顺序无关")
print(f"  divide(a=10, b=2) = {divide(a=10, b=2)}")
print(f"  divide(b=2, a=10) = {divide(b=2, a=10)}   (顺序变了也不影响)")

# 3. 默认参数 (Default Arguments)
print("\n3. 默认参数: 调用时可以省略，使用默认值")


def power(base: int, exp: int = 2) -> int:
    return base**exp


print(f"  power(3)       = {power(3)}          (exp 默认 2, 计算 3**2)")
print(f"  power(3, 3)    = {power(3, 3)}       (3**3)")
print(f"  power(3, exp=4)= {power(3, exp=4)}   (3**4)")

# 注意: 默认参数不要用可变对象!
print("\n  ⚠️  默认参数陷阱: 可变对象作为默认值会被共享!")


def append_to_list(value, target=[]):
    target.append(value)
    return target


print(f"  第一次调用: {append_to_list(1)}")
print(f"  第二次调用: {append_to_list(2)}   (默认列表被污染了!)")


# 正确写法
def append_to_list_safe(value, target=None):
    if target is None:
        target = []
    target.append(value)
    return target


print(f"  安全写法:   {append_to_list_safe(1)}")
print(f"  安全写法:   {append_to_list_safe(2)}   (每次都是新列表)")

# 4. 位置参数只能在前，默认参数在后
print("\n4. 位置参数 + 默认参数混合: 必填在前，默认在后")


def create_user(username: str, age: int = 18, city: str = "北京") -> str:
    return f"用户: {username}, {age}岁, {city}"


print(f"  create_user('Alice')              -> {create_user('Alice')}")
print(f"  create_user('Bob', 25)            -> {create_user('Bob', 25)}")
print(f"  create_user('Carol', city='上海') -> {create_user('Carol', city='上海')}")

# 5. 可变位置参数 *args
print("\n5. *args: 接收任意数量的位置参数 (元组)")


def sum_all(*args: int) -> int:
    print(f"  接收到 {len(args)} 个参数: {args}")
    return sum(args)


print(f"  sum_all(1, 2, 3)       = {sum_all(1, 2, 3)}")
print(f"  sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
print(f"  sum_all()              = {sum_all()}")

# 6. 可变关键字参数 **kwargs
print("\n6. **kwargs: 接收任意数量的关键字参数 (字典)")


def show_config(**kwargs) -> None:
    print(f"  接收到 {len(kwargs)} 个配置:")
    for key, value in kwargs.items():
        print(f"    {key} = {value}")


show_config(host="localhost", port=8080, debug=True)
print()
show_config(database="MySQL", user="root")

# 7. *args 和 **kwargs 同时使用
print("\n7. *args + **kwargs 同时使用 (函数定义参数必须这样: 普通, *args, **kwargs)")


def demo_mixed(required, *args, **kwargs):
    print(f"  必填参数: {required}")
    print(f"  *args:   {args}")
    print(f"  **kwargs:{kwargs}")


demo_mixed("hello", 1, 2, 3, name="test", value=42)

# 8. 仅关键字参数 (Keyword-Only Arguments)
print("\n8. 仅关键字参数: 必须用关键字传递，放在 * 后面")


def configure(*, host="127.0.0.1", port=8080, debug=False):
    return f"服务器: {host}:{port}, 调试={debug}"


print(f"  configure()                           -> {configure()}")
print(f"  configure(port=3306)                  -> {configure(port=3306)}")
print("  configure('localhost')                -> 报错! 只能用关键字传递")

# 9. 位置参数仅限 (Positional-Only Arguments) — Python 3.8+
print("\n9. 位置参数仅限: 只能位置传递，不能用关键字 (用 / 分隔)")


def divide_pos_only(a, b, /):
    return a / b


print(f"  divide_pos_only(10, 2)     = {divide_pos_only(10, 2)}")
print("  divide_pos_only(a=10, b=2) -> 报错! 只能位置传递")

# 10. 参数解包
print("\n10. 参数解包: 把列表/字典拆开传给函数")
nums = [10, 20, 30]
print(f"  列表解包: sum_all(*nums) = {sum_all(*nums)}")

config = {"host": "0.0.0.0", "port": 9000}
print(f"  字典解包: {configure(**config)} -> {configure(**config)}")

# 11. 类型注解 (Type Hints)
print("\n11. 类型注解: 标注参数和返回值类型，便于 IDE 检查")


def typed_func(name: str, count: int = 1) -> str:
    return f"{name} x {count}"


print(f"  typed_func('ha', 3) = {typed_func('ha', 3)}")

# 12. 函数作为参数 (高阶函数)
print("\n12. 函数作为参数传递 (高阶函数)")


def apply_operation(x: int, y: int, op: Callable[[int, int], int]) -> int:
    return op(x, y)


def multiply(a: int, b: int) -> int:
    return a * b


print(f"  apply_operation(3, 4, multiply) = {apply_operation(3, 4, multiply)}")


print("\n" + "=" * 70)
print("三、匿名函数 lambda")
print("=" * 70)

# 基本语法: lambda 参数: 表达式
print("1. 基本语法: lambda 参数: 表达式 (只能包含一个表达式)")
square = lambda x: x**2
print("  square = lambda x: x**2")
print(f"  square(5) = {square(5)}")

# 多参数
add_lambda = lambda a, b: a + b
print(f"  add_lambda(3, 5) = {add_lambda(3, 5)}")

# 带默认参数
greet_lambda = lambda name="World": f"Hello, {name}!"
print(f"  greet_lambda()           = {greet_lambda()}")
print(f"  greet_lambda('Alice')    = {greet_lambda('Alice')}")

# 2. 常用于排序
print("\n2. lambda 常用于 sorted/max/min 等函数的 key 参数")
students = [("Alice", 95), ("Bob", 87), ("Charlie", 92)]
print(f"  学生列表: {students}")

# 按分数排序
sorted_by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(f"  按分数排序: {sorted_by_score}")

# 按名字排序
sorted_by_name = sorted(students, key=lambda s: s[0])
print(f"  按名字排序: {sorted_by_name}")

# 找出分数最高的学生
top_student = max(students, key=lambda s: s[1])
print(f"  分数最高: {top_student}")

# 3. 配合 map/filter/reduce
print("\n3. 配合 map/filter 使用")
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
print(f"  map: {nums} -> {doubled}")

evens = list(filter(lambda x: x % 2 == 0, nums))
print(f"  filter: {nums} -> {evens} (偶数)")

from functools import reduce

total = reduce(lambda a, b: a + b, nums)
print(f"  reduce: {nums} 求和 = {total}")

# 4. 闭包 + lambda
print("\n4. lambda 结合闭包使用")


def make_multiplier(n):
    return lambda x: x * n


double = make_multiplier(2)
triple = make_multiplier(3)
print(f"  double(5)  = {double(5)}")
print(f"  triple(5)  = {triple(5)}")

# 5. lambda 的局限
print("\n5. lambda 局限: 只能写一个表达式，复杂逻辑请用 def")
print("  ❌ 不能写多行语句")
print("  ❌ 不能有 if/for (但可以用三元表达式)")
print("  ❌ 可读性差，复杂逻辑请用 def")

# 错误示例 (演示局限)
# bad_lambda = lambda x: if x > 0: print(x)  # SyntaxError!
ok_lambda = lambda x: "正数" if x > 0 else "非正数"
print("  ✅ 可以用三元表达式: lambda x: '正数' if x > 0 else '非正数'")
print(f"     ok_lambda(5) = {ok_lambda(5)}")
print(f"     ok_lambda(-3) = {ok_lambda(-3)}")


print("\n" + "=" * 70)
print("四、闭包 (Closure)")
print("=" * 70)

# 什么是闭包: 函数 + 其引用的外部变量 = 闭包
print("1. 基本闭包: 内部函数引用了外部变量，外部函数返回内部函数")


def make_counter():
    count = 0  # 自由变量 (被内部函数引用)

    def increment():
        nonlocal count  # 声明使用外层变量
        count += 1
        return count

    return increment


counter = make_counter()
print(f"  counter() 第一次: {counter()}")  # 1
print(f"  counter() 第二次: {counter()}")  # 2
print(f"  counter() 第三次: {counter()}")  # 3

counter2 = make_counter()
print(f"  新计数器 counter2() 第一次: {counter2()}")  # 1 (独立的)

# 2. 闭包的应用: 工厂函数
print("\n2. 闭包应用: 生成特定功能的函数")


def make_validator(min_val, max_val):
    """生成一个验证函数，检查值是否在范围内"""

    def validate(value):
        return min_val <= value <= max_val

    return validate


age_validator = make_validator(0, 150)
print(f"  age_validator(25)  = {age_validator(25)}")  # True
print(f"  age_validator(-1)  = {age_validator(-1)}")  # False
print(f"  age_validator(200) = {age_validator(200)}")  # False

score_validator = make_validator(0, 100)
print(f"  score_validator(85) = {score_validator(85)}")  # True

# 3. 闭包实现装饰器的基础
print("\n3. 闭包实现计时器装饰器 (简化版)")
import time


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  函数 {func.__name__} 耗时 {elapsed:.6f} 秒")
        return result

    return wrapper


@timer_decorator
def slow_add(a, b):
    time.sleep(0.01)
    return a + b


print(f"  slow_add(3, 5) = {slow_add(3, 5)}")

# 4. 闭包 vs 类
print("\n4. 闭包 vs 类: 都能保存状态")


# 用闭包实现
def make_account_balance(initial=0):
    balance = initial

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount):
        nonlocal balance
        balance -= amount
        return balance

    def get_balance():
        return balance

    return {"deposit": deposit, "withdraw": withdraw, "balance": get_balance}


account = make_account_balance(100)
print(f"  闭包账户 初始余额: {account['balance']()}")
print(f"  存入50: {account['deposit'](50)}")
print(f"  取出30: {account['withdraw'](30)}")


print("\n" + "=" * 70)
print("五、局部变量 vs 全局变量")
print("=" * 70)

# 1. 作用域规则: Local -> Enclosing -> Global -> Built-in (LEGB)
print("Python 变量查找顺序 (LEGB 规则):")
print("  L (Local)     - 函数内部")
print("  E (Enclosing) - 嵌套函数的外层函数")
print("  G (Global)    - 模块级别")
print("  B (Built-in)  - Python 内置 (如 int, print)")

# 2. 局部变量
print("\n1. 局部变量: 函数内部定义，仅函数内有效")


def show_local():
    local_var = "我是局部变量"
    print(f"  函数内: local_var = {local_var}")
    print("  只能在函数内访问")


show_local()
# print(local_var)  # NameError! 外部不能访问

# 3. 全局变量
print("\n2. 全局变量: 模块级别定义，整个文件都可访问")

global_var = "我是全局变量"


def show_global():
    print(f"  函数内可以直接读取全局变量: {global_var}")


show_global()
print(f"  函数外也能访问: {global_var}")

# 4. 修改全局变量 (需要 global 关键字)
print("\n3. 修改全局变量: 需要 global 关键字声明")

count = 0


def increment_global():
    # count += 1  # 错误! 这会被当作局部变量，但它未被赋值
    global count  # 声明使用全局变量
    count += 1


print(f"  修改前: count = {count}")
increment_global()
print(f"  修改后: count = {count}")

# 5. 局部变量遮蔽全局变量
print("\n4. 局部变量遮蔽: 函数内同名局部变量会遮蔽全局变量")

name = "全局的Alice"


def show_name():
    name = "局部的Bob"  # 这个局部变量遮蔽了全局的 name
    print(f"  函数内 name = {name}")


show_name()
print(f"  函数外 name = {name}")

# 6. nonlocal 关键字
print("\n5. nonlocal: 修改嵌套函数中的外层函数变量")


def outer():
    message = "外层消息"

    def inner():
        nonlocal message
        message = "被内层修改了"
        print(f"  inner: {message}")

    inner()
    print(f"  outer: {message}")


outer()

# 7. globals() 和 locals() 函数
print("\n6. 查看作用域中的所有变量")
print("  globals() 包含: 'global_var', 'count', 'name' ...")
print("  locals() 在不同位置结果不同")

sample = "demo"
print(f"  当前模块 locals() keys: {list(locals().keys())[:10]}...")


def show_scopes():
    inner_var = "inner"
    print(f"  函数内 locals() keys: {list(locals().keys())}")


show_scopes()

# 8. global 和 nonlocal 对比
print("\n7. global vs nonlocal 对比:")
print("  global:   声明/修改 模块级变量")
print("  nonlocal: 声明/修改 外层嵌套函数的变量")
print("  都不使用: 只能读取，不能修改 (除非是可变对象的方法)")

# 可变对象的方法调用不需要 global
my_list = []


def add_to_list(item):
    my_list.append(item)  # 不需要 global! 只是调用方法，不是重新赋值


add_to_list(1)
add_to_list(2)
print(f"  调用方法不需要 global: my_list = {my_list}")

# 9. 变量作用域最佳实践
print("\n8. 最佳实践:")
print("  ✅ 尽量使用参数传递和返回值，避免全局变量")
print("  ✅ 需要共享状态时使用类或闭包")
print("  ✅ global/nonlocal 只在必要时使用")
print("  ✅ 函数内变量用有意义的名称，避免和全局变量同名")


print("\n" + "=" * 70)
print("六、递归函数")
print("=" * 70)


def factorial(n: int) -> int:
    """递归: 阶乘"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print(f"  factorial(5) = {factorial(5)}")  # 120


def fibonacci(n: int) -> int:
    """递归: 斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


fib_results = [fibonacci(i) for i in range(8)]
print(f"  斐波那契前8项: {fib_results}")


print("\n" + "=" * 70)
print("七、函数的其他实用技巧")
print("=" * 70)

# 1. 文档字符串
print("1. 文档字符串 (docstring): 函数的第一行字符串")


def calculate_bmi(weight: float, height: float) -> float:
    """计算 BMI 指数

    Args:
        weight: 体重 (kg)
        height: 身高 (m)

    Returns:
        BMI 值
    """
    return weight / (height**2)


print(f"  BMI(70kg, 1.75m) = {calculate_bmi(70, 1.75):.1f}")
print(f"  文档字符串: {calculate_bmi.__doc__[:20]}...")

# 2. 获取函数信息
print("\n2. 获取函数信息")
print(f"  函数名: {add.__name__}")
print(f"  函数默认值: {power.__defaults__}")
import inspect

print(f"  函数签名: {inspect.signature(configure)}")

# 3. 函数缓存 (lru_cache)
print("\n3. 函数缓存 @lru_cache (避免重复计算)")
from functools import lru_cache


@lru_cache(maxsize=128)
def fib_cached(n: int) -> int:
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


start = time.time()
result = fib_cached(30)
elapsed = time.time() - start
print(f"  斐波那契(30) 缓存后耗时: {elapsed:.6f}秒, 结果: {result}")


print("\n" + "=" * 70)
print("演示完成！Python 函数的所有核心概念已覆盖。")
print("=" * 70)
