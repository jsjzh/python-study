import types


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student("king", 18)


print(isinstance(stu, Student))


def demo(name: str = "de"):
    print(name)


print(type(demo) == types.FunctionType)
print(isinstance(None, object))
print(dir(stu))

obj = {"name": "king"}

print(isinstance(obj, object))

print(hasattr(stu, "name"))
print(stu.name)

# print(hasattr(obj, "name"))
# print(getattr(obj, "name"))

print(obj.get("names", 404))
print(getattr(obj, "name", 404))
