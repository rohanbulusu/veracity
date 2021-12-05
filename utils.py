
from types import FunctionType


class _ExecutedTest:
    __slots__ = ('name', 'succeeded', 'tb')
    def __init__(self, name: str, succeeded: bool, tb):
        self.name = name
        self.succeeded = succeeded
        self.tb = tb


def isTestName(candidate):
    test_prefixes = ['test', 'Test']
    return any(prefix in candidate for prefix in test_prefixes)

def isTest(candidate):
    if not isinstance(candidate, FunctionType):
        return False
    return isTestName(candidate.__name__)
