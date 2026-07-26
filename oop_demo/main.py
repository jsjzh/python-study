# -*- coding: utf-8 -*-
"""
oop_demo 主入口 - 汇总演示所有面向对象知识点

运行方式: python -m oop_demo.main
或:      python oop_demo/main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oop_demo.classes_basics import demo as demo_basics
from oop_demo.methods_demo import demo as demo_methods
from oop_demo.magic_methods import demo as demo_magic
from oop_demo.inheritance_demo import demo as demo_inheritance
from oop_demo.encapsulation_demo import demo as demo_encapsulation


def main():
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "Python 面向对象编程全演示" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")

    sections = [
        ("一、类基础", demo_basics),
        ("二、方法类型", demo_methods),
        ("三、魔法方法", demo_magic),
        ("四、继承多态", demo_inheritance),
        ("五、封装属性", demo_encapsulation),
    ]

    for title, func in sections:
        input(f"\n按 Enter 运行 [{title}]...")
        func()

    print("\n" + "=" * 70)
    print("  🎉 所有面向对象知识点演示完毕!")
    print("=" * 70)
    print("""
  📚 知识点总结:
  
  1. 类 = 属性 (数据) + 方法 (行为)
  2. 变量: 实例变量 (self.x) vs 类变量 (Class.x)
  3. 方法: 实例方法(self) vs 类方法(cls) vs 静态方法(无)
  4. 魔法方法: __init__, __str__, __add__, __getitem__ 等
  5. 继承: 单继承、多继承、方法覆盖、super()
  6. 多态: 同一接口不同实现
  7. 封装: _name, __name, @property
  
  📂 文件结构:
  oop_demo/
  ├── __init__.py          # 包初始化
  ├── main.py              # 主入口 (本文件)
  ├── classes_basics.py    # 类基础
  ├── methods_demo.py      # 方法类型
  ├── magic_methods.py     # 魔法方法
  ├── inheritance_demo.py  # 继承多态
  └── encapsulation_demo.py # 封装属性
""")


if __name__ == "__main__":
    main()
