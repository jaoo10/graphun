import unittest
from progunit import *

class TestCaseTest(unittest.TestCase):
    def test_run(self):
        events = []
        expected_program_result = ProgramResult(0, "1", "2")
        def program():
            events.append('program')
            return expected_program_result
        def check(test_result, program_result):
            events.append('check')
            self.assertIs(expected_program_result, program_result)
            test_result.add_error("erro1", 0, 1)

        test_case = TestCase("test1", program, check)
        test_result = test_case.run()
        self.assertEqual(['program', 'check'], events)
        self.assertEqual(1, len(test_result.errors))
        error = test_result.errors[0]
        self.assertEqual("erro1", error.msg)
        self.assertEqual(0, error.expected)
        self.assertEqual(1, error.actual)

    def test_run_exception(self):
        def program():
            raise Exception()
        def check(test_result, program_result):
            self.fail("should not be called")
        
        test_case = TestCase("test1", program, check)
        test_result = test_case.run()
        self.assertFalse(test_result.success())

class RunnerTest(unittest.TestCase):
    def test_run(self):
        class TestCase(object):
            def __init__(self, num):
                self.num = num
            def run(self):
                return self.num
        test_cases = [TestCase(1), TestCase(2), TestCase(3)]
        events = []
        class Reporter(object):
            def start(self):
                events.append('start')
            def end(self):
                events.append('end')
            def start_test(self, test_case):
                events.append('start_test %d' % test_case.num)
            def end_test(self, test_case, result):
                events.append('end_test %d %d' % (test_case.num, result))

        runner = Runner(test_cases, Reporter())
        runner.run()
        self.assertEqual(['start',
                          'start_test 1', 'end_test 1 1',
                          'start_test 2', 'end_test 2 2',
                          'start_test 3', 'end_test 3 3',
                          'end'],
                          events)

class ReporterTest(unittest.TestCase):
    def test(self):
        events = []
        class TestResult(object):
            def __init__(self, _success, num):
                self._success = _success
                self.num = num
            def success(self):
                return self._success
        class MyReporter(Reporter):
            def _on_success(self, test_case, test_result):
                events.append('success %d %d' % (test_case, test_result.num))
            def _on_failure(self, test_case, test_result):
                events.append('failure %d %d' % (test_case, test_result.num))
        tests_results = [TestResult(True, 0), TestResult(True, 1), TestResult(False, 2)]
        reporter = MyReporter()
        reporter.start()
        for i, test_result in enumerate(tests_results):
            reporter.start_test(i)
            reporter.end_test(i, test_result)
        reporter.end()
        self.assertEqual(['success 0 0', 'success 1 1', 'failure 2 2'], events)
        self.assertEqual(3, reporter.total)
        self.assertEqual(2, reporter.success)

class TestTimeStr(unittest.TestCase):
    def test(self):
        self.assertEquals('123ms', time_str(123))
        self.assertEquals('1s 123ms', time_str(1123))
        self.assertEquals('1m 5s', time_str(65123))
        self.assertEquals('1h 3m', time_str(3789123))

if __name__ == '__main__':
    unittest.main()
