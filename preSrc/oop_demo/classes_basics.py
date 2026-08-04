# -*- coding: utf-8 -*-
"""
一、类的基础：实例变量 vs 类变量
"""


def demo():
    print("\n" + "=" * 70)
    print("一、类的基础：实例变量 vs 类变量")
    print("=" * 70)

    # 1. 类变量 (Class Variable) — 所有实例共享
    #    定义在类内部但在方法外部
    class Dog:
        species = "犬科"  # 类变量：所有狗共享同一个值

        def __init__(self, name, age):
            self.name = name   # 实例变量：每个实例独立
            self.age = age     # 实例变量：每个实例独立

    dog1 = Dog("旺财", 3)
    dog2 = Dog("小黑", 5)

    print("\n1) 类变量 vs 实例变量")
    print(f"   dog1.name={dog1.name}, dog1.species={dog1.species}")
    print(f"   dog2.name={dog2.name}, dog2.species={dog2.species}")
    print(f"   id(dog1.species) == id(dog2.species): {dog1.species is dog2.species}")
    print(f"   id(dog1.name) != id(dog2.name): {dog1.name is not dog2.name}")

    # 修改类变量：所有实例都会看到变化
    Dog.species = "Canine (犬科)"
    print(f"\n   修改 Dog.species 后:")
    print(f"   dog1.species = {dog1.species}")
    print(f"   dog2.species = {dog2.species}")

    # 修改实例变量：只影响该实例
    dog1.name = "大黄"
    print(f"\n   修改 dog1.name 后:")
    print(f"   dog1.name = {dog1.name}")
    print(f"   dog2.name = {dog2.name}")

    # 2. 通过 __dict__ 查看变量存储位置
    print("\n2) 变量存储位置")
    print(f"   dog1.__dict__ = {dog1.__dict__}")
    print(f"   dog2.__dict__ = {dog2.__dict__}")
    print(f"   Dog.__dict__ keys = {[k for k in Dog.__dict__.keys() if not k.startswith('__')]}")

    # 3. 变量查找顺序：实例 -> 类 -> 父类
    print("\n3) 变量查找顺序: 实例 -> 类 -> 父类")
    class Cat(Dog):
        pass

    cat = Cat("咪咪", 2)
    print(f"   cat.name (实例变量): {cat.name}")
    print(f"   cat.species (类变量, 从 Dog 继承): {cat.species}")

    # 4. 可变类变量的陷阱
    print("\n4) ⚠️ 可变类变量陷阱")
    class Counter:
        count = []  # 危险！所有实例共享同一个列表

        def __init__(self, name):
            self.name = name

    c1 = Counter("A")
    c2 = Counter("B")
    c1.count.append(1)
    c1.count.append(2)
    print(f"   c1.count = {c1.count}")
    print(f"   c2.count = {c2.count}  ← 也被修改了！共享的是同一个列表！")

    # 正确做法：可变变量应作为实例变量
    class SafeCounter:
        def __init__(self, name):
            self.name = name
            self.count = []  # 实例变量，每个实例独立

    sc1 = SafeCounter("X")
    sc2 = SafeCounter("Y")
    sc1.count.append(1)
    print(f"   sc1.count = {sc1.count}")
    print(f"   sc2.count = {sc2.count}  ← 独立的列表")

    # 5. __init__ 初始化方法
    print("\n5) __init__ 初始化方法")
    class Point:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Point({self.x}, {self.y})"

    p1 = Point()
    p2 = Point(3, 4)
    p3 = Point(x=10)
    print(f"   Point()    = {p1}")
    print(f"   Point(3,4) = {p2}")
    print(f"   Point(x=10)= {p3}")

    # 6. self 的含义
    print("\n6) self 的含义：指向当前实例")
    class Exampler:
        def show(self):
            print(f"   self 就是实例本身, type(self) = {type(self).__name__}")

    ex = Exampler()
    ex.show()
    print(f"   ex.show() 等价于 Exampler.show(ex)")
    Exampler.show(ex)


if __name__ == "__main__":
    demo()
