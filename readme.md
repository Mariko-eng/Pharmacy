class MyClass:
    # Class-level attribute
    class_variable = "I am a class-level attribute"

    def __init__(self, instance_variable):
        # Instance-level attribute
        self.instance_variable = instance_variable

    def print_attributes(self):
        # Accessing both class-level and instance-level attributes
        print(f"Class-level attribute: {MyClass.class_variable}")
        print(f"Instance-level attribute: {self.instance_variable}")


# Creating instances of the class
obj1 = MyClass("Instance 1")
obj2 = MyClass("Instance 2")

# Accessing class-level attribute
print(MyClass.class_variable)  # Outputs: I am a class-level attribute

# Accessing instance-level attributes
obj1.print_attributes()
obj2.print_attributes()


Difference betweeen @classmethod and @staticmethod in python

In Python, both @classmethod and @staticmethod are decorators that can be used to define methods within a class, but they serve different purposes.

# @classmethod:
A method decorated with @classmethod takes a reference to the class itself as its first parameter, conventionally named cls.
It allows the method to access and modify class-level attributes or call other class-level methods.
It is commonly used for factory methods or methods that involve the class itself.

class MyClass:
    class_variable = "Hello"

    @classmethod
    def print_class_variable(cls):
        print(cls.class_variable)

MyClass.print_class_variable()  # Outputs: Hello

# @staticmethod:
A method decorated with @staticmethod does not take a reference to the class or instance as its first parameter.
It behaves like a regular function but is defined within a class for organization purposes.
It cannot access or modify class-level attributes or call other class-level methods.

class MyClass:
    @staticmethod
    def print_hello():
        print("Hello")

MyClass.print_hello()  # Outputs: Hello

In summary:

Use @classmethod when you need access to class-level attributes or methods.
Use @staticmethod when the method does not require access to class-level attributes and behaves like a utility function within the class.