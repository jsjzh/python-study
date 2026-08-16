"""
四、继承与多态
"""


def demo():
    print("\n" + "=" * 70)
    print("四、继承与多态")
    print("=" * 70)

    # ========== 1. 单继承 ==========
    print("\n--- 1. 单继承 ---")

    class Animal:
        """父类 (基类)"""

        kingdom = "动物界"

        def __init__(self, name, age):
            self.name = name
            self.age = age

        def eat(self):
            print(f"    {self.name} 在吃东西")

        def sleep(self):
            print(f"    {self.name} 在睡觉")

        def __repr__(self):
            return f"{self.__class__.__name__}({self.name}, {self.age})"

    class Dog(Animal):
        """子类：继承 Animal"""

        species = "犬科"

        def bark(self):
            print(f"    {self.name} 在汪汪叫")

        def fetch(self):
            print(f"    {self.name} 在捡球")

    dog = Dog("旺财", 3)
    print(f"    dog = {dog}")
    dog.eat()  # 继承自 Animal
    dog.sleep()  # 继承自 Animal
    dog.bark()  # Dog 自己的方法
    dog.fetch()  # Dog 自己的方法
    print(f"    dog.kingdom = {dog.kingdom}")  # 继承的类变量
    print(f"    dog.species = {dog.species}")  # Dog 的类变量

    # ========== 2. 方法覆盖 (Override) ==========
    print("\n--- 2. 方法覆盖 (Override) ---")

    class Cat(Animal):
        def __init__(self, name, age, indoor=True):
            super().__init__(name, age)  # 调用父类 __init__
            self.indoor = indoor

        def make_sound(self):
            print(f"    {self.name} 在喵喵叫")

        def eat(self):
            """覆盖父类的 eat 方法"""
            super().eat()  # 先调用父类方法
            print(f"    {self.name} 是一只优雅地吃")

        def __repr__(self):
            return f"Cat({self.name}, {self.age}, indoor={self.indoor})"

    cat = Cat("咪咪", 2, indoor=True)
    print(f"    cat = {cat}")
    cat.eat()  # 调用的是 Cat 覆盖后的版本
    cat.sleep()  # 仍然是 Animal 的版本

    # ========== 3. super() 的使用 ==========
    print("\n--- 3. super() 的使用 ---")

    class Employee:
        def __init__(self, name, salary):
            self.name = name
            self.salary = salary

        def get_info(self):
            return f"员工: {self.name}, 月薪: {self.salary}"

    class Manager(Employee):
        def __init__(self, name, salary, department):
            # 调用父类构造器
            super().__init__(name, salary)
            self.department = department

        def get_info(self):
            # 扩展父类方法
            base_info = super().get_info()
            return f"{base_info}, 部门: {self.department}"

    mgr = Manager("张经理", 20000, "技术部")
    print(f"    mgr.get_info() = {mgr.get_info()}")

    # ========== 4. 多继承 ==========
    print("\n--- 4. 多继承 (MRO) ---")

    class Flyable:
        def fly(self):
            print("    能飞")

    class Swimmable:
        def swim(self):
            print("    能游泳")

    class Runnable:
        def run(self):
            print("    能跑")

    class Duck(Flyable, Swimmable, Runnable):
        def __init__(self, name):
            self.name = name

    duck = Duck("唐老鸭")
    duck.fly()
    duck.swim()
    duck.run()

    # 查看 MRO (方法解析顺序)
    print(f"    Duck.__mro__: {[c.__name__ for c in Duck.__mro__]}")

    # ========== 5. 菱形继承问题 ==========
    print("\n--- 5. 菱形继承与 C3 线性化 ---")

    class A:
        def greet(self):
            print("    A.greet()")

    class B(A):
        def greet(self):
            print("    B.greet()")
            super().greet()

    class C(A):
        def greet(self):
            print("    C.greet()")
            super().greet()

    class D(B, C):
        def greet(self):
            print("    D.greet()")
            super().greet()

    d = D()
    d.greet()
    print(f"    D.__mro__: {[c.__name__ for c in D.__mro__]}")

    # ========== 6. 多态 ==========
    print("\n--- 6. 多态 (Polymorphism) ---")

    class Shape:
        """抽象基类"""

        def area(self):
            raise NotImplementedError("子类必须实现 area()")

        def name(self):
            return "Shape"

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius

        def area(self):
            import math

            return math.pi * self.radius**2

        def name(self):
            return "圆"

    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height

        def name(self):
            return "矩形"

    class Triangle(Shape):
        def __init__(self, base, height):
            self.base = base
            self.height = height

        def area(self):
            return 0.5 * self.base * self.height

        def name(self):
            return "三角形"

    def print_area(shape):
        """多态：不关心具体类型，只要是 Shape 就行"""
        print(f"    {shape.name()} 面积: {shape.area():.2f}")

    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 8),
    ]
    for s in shapes:
        print_area(s)

    # ========== 7. isinstance vs type ==========
    print("\n--- 7. isinstance() vs type() ---")

    dog = Dog("旺财", 3)
    print(f"    isinstance(dog, Dog):      {isinstance(dog, Dog)}")
    print(f"    isinstance(dog, Animal):   {isinstance(dog, Animal)}")  # True!
    print(f"    type(dog) is Dog:          {type(dog) is Dog}")
    print(f"    type(dog) is Animal:       {type(dog) is Animal}")  # False!
    print("    isinstance 检查继承链，type 只检查精确类型")

    # ========== 8. 抽象基类 ==========
    print("\n--- 8. 抽象基类 (ABC) ---")

    from abc import ABC, abstractmethod

    class Payment(ABC):
        @abstractmethod
        def pay(self, amount):
            """子类必须实现"""
            pass

        @abstractmethod
        def refund(self, amount):
            """子类必须实现"""
            pass

        def description(self):
            return "支付系统"

    class Alipay(Payment):
        def pay(self, amount):
            return f"支付宝支付 ¥{amount}"

        def refund(self, amount):
            return f"支付宝退款 ¥{amount}"

    class WeChatPay(Payment):
        def pay(self, amount):
            return f"微信支付 ¥{amount}"

        def refund(self, amount):
            return f"微信退款 ¥{amount}"

    alipay = Alipay()
    wechat = WeChatPay()
    print(f"    {alipay.pay(100)}")
    print(f"    {wechat.refund(50)}")
    print(f"    isinstance(alipay, Payment): {isinstance(alipay, Payment)}")

    # 尝试实例化抽象类会报错
    print("    Payment() 会报 TypeError! (抽象类不能直接实例化)")


if __name__ == "__main__":
    demo()
