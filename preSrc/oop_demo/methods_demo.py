"""
二、方法的三种类型：实例方法、类方法、静态方法
"""


def demo():
    print("\n" + "=" * 70)
    print("二、方法的三种类型：实例方法、类方法、静态方法")
    print("=" * 70)

    class MathUtils:
        """数学工具类 - 演示三种方法"""

        # 类变量
        pi = 3.14159

        def __init__(self, value):
            self.value = value

        # 1. 实例方法 (Instance Method)
        #    - 第一个参数是 self (实例)
        #    - 可访问实例变量和类变量
        #    - 通过 实例.方法() 或 类.方法(实例) 调用
        def double(self):
            """实例方法：计算实例值的两倍"""
            return self.value * 2

        def display(self):
            """实例方法：显示信息"""
            print(f"    [实例方法] value={self.value}, pi={self.pi}")

        # 2. 类方法 (Class Method)
        #    - 使用 @classmethod 装饰器
        #    - 第一个参数是 cls (类本身)
        #    - 只能访问类变量，不能访问实例变量
        #    - 通过 类.方法() 或 实例.方法() 调用
        @classmethod
        def from_string(cls, s):
            """类方法：从字符串创建实例 (工厂方法)"""
            value = float(s.replace("值=", "").strip())
            return cls(value)

        @classmethod
        def info(cls):
            """类方法：显示类信息"""
            print(f"    [类方法] 类名={cls.__name__}, pi={cls.pi}")

        # 3. 静态方法 (Static Method)
        #    - 使用 @staticmethod 装饰器
        #    - 不需要 self 或 cls 参数
        #    - 不能访问实例变量或类变量 (除非显式传参)
        #    - 相当于一个放在类里的普通函数
        @staticmethod
        def is_positive(x):
            """静态方法：判断是否为正数"""
            return x > 0

        @staticmethod
        def help():
            """静态方法：帮助信息"""
            print("    [静态方法] MathUtils: 数学工具类")
            print("      - double(): 计算两倍")
            print("      - from_string(): 从字符串创建")
            print("      - is_positive(): 判断正数")

    # ========== 演示三种方法 ==========
    print("\n1) 实例方法 (Instance Method)")
    mu1 = MathUtils(5)
    mu2 = MathUtils(10)
    print(f"   mu1.value = {mu1.value}")
    print(f"   mu1.double() = {mu1.double()}")
    print(f"   mu2.double() = {mu2.double()}")
    MathUtils.display(mu1)  # 等价于 mu1.display()

    print("\n2) 类方法 (Class Method)")
    mu3 = MathUtils.from_string("值=42")
    print(f"   MathUtils.from_string('值=42') -> value={mu3.value}")
    MathUtils.info()  # 通过类调用
    mu1.info()  # 通过实例也能调用 (但通常通过类调用)

    print("\n3) 静态方法 (Static Method)")
    print(f"   MathUtils.is_positive(5) = {MathUtils.is_positive(5)}")
    print(f"   MathUtils.is_positive(-3) = {MathUtils.is_positive(-3)}")
    MathUtils.help()
    mu1.help()  # 也可以通过实例调用

    # ========== 对比总结 ==========
    print("\n4) 三种方法对比总结")
    print("   ┌─────────────┬──────────┬──────────┬──────────┐")
    print("   │    类型      │ 第一个参数│ 访问实例 │ 访问类   │")
    print("   ├─────────────┼──────────┼──────────┼──────────┤")
    print("   │ 实例方法     │ self     │    ✅    │    ✅    │")
    print("   │ 类方法       │ cls      │    ❌    │    ✅    │")
    print("   │ 静态方法     │ 无       │    ❌    │    ❌    │")
    print("   └─────────────┴──────────┴──────────┴──────────┘")

    # ========== 工厂方法模式 ==========
    print("\n5) 类方法的典型用途：工厂方法")

    class User:
        def __init__(self, name, role):
            self.name = name
            self.role = role

        def __repr__(self):
            return f"User({self.name}, {self.role})"

        @classmethod
        def admin(cls, name):
            return cls(name, "admin")

        @classmethod
        def editor(cls, name):
            return cls(name, "editor")

        @classmethod
        def viewer(cls, name):
            return cls(name, "viewer")

    print(f"   User.admin('Alice') = {User.admin('Alice')}")
    print(f"   User.editor('Bob')  = {User.editor('Bob')}")
    print(f"   User.viewer('Carol')= {User.viewer('Carol')}")

    # ========== 静态方法的典型用途 ==========
    print("\n6) 静态方法的典型用途：工具函数")

    class StringHelper:
        @staticmethod
        def reverse(s):
            return s[::-1]

        @staticmethod
        def is_palindrome(s):
            """判断回文"""
            return s == s[::-1]

        @staticmethod
        def word_count(s):
            return len(s.split())

    print(f"   reverse('Python')    = {StringHelper.reverse('Python')}")
    print(f"   is_palindrome('aba') = {StringHelper.is_palindrome('aba')}")
    print(f"   is_palindrome('abc') = {StringHelper.is_palindrome('abc')}")
    print(
        f"   word_count('Hello World from OOP') = {StringHelper.word_count('Hello World from OOP')}"
    )


if __name__ == "__main__":
    demo()
