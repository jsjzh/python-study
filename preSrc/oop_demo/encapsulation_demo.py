# -*- coding: utf-8 -*-
"""
五、封装与 @property
"""


def demo():
    print("\n" + "=" * 70)
    print("五、封装与 @property")
    print("=" * 70)

    # ========== 1. 访问控制约定 ==========
    print("\n--- 1. 下划线约定 ---")
    print("    _name  : 单下划线 - 约定为内部使用 (不强制)")
    print("    __name : 双下划线 - 名称改写 (name mangling)")
    print("    __name__: 双下划线前后 - 魔法方法 (不要自定义)")

    class BankAccount:
        def __init__(self, owner, balance=0):
            self.owner = owner          # 公开
            self._balance = balance     # 约定内部使用
            self.__secret = "密钥123"   # 名称改写

        def deposit(self, amount):
            self._balance += amount

        def withdraw(self, amount):
            self._balance -= amount

        def get_balance(self):
            return self._balance

    account = BankAccount("Alice", 1000)
    print(f"\n    account.owner = {account.owner}")
    print(f"    account._balance = {account._balance}  (单下划线，可访问但约定不)")

    # 双下划线名称改写
    print(f"    account.__secret 直接访问会报错!")
    print(f"    account._BankAccount__secret = {account._BankAccount__secret}")

    # ========== 2. @property 属性装饰器 ==========
    print("\n--- 2. @property 基础用法 ---")

    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @property
        def radius(self):
            """getter: 获取半径"""
            return self._radius

        @property
        def area(self):
            """只读属性: 面积"""
            import math
            return math.pi * self._radius ** 2

        @property
        def circumference(self):
            """只读属性: 周长"""
            import math
            return 2 * math.pi * self._radius

    c = Circle(5)
    print(f"    c.radius = {c.radius}")
    print(f"    c.area = {c.area:.2f}")
    print(f"    c.circumference = {c.circumference:.2f}")
    print(f"    c.area = 50  -> AttributeError! 只读属性不能赋值")

    # ========== 3. 带 setter 的 property ==========
    print("\n--- 3. 带 setter 的 property ---")

    class Temperature:
        def __init__(self, celsius=0):
            self._celsius = celsius

        @property
        def celsius(self):
            """读取温度 (摄氏度)"""
            return self._celsius

        @celsius.setter
        def celsius(self, value):
            """设置温度 (带验证)"""
            if value < -273.15:
                raise ValueError("温度不能低于绝对零度 (-273.15°C)")
            self._celsius = value

        @property
        def fahrenheit(self):
            """读取华氏温度 (计算属性)"""
            return self._celsius * 9 / 5 + 32

        @fahrenheit.setter
        def fahrenheit(self, value):
            """通过华氏温度设置"""
            self.celsius = (value - 32) * 5 / 9

        def __repr__(self):
            return f"Temperature({self._celsius}°C)"

    temp = Temperature(25)
    print(f"    temp.celsius = {temp.celsius}")
    print(f"    temp.fahrenheit = {temp.fahrenheit:.1f}")

    temp.celsius = 100
    print(f"    设为100°C: temp.fahrenheit = {temp.fahrenheit:.1f}")

    temp.fahrenheit = 32
    print(f"    设为32°F: temp.celsius = {temp.celsius}")

    # setter 中的验证
    print("    尝试设置 -300°C:")
    try:
        temp.celsius = -300
    except ValueError as e:
        print(f"    ValueError: {e}")

    # ========== 4. 带 deleter 的 property ==========
    print("\n--- 4. 带 deleter 的 property ---")

    class Cache:
        def __init__(self):
            self._data = {}

        @property
        def last_key(self):
            """获取最后一个键"""
            if not self._data:
                return None
            return list(self._data.keys())[-1]

        @last_key.deleter
        def last_key(self):
            """删除最后一个键"""
            if self._data:
                last = list(self._data.keys())[-1]
                del self._data[last]

        def set(self, key, value):
            self._data[key] = value

        def __repr__(self):
            return f"Cache({self._data})"

    cache = Cache()
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    print(f"    cache.last_key = {cache.last_key}")
    print(f"    cache = {cache}")
    del cache.last_key
    print(f"    del cache.last_key 后: {cache}")

    # ========== 5. 计算属性 vs 存储属性 ==========
    print("\n--- 5. 计算属性 vs 存储属性 ---")

    class Product:
        def __init__(self, name, price, discount=0):
            self.name = name
            self.price = price
            self.discount = discount

        @property
        def final_price(self):
            """计算属性 (不存储，每次计算)"""
            return self.price * (1 - self.discount)

        @final_price.setter
        def final_price(self, value):
            """通过最终价格反推折扣"""
            if value > self.price:
                raise ValueError("最终价格不能高于原价")
            self.discount = 1 - value / self.price

    product = Product("商品", 100, discount=0.2)
    print(f"    原价: ¥{product.price}")
    print(f"    折扣: {product.discount*100}%")
    print(f"    最终价: ¥{product.final_price:.2f}")

    product.final_price = 75
    print(f"    设置最终价¥75后: 折扣={product.discount*100:.1f}%, 原价={product.price}")

    # ========== 6. @property 的实际优势 ==========
    print("\n--- 6. @property 实际优势 ---")

    print("    优势1: 数据验证 (setter 中检查合法性)")
    print("    优势2: 延迟计算 (属性只有在访问时才计算)")
    print("    优势3: 兼容旧代码 (从普通属性升级为 property)")
    print("    优势4: 只读/只写控制 (没有 setter 就是只读)")

    class UserProfile:
        """演示：从普通属性迁移到 property"""
        def __init__(self, name):
            # 第一版: self.name = name
            # 第二版: 改为 property 而不改变外部接口
            self._name = name

        @property
        def name(self):
            return self._name.strip().title()

        @name.setter
        def name(self, value):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("名字必须是非空字符串")
            self._name = value.strip()

    user = UserProfile("  alice  ")
    print(f"    user.name (自动清理格式): {user.name}")
    user.name = "bob"
    print(f"    user.name = {user.name}")
    try:
        user.name = ""
    except ValueError as e:
        print(f"    空字符串报错: {e}")


if __name__ == "__main__":
    demo()
