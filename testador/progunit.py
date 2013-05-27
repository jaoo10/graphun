# encoding: utf-8

import sys
import codecs
import traceback
from time import time

class ProgramResult(object):
    def __init__(self, retcode, out, err):
        self.retcode = retcode
        self.out = out
        self.err = err


class TestCase(object):
    def __init__(self, description, program, check):
        self.description = description
        self.program = program
        self.check = check
        self.stopwatch = Stopwatch()

    def run(self):
        try:
            self.stopwatch.start()
            program_result = self.program()
            program_result.time = self.stopwatch.elapsed()
            test_result = TestResult(self, program_result)
            self.check(test_result, program_result)
            return test_result
        except Exception as e:
            test_result = TestResult(self)
            test_result.add_error("internal error: " + str(e)
                                  + "\n".join(traceback.format_tb(sys.exc_traceback)))
            return test_result


class ResultError(object):
    def __init__(self, msg, expected = None, actual = None):
        self.msg = msg
        self.expected = expected
        self.actual = actual
        #TODO: if expected is None?
        if (self.expected == None and self.actual != None) or (self.expected == None and self.actual != None):
            raise Exception()
            
    def simple(self):
        return not self.expected


class TestResult(object):
    def __init__(self, test_case, program_result = None):
        self.program_result = program_result
        self.test_case = test_case
        self.errors = []
    
    def add_error(self, msg, expected = None, actual = None):
        self.errors.append(ResultError(msg, expected, actual))

    def success(self):
        return not self.errors


class Runner(object):
    def __init__(self, test_cases, reporter):
        self.test_cases = test_cases
        self.reporter = reporter
    
    def run(self):
        self.reporter.start()
        for test_case in self.test_cases:
            self.reporter.start_test(test_case)
            test_result = test_case.run()
            self.reporter.end_test(test_case, test_result)
        self.reporter.end()


class Reporter(object):
    def __init__(self):
        self.total = 0
        self.success = 0

    def start(self):
        pass

    def end(self):
        pass

    def start_test(self, test_case):
        self.total += 1

    def end_test(self, test_case, test_result):
        if test_result.success():
            self._on_success(test_case, test_result)
            self.success += 1
        else:
            self._on_failure(test_case, test_result)

    def _on_success(self):
        pass

    def _on_failure(self):
        pass


class SimpleReporter(Reporter):
    def __init__(self, logfile, out = sys.stdout):
        Reporter.__init__(self)
        self.logfile = logfile
        self._out = out
        self._log = codecs.open(logfile, "w", "utf-8")
        self.stopwatch = Stopwatch()

    def start(self):
        self.stopwatch.start()

    def end(self):
        elapsed = time_str(self.stopwatch.elapsed())
        self._write(u'Total: %d  Errors: %d (%s)\n' % (self.total, self.total - self.success, elapsed))

    def start_test(self, test_case):
        super(SimpleReporter, self).start_test(test_case)
        self._write(test_case.description + ": ")

    def _write(self, s):
        self._write_out(s)
        self._write_log(s)

    def _write_log(self, s, level = 0):
        self._log.write(u" " * level * 2 + s)
        self._log.flush()

    def _write_log_lines(self, lines, level):
        for line in lines:
            self._write_log(line + "\n", level)
    
    def _write_out(self, s):
        self._out.write(s)
        self._out.flush()

    def _on_success(self, test_case, test_result):
        self._write("OK (%s)\n" % time_str(test_result.program_result.time))

    def _on_failure(self, test_case, test_result):
        self._write_out("Fail (see '%s' file)\n" % self.logfile)
        self._write_log("Fail\n")
        if test_result.program_result:
            self._write_log("** STDOUT **\n", level = 1)
            self._write_log_lines(test_result.program_result.out.splitlines(), level = 2)
            self._write_log("** STDERR **\n", level = 1)
            self._write_log_lines(test_result.program_result.err.splitlines(), level = 2)
        self._write_log("** ERRORS **\n", level = 1)
        for error in test_result.errors:
            self._write_log(error.msg + "\n", level = 2)
            if not error.simple():
                #TODO: if expected or actual is multiline
                self._write_log(u"Expected: " + unicode(error.expected) + "\n", level = 3)
                self._write_log(u"Result  : " + unicode(error.actual) + "\n", level = 3)


# Stopwatch

class Stopwatch(object):
    def __init__(self):
        self.start()

    def start(self):
        self._started = time()

    def elapsed(self):
        self._elapsed = time() - self._started
        return int(1000 * self._elapsed)

def units(value, prefix, last_prefix):
    r = []
    for factor, symbol in prefix:
        d = value % factor
        value = value / factor
        r.append((d, symbol))
        if value == 0:
            break
    if value != 0:
        r.append((value, last_prefix))
    return r

def time_str(value):
    r = units(value, [(1000, 'ms'), (60,  's'), (60,  'm'), (60,  'h')], 'd')
    r = list(reversed(r))[:2]
    return ' '.join(['%d%s' % (v, u) for v, u in r])

# utilities
def exec_program(cmd):
    from subprocess import Popen, PIPE
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return ProgramResult(p.returncode, out.decode('utf-8'), err.decode('utf-8'))

def create_program(cmd):
    def run():
        return exec_program(cmd)
    return run
