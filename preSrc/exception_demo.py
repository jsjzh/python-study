"""
Python 异常处理机制全演示
涵盖: 常见异常、try/except/else/finally、raise、自定义异常、assert、异常链等
"""

import sys
import traceback


def section(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def subsection(title: str) -> None:
    print(f"\n  --- {title} ---")


# ================================================================
# 一、常见的内置异常类型
# ================================================================
section("一、常见内置异常类型速查")

exceptions = [
    ("Exception", "所有非系统退出异常的基类"),
    ("BaseException", "所有异常的基类 (包括 KeyboardInterrupt, SystemExit)"),
    ("SystemExit", "sys.exit() 触发的系统退出"),
    ("KeyboardInterrupt", "Ctrl+C 中断"),
    ("GeneratorExit", "生成器/协程关闭时触发"),
    ("ArithmeticError", "算术错误基类"),
    ("  ZeroDivisionError", "除零错误"),
    ("  OverflowError", "数值溢出"),
    ("  FloatingPointError", "浮点运算错误"),
    ("LookupError", "查找错误基类"),
    ("  IndexError", "索引超出范围"),
    ("  KeyError", "字典键不存在"),
    ("AttributeError", "对象没有某个属性"),
    ("TypeError", "类型不兼容的操作"),
    ("ValueError", "值的类型正确但内容非法"),
    ("NameError", "变量名未定义"),
    ("UnboundLocalError", "局部变量未绑定就使用"),
    ("OSError", "操作系统错误基类"),
    ("  FileNotFoundError", "文件不存在"),
    ("  PermissionError", "权限不足"),
    ("  ConnectionError", "网络连接错误基类"),
    ("RuntimeError", "运行时错误基类"),
    ("  RecursionError", "递归深度超过限制"),
    ("  NotImplementedError", "抽象方法未实现"),
    ("SyntaxError", "语法错误 (编码阶段捕获，无法 try/except)"),
    ("  IndentationError", "缩进错误"),
    ("UnicodeError", "Unicode 编码/解码错误"),
    ("StopIteration", "迭代器没有更多元素 (Python 3 中不再作为 StopIteration 泄漏)"),
    ("ImportError", "导入错误基类"),
    ("  ModuleNotFoundError", "模块找不到"),
]

for name, desc in exceptions:
    print(f"  {name:30s} - {desc}")


# ================================================================
# 二、try / except 基本用法
# ================================================================
section("二、try / except 基本用法")

# 2.1 捕获单个异常
subsection("捕获单个异常")


def divide(a, b):
    return a / b


try:
    result = divide(10, 0)
except ZeroDivisionError:
    print("  ❌ 捕获 ZeroDivisionError: 不能除以零!")

# 2.2 捕获多个异常 (多个 except 分支)
subsection("捕获多个异常")


def parse_number(text):
    return int(text)


test_cases = ["123", "abc", None]
for case in test_cases:
    try:
        val = parse_number(case)
        print(f"  输入 {case!r} -> 成功: {val}")
    except ValueError:
        print(f"  输入 {case!r} -> ValueError: 不是有效整数")
    except TypeError:
        print(f"  输入 {case!r} -> TypeError: 类型不对")

# 2.3 一个 except 捕获多个异常 (元组形式)
subsection("一个 except 捕获多个异常")

for val in ["abc", None]:
    try:
        result = int(val)
    except (ValueError, TypeError) as e:
        print(f"  输入 {val!r} -> 错误: {type(e).__name__}: {e}")

# 2.4 捕获所有异常 (不推荐生产环境使用)
subsection("捕获所有异常 (Exception)")

try:
    1 / 0
except Exception as e:
    print(f"  捕获 Exception: {type(e).__name__}: {e}")

# 2.5 获取异常实例
subsection("获取异常实例 (as 关键字)")

try:
    d = {"a": 1}
    val = d["b"]
except KeyError as e:
    print(f"  KeyError: {e}")  # 异常值
    print(f"  args: {e.args}")  # 异常参数元组
    print(f"  str(e): {e!s}")  # 字符串表示


# ================================================================
# 三、try / except / else / finally 完整结构
# ================================================================
section("三、try / except / else / finally")

subsection("else: 没有异常时执行")


def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  ⚠️  除零错误: {a} / {b}")
        return None
    else:
        print(f"  ✅ 计算成功: {a} / {b} = {result}")
        return result
    finally:
        print("  🔄 finally 块总是会执行")


safe_divide(10, 2)
safe_divide(10, 0)

subsection("finally: 无论如何都执行 (常用于资源清理)")


def read_file_safe(filename):
    f = None
    try:
        f = open(filename, encoding="utf-8")
        content = f.read()
        print(f"  读取成功: {content[:50]}...")
    except FileNotFoundError:
        print(f"  ❌ 文件不存在: {filename}")
    except OSError as e:
        print(f"  ❌ IO 错误: {e}")
    finally:
        if f:
            f.close()
            print("  🔄 文件已关闭")
        print("  🔄 finally 清理完成")


read_file_safe("temp_exist_demo.txt")
read_file_safe("temp_not_exist.txt")

# 演示 finally 在任何情况下都会执行
subsection("finally 在所有情况都会执行")


def test_finally(trigger_error):
    print("  进入函数")
    try:
        print("  try 块")
        if trigger_error:
            raise ValueError("模拟错误")
        print("  try 块成功")
    except ValueError:
        print("  except 块处理错误")
    else:
        print("  else 块 (无异常)")
    finally:
        print("  finally 块 (总是执行)")
    print("  函数结束")


print("  --- 触发异常 ---")
test_finally(True)
print("\n  --- 不触发异常 ---")
test_finally(False)


# ================================================================
# 四、raise 抛出异常
# ================================================================
section("四、raise 抛出异常")

subsection("raise 主动抛出异常")


def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"age 必须是 int 类型， got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"age 不能为负数: {age}")
    if age > 150:
        raise ValueError(f"age 不合理: {age}")
    print(f"  ✅ age 验证通过: {age}")


for age in [25, -5, 200, "abc"]:
    try:
        validate_age(age)
    except (TypeError, ValueError) as e:
        print(f"  ❌ 验证 {age!r} 失败: {type(e).__name__}: {e}")

subsection("重新抛出异常")


def process_data(data):
    try:
        result = data / 0
    except ZeroDivisionError:
        print("  内部处理: 不能除以零")
        raise  # 重新抛出原异常


try:
    process_data(10)
except ZeroDivisionError:
    print("  外层也捕获到了")

subsection("raise ... from (异常链)")


def read_config():
    try:
        with open("nonexistent_config.json") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError("配置文件读取失败") from e


try:
    read_config()
except RuntimeError as e:
    print(f"  捕获到: {e}")
    print(f"  原始异常 (from): {e.__cause__}")

subsection("raise ... from None (禁用异常链)")

try:
    try:
        int("abc")
    except ValueError:
        raise TypeError("转换失败") from None  # 禁用异常链
except TypeError as e:
    print(f"  捕获到: {e}")
    print(f"  __cause__ 为: {e.__cause__}")  # None


# ================================================================
# 五、自定义异常
# ================================================================
section("五、自定义异常类")

# 5.1 基础自定义异常
subsection("基础自定义异常")


class BusinessError(Exception):
    """业务逻辑错误基类"""

    pass


class InsufficientBalanceError(BusinessError):
    """余额不足"""

    def __init__(self, balance: float, required: float):
        self.balance = balance
        self.required = required
        super().__init__(f"余额不足: 当前 {balance:.2f}，需要 {required:.2f}")


class InvalidTransactionError(BusinessError):
    """无效交易"""

    pass


def transfer(balance, amount):
    if amount <= 0:
        raise InvalidTransactionError("转账金额必须为正数")
    if balance < amount:
        raise InsufficientBalanceError(balance, amount)
    return balance - amount


# 测试
transactions = [
    (1000, 500),
    (100, 500),
    (1000, -100),
]
for bal, amt in transactions:
    try:
        new_bal = transfer(bal, amt)
        print(f"  ✅ 转账 {amt} 成功: {bal} -> {new_bal}")
    except InsufficientBalanceError as e:
        print(f"  ❌ 余额不足: {e.balance:.2f} < {e.required:.2f}")
    except InvalidTransactionError as e:
        print(f"  ❌ 无效交易: {e}")
    except BusinessError as e:
        print(f"  ❌ 业务错误: {e}")

# 5.2 异常层级结构
subsection("异常层级结构")


class AppError(Exception):
    """应用错误基类"""

    pass


class DatabaseError(AppError):
    """数据库错误基类"""

    pass


class ConnectionError(DatabaseError):
    """连接错误"""

    pass


class QueryError(DatabaseError):
    """查询错误"""

    pass


class ValidationError(AppError):
    """验证错误"""

    pass


# 捕获父类可以捕获子类
try:
    raise ConnectionError("无法连接数据库")
except DatabaseError as e:
    print(f"  DatabaseError 捕获到 ConnectionError: {e}")

try:
    raise QueryError("SQL 语法错误")
except AppError as e:
    print(f"  AppError 捕获到 QueryError: {e}")


# ================================================================
# 六、assert 断言
# ================================================================
section("六、assert 断言")

subsection("基本用法")


def calculate_discount(price, discount_rate):
    assert 0 <= discount_rate <= 1, f"折扣率必须在 0~1 之间，当前: {discount_rate}"
    assert price > 0, f"价格必须为正数，当前: {price}"
    return price * (1 - discount_rate)


try:
    result = calculate_discount(100, 0.2)
    print(f"  ✅ 计算成功: {result}")
except AssertionError as e:
    print(f"  ❌ 断言失败: {e}")

try:
    result = calculate_discount(100, 1.5)
    print("  ❌ 不应该走到这里")
except AssertionError as e:
    print(f"  ❌ 断言失败: {e}")

# 断言可被 -O 优化标志禁用
subsection("⚠️  注意: Python -O 模式下 assert 会被移除!")
print("  生产环境不要用 assert 做输入验证，应用 if + raise ValueError")


# ================================================================
# 七、异常的捕获顺序与层级
# ================================================================
section("七、异常捕获顺序与层级")

subsection("捕获顺序: 子类在前，父类在后")

try:
    d = {}
    d[1 / 0]  # 触发 ZeroDivisionError
except ZeroDivisionError:
    print("  捕获 ZeroDivisionError (子类)")
except ArithmeticError:
    print("  捕获 ArithmeticError (父类)")
except Exception:
    print("  捕获 Exception (更父类)")

# 错误示例: 父类在前会吞掉子类异常
subsection("❌ 错误示范: 父类在前，子类捕获不到")

try:
    int("abc")
except Exception:
    print("  ❌ Exception 先捕获了，ValueError 分支永远不会执行")
except ValueError:
    print("  这段代码永远不会被执行!")


# ================================================================
# 八、异常信息与堆栈追踪
# ================================================================
section("八、异常信息与堆栈追踪")

subsection("获取异常详细信息")


def function_a():
    function_b()


def function_b():
    function_c()


def function_c():
    raise ValueError("最深层的错误")


try:
    function_a()
except ValueError as e:
    print(f"  异常类型: {type(e).__name__}")
    print(f"  异常消息: {e}")
    print(f"  异常参数: {e.args}")
    print(f"  异常上下文 (__context__): {e.__context__}")
    print(f"  异常链 (__cause__): {e.__cause__}")

subsection("traceback 模块获取堆栈")

try:
    function_a()
except ValueError:
    print("  traceback.format_exc():")
    tb_text = traceback.format_exc()
    for line in tb_text.split("\n")[:8]:
        print(f"    {line}")

subsection("sys.exc_info() 获取当前异常")


def demo_exc_info():
    try:
        raise TypeError("sys.exc_info 演示")
    except TypeError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"  类型: {exc_type}")
        print(f"  值:   {exc_value}")
        print(f"  追踪: {exc_traceback} (对象)")


