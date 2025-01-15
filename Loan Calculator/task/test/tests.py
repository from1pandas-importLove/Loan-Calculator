from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class LoanCalcTest(StageTest):
    def generate(self):
        return [
            TestCase(
                stdin='1000\n200',
                attach=5,
            ),
            TestCase(
                stdin='1000\n1000',
                attach=1,
            ),
            TestCase(
                stdin='1000\n100',
                attach=10,
            ),
        ]

    def check(self, reply, attach):
        reply = reply.lower()
        if not any(char.isdigit() for char in reply):
            return CheckResult.wrong('Your program didn\'t print the number of months required to replay the loan.')
        elif str(attach) not in reply:
            return CheckResult.wrong('Incorrect number of months required to replay the loan.\n'
                f'Expected: {attach}')

        return CheckResult.correct()


if __name__ == '__main__':
    LoanCalcTest('creditcalc.creditcalc').run_tests()