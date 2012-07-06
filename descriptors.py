###
# Discovering Descriptors
#
# 6th July
#
# Peter Inglesby
# @inglesp / peter.inglesby@gmail.com
#
# https://github.com/inglesp/Discovering-Descriptors
###

# Goals:
#  * explain the descriptor protocol
#  * demonstrate how descriptors are used in implementation of Python
#  * provide examples of how descriptors can be used in your own code

# Let's get going
class C:
    class_attr = 123
    def __init__(self):
        self.instance_attr = 456

i = C()
i.instance_attr
i.class_attr

# What happens when we look up an attribute on an instance?
i.__dict__
C.__dict__

# Where do descriptors come in?
class RandomAttribute:
    def __init__(self, n):
        self.n = n
    def __get__(self, inst, cls):
        import random
        print("calling __get__ on instance of RandomAttribute")
        return random.randint(1, self.n)

class C:
    random_attr = RandomAttribute(10)

i = C()
i.__dict__
C.__dict__
i.random_attr
i.random_attr
i.random_attr

# A descriptor is an object that defines at least one of:
#  * __get__()
#  * __set__()
#  * __delete__()

# How about something more interesting?
class CachedAttribute:
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def __get__(self, inst, cls):
        print("calling __get__ on instance of CachedAttribute")
        inst.__dict__[self.name] = self.func(inst)
        return inst.__dict__[self.name]

class C:
    def expensive_calculation(self):
        import time
        time.sleep(5)
        return 42
    attr = CachedAttribute('attr', expensive_calculation)

i = C()
i.__dict__
i.attr
i.__dict__
i.attr

# One more (useless) example
class NoisyDescriptor:
    def __get__(self, inst, cls):
        print("calling __get__ on instance of NoisyDescriptor")
        print("  self:", self)
        print("  inst:", inst)
        print("  cls: ", cls)

class C:
    attr = NoisyDescriptor()

i = C()
i.attr
i
C.attr

# Some motivation
class C:
    def a_method(self):
        print("called a method on instance %s" % id(self))

i = C()
i.a_method()
C.a_method(i)
i.a_method
C.a_method
i.__dict__
C.__dict__['a_method']
C.__dict__['a_method'].__get__(i, C)
C.__dict__['a_method'].__get__(None, C)

# What about setting attributes?
class C:
    class_attr = 123
    def __init__(self):
        self.instance_attr = 456

i = C()
i.__dict__
C.__dict__
i.instance_attr = 321
i.__dict__
i.class_attr = 654
i.__dict__
C.__dict__

# A useless example
class NoisyDescriptor:
    def __set__(self, inst, val):
        print("calling __set__ on instance of NoisyDescriptor")
        print("  self:", self)
        print("  inst:", inst)
        print("  val: ", val)

class C:
    attr = NoisyDescriptor()

i = C()
i.attr = 123
C.attr = 123
C.__dict__

# A less useless example
class TypedAttribute:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
    def __set__(self, inst, val):
        if isinstance(val, self.typ):
            inst.__dict__[self.name] = val
        else:
            raise TypeError

class Person:
    name = TypedAttribute('name', str)
    age = TypedAttribute('age', int)

i = Person()
i.name = 'Bill'
i.age = 25
i.__dict__
i.age = '25'
i.__dict__['age'] = 'definitely not a number'
i.age

# Slots
class C:
    __slots__ = ['x', 'y']

i = C()
i.x = 123
i.x
i.y = 456
i.y
i.z = 789
i.__dict__
C.__dict__
C.__dict__['x'].__get__(i, C)
i.x
C.__dict__['x'].__set__(i, 789)
i.x

# What are slots for?
#  * Efficiency!
#  * Faster access
#  * Lower occupancy

# Properties
class C:
    def __init__(self, x):
        self._x = x
    def get_x(self):
        print('getting x')
        return self._x
    def set_x(self, x):
        print('setting x')
        self._x = x
    x = property(get_x, set_x)

i = C(123)
i.__dict__
i.x
i.x = 456
i.__dict__
C.__dict__['x']
C.__dict__['x'].__get__(i, C)
i.x
C.__dict__['x'].__set__(i, 789)
i.x

# A more useful example
class MarsProbe(object):
    def get_distance_meters(self):
        return self._distance_meters
    def set_distance_meters(self, dist):
        self._distance_meters = dist * 1.0
    def get_distance_yards(self):
        return self._distance_meters / 0.9144
    def set_distance_yards(self, dist):
        self._distance_meters = dist * 0.9144
    distance_meters = property(get_distance_meters, set_distance_meters)
    distance_yards = property(get_distance_yards, set_distance_yards)

i = MarsProbe()
i.distance_yards = 120
i.distance_meters

# How to choose between descriptors and properties?
#  * Properties work best when they know about the class
#  * Descriptors are more general, can often apply to any class
#  * Use descriptors if behaviour is different for classes and instances
#  * Properties are syntactic sugar
#  * Experiment!

# What next?
#  * Read
#     - Data Model reference
#     - 'Descriptor HowTo Guide'
#     - 'Unifying types and classes in Python 2.2'
#     - Guido's History of Python blog
#  * Read code
#     - Lots of good examples in Django, such as related objects
#     - Hyrbid attributes in SQLAlchemy
#     - Tools/demo/eiffel.py
#     - $ grep __get__ site_packages
#  * Play
#     - Implement methods, __slots__, properties in pure Python
#     - Tinker with the CPython source (grep for 'tp_descr_get')
#     - Work out why C.__dict__ has an attribute called '__dict__'

# Finally:
#  * Ignore everything I've just said

import this

# Thanks!