demo_exc_info()


# ================================================================
# 九、异常处理最佳实践模式
# ================================================================
section("九、异常处理最佳实践模式")

# 9.1 EAFP (Easier to Ask for Forgiveness than Permission)
subsection("模式 1: EAFP - 先执行，出错再处理")


def get_nested_value(d, keys, default=None):
    """安全获取嵌套字典的值"""
    try:
        for key in keys:
            d = d[key]
        return d
    except (KeyError, TypeError):
        return default


data = {"user": {"profile": {"age": 25}}}
print(f"  存在的键:   {get_nested_value(data, ['user', 'profile', 'age'])}")
print(f"  不存在的键: {get_nested_value(data, ['user', 'email'])}")
print(f"  类型错误:   {get_nested_value(data, ['user', 'profile', 'age', 'deep'])}")


# 对比 LBYL (Look Before You Leap) - 不推荐
def get_nested_safe(d, keys, default=None):
    """LBYL 方式 - 繁琐且有竞争条件"""
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


# 9.2 使用 with 保证资源释放
subsection("模式 2: with 语句保证资源释放")


def safe_file_operation(filename):
    try:
        with open(filename, "w") as f:
            f.write("Hello!")
        return True
    except OSError as e:
        print(f"  ❌ 文件操作失败: {e}")
        return False
    # 不需要 finally, with 已经保证了关闭


