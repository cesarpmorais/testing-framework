from TestCase import TestCase, TestResult, TestSuite
from test_TestCase import TestSpy, TestStub


class TestLoader:

    TEST_METHOD_PREFIX = "test"

    def get_test_case_names(self, test_case_class):
        methods = dir(test_case_class)
        test_method_names = list(
            filter(lambda method: method.startswith(self.TEST_METHOD_PREFIX), methods)
        )
        return test_method_names

    def make_suite(self, test_case_class):
        suite = TestSuite()
        for test_method_name in self.get_test_case_names(test_case_class):
            test_method = test_case_class(test_method_name)
            suite.add_test(test_method)
        return suite


class TestLoaderTest(TestCase):

    def test_create_suite(self):
        loader = TestLoader()
        suite = loader.make_suite(TestStub)
        assert len(suite.tests) == 3

    def test_create_suite_of_suites(self):
        loader = TestLoader()
        stub_suite = loader.make_suite(TestStub)
        spy_suite = loader.make_suite(TestSpy)

        suite = TestSuite()
        suite.add_test(stub_suite)
        suite.add_test(spy_suite)

        assert len(suite.tests) == 2

    def test_get_multiple_test_case_names(self):
        loader = TestLoader()
        names = loader.get_test_case_names(TestStub)
        assert names == ["test_error", "test_failure", "test_success"]

    def test_get_no_test_case_names(self):

        class Test(TestCase):
            def foobar(self):
                pass

        loader = TestLoader()
        names = loader.get_test_case_names(Test)
        assert names == []


class TestRunner:

    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        test.run(self.result)
        print(self.result.summary())
        return self.result


loader = TestLoader()
suite = loader.make_suite(TestLoaderTest)

runner = TestRunner()
runner.run(suite)
