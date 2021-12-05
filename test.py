
from traceback import print_tb

from utils import isTestName, isTest, _ExecutedTest


_ERROR_COLOR = lambda embed: f'\u001b[0;31m {embed} \033[0;0m'
_SUCCESS_COLOR = lambda embed: f'\u001b[0;32m {embed} \033[0;0m'


class Test:

    _subclass_registry = []

    def __init_subclass__(subcls, **kwargs):
        super().__init_subclass__(**kwargs)
        Test.__mk_testmethods_static(subcls)

        tests = {
            f'{subcls.__qualname__}.{key}': val.__func__ for key, val in vars(subcls).items()
            if isTestName(key)
        }
        setattr(subcls, '_tests', tests)

        Test._subclass_registry.append(subcls)

    @staticmethod
    def __mk_testmethods_static(clsobj):
        test_keys = [key for key, val in vars(clsobj).items() if isTest(val)]
        for key in test_keys:
            setattr(clsobj, key, staticmethod(getattr(clsobj, key)))

    @classmethod
    def _run(cls):
        results = []
        for name, test in cls._tests.items():
            _result = None
            tb = None
            try:
                test()
                _result = True
            except AssertionError as e:
                _result = False
                tb = e.__traceback__
            except Exception as e:
                raise e
            finally:
                results.append(_ExecutedTest(name, _result, tb))
        return results


class AssertRaises:

    def __init__(self, exc):
        self.__exc = exc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__exc == exc_type:
            return True
        raise AssertionError(exc_tb)


def run_all():
    if not Test._subclass_registry:
        return

    print('\n')
    for test_class in Test._subclass_registry:
        for result in test_class._run():
            if result.succeeded:
                print(_SUCCESS_COLOR(f'{result.name} succeeded'))
            else:
                print(_ERROR_COLOR(f'{result.name} failed'))
                print_tb(result.tb)
    print('\n')