# 9.3 contextlib.suppress 忽略特定异常
subsection("模式 3: suppress 忽略特定异常")

from contextlib import suppress


def safe_remove(filename):
    """安全删除文件，文件不存在时不报错"""
    with suppress(FileNotFoundError):
        import os

        os.remove(filename)
        print(f"  已删除: {filename}")
    print(f"  忽略了 FileNotFoundError: {filename}")


safe_remove("temp_nonexistent_file_xyz123")

# 9.4 异常转换 (在边界层转换异常)
subsection("模式 4: 在边界层转换异常")


class APIError(Exception):
    """API 层错误"""

    pass


def fetch_data(url):
    """获取数据，将底层异常转换为业务异常"""
    import urllib.error
    import urllib.request

    try:
        response = urllib.request.urlopen(url, timeout=1)
        return response.read().decode()
    except urllib.error.URLError as e:
        raise APIError(f"网络请求失败: {e.reason}") from e
    except TimeoutError:
        raise APIError("请求超时") from None


# 9.5 不要用异常做正常流程控制
subsection("❌ 反模式: 不要用异常做正常流程")

# 反例
results = []
for i in range(100):
    try:
        val = 100 // i
    except ZeroDivisionError:
        continue  # 这是特殊情况，不是"正常流程"
    results.append(val)
