# class MetaClass(type):
#     def __init__(cls, name, bases, attrs):
#         print('Defining %s' % cls)
#         print('Name: %s' % name)
#         print('Bases: %s' % (bases,))
#         print('Attributes:')
#         for (name, value) in attrs.items():
#             print('    %s: %r' % (name, value))
#
#
# class RealClass(object, metaclass=MetaClass):
#     spam = 'eggs'
#
#
# class su(RealClass):
#     shi=1
#
#
# class BaseAttribute():
#     creation_counter = 1
#
#     def __init__(self):
#         self.creation_counter = BaseAttribute.creation_counter
#         BaseAttribute.creation_counter += 1
#         print(self.creation_counter)
#
#
# x = BaseAttribute()
# z = BaseAttribute()
# f = BaseAttribute()
# print(vars(BaseAttribute))

def add(a, b, c):
    return a + b + c

args = (2, 3)

print(add(*args,1))