|License| |Version| |Downloads|

.. |License| image:: https://img.shields.io/pypi/l/enforcetypes
   :alt: License
   :target: https://github.com/RivenSkaye/EnforceTypes/blob/master/LICENSE
.. |Version| image:: https://img.shields.io/pypi/v/enforcetypes
   :alt: PyPI
   :target: https://pypi.org/project/EnforceTypes/
.. |Downloads| image:: https://static.pepy.tech/personalized-badge/enforcetypes?period=total&units=none&left_color=gray&right_color=green&left_text=Downloads
   :target: https://pepy.tech/project/enforcetypes
   :alt: PePy stats

############
EnforceTypes
############

Simple decorators for enforcing types during runtime.

The idea behind this is to reduce time spent developing and using packages
that are computationally intensive by allowing for early raising and exiting
rather than running for a long time and failing on type or class problems.
Currently the easiest way to do this, which is most commonly seen in packages
and modules that have type hints applied, is by adding ``isinstance`` checks
and ``assert`` statements throughout the code. This quickly becomes repetitive,
doesn't help readability of the code and can easily be forgotten.

The decorators provided in this module resolve that problem by handling these
type checks (as annotated) and raising when unexpected types are provided.
They also aid in debugging and development by providing both the expected type
and the provided argument's runtime type.
There are separate decorators for functions and classes, please do not use them
the wrong way around.

Due to some very iffy results and instability in the way decorators work when combined,
please try using decorators in a different order *before* submitting bug reports.
I can't help that, it's a limitation with the way Python itself handles it.

I'm working on combining common use cases (such as ``@dataclass`` which has already
been implemented) and would gladly take suggestions!
I've also been putting some effort into splitting the package, so auto-imports and
``__all__`` might be somewhat affected until v0.1.0, which I'll release once I'm
confident that it's mostly stable (except for the API)

.. code-block:: python

   from EnforceTypes import classtypes, functypes, methtypes


   @functypes
   def add(a: int, b: int) -> None:
       print(f"Adding {a} to {b} equals {a + b}")


   add(2, 2)  # prints "Adding 2 to 2 equals 4"
   add("a", 2)  # This causes the decorator to raise a TypeError!

   @classtypes
   class Add:
       def __init__(a: int, b: int):
           self.a = a
           self.b = b

       @property
       def printadd(self):
           print(f"Adding {self.a} to {self.b} equals {self.add()}")

       @classmethod
       @methtypes
       def add_values(cls, *, a: int = 1, b: int = 1) -> int:
           obj = cls(a, b)
           return obj.add()

       @methtypes
       def add(self) -> int:
           return self.a + self.b


   Add(1, 1).printadd  # prints 2
   a = Add(1, "a")  # TypeError raised because of a `str` instead of an `int`.
   Add(1, "b").printadd  # This causes a TypeError too, before instantiating an `Add` object!
   Add.add_values(b=5)  # returns 6
   a = Add(10, 20)
   a.add()  # returns 30
