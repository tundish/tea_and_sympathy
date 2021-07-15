import unittest

from collections import ChainMap
from collections import Counter
from types import SimpleNamespace
import uuid


class Construct(ChainMap):

    @classmethod
    def create(cls, uid=None, **kwargs):
        uid = uid or uuid.uuid4()
        return cls(uid, Counter(**kwargs))

    def __init__(self, uid, *maps):
        super().__init__(*maps)
        self.uid = uid


class TypeTests(unittest.TestCase):

    def test_construct(self):
        c = Construct.create()
        self.assertIsInstance(c.uid, uuid.UUID)