print("  反例: 使用异常处理特殊情况 (100 次循环, 跳过除零)")

# 正例: 预先检查
results = []
for i in range(100):
    if i == 0:
        continue
    results.append(100 // i)
print("  正例: 预先检查条件 (更高效)")


# ================================================================
# 十、异常的完整处理流程示例
# ================================================================
section("十、完整异常处理实战: 用户输入验证系统")


class InputError(Exception):
    """输入错误"""

    pass


class ValidationPipeline:
    """输入验证流水线"""

    def validate(self, data):
        try:
            self._validate_type(data)
            self._validate_range(data)
            self._validate_format(data)
            print(f"  ✅ 验证通过: {data}")
            return True
        except InputError as e:
            print(f"  ❌ 输入错误: {e}")
            return False
        except Exception as e:
            print(f"  ❌ 未知错误: {type(e).__name__}: {e}")
            return False

    def _validate_type(self, data):
        if not isinstance(data, (int, float)):
            raise InputError(f"类型错误: 期望数字，得到 {type(data).__name__}")

    def _validate_range(self, data):
        if data < 0:
            raise InputError(f"取值范围错误: 不能为负数 ({data})")
        if data > 1000:
            raise InputError(f"取值范围错误: 太大了 ({data})")

    def _validate_format(self, data):
        import math

        if math.isnan(data):
            raise InputError("格式错误: 不能是 NaN")
        if math.isinf(data):
            raise InputError("格式错误: 不能是无穷数")


pipeline = ValidationPipeline()
test_inputs = [42, -5, 9999, "abc", float("nan"), float("inf"), 3.14]
for inp in test_inputs:
    pipeline.validate(inp)


print("\n" + "=" * 70)
print("演示完成！Python 异常处理机制已全覆盖。")
print("=" * 70)
