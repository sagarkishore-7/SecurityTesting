"""
Use this file to implement your solution for exercise 5-1 b.
"""
from fuzzingbook.Fuzzer import RandomFuzzer
from exercise_2a import FunctionCoverageRunner
import html


class RandomCoverageFuzzer(RandomFuzzer):

    def runs(self, runner: FunctionCoverageRunner):
        max_consecutive_failures = 10
        result = []

        for _ in range(max_consecutive_failures):
            iteration_result, iteration_coverage = self.run_iteration(runner)
            result.append(iteration_result)

            if iteration_coverage:
                break

        return result

    def run_iteration(self, runner: FunctionCoverageRunner):
        iteration_result = self.run(runner)
        iteration_coverage = runner.coverage
        return iteration_result, iteration_coverage


if __name__ == '__main__':
    fuzzer = RandomCoverageFuzzer()
    print(fuzzer.runs(FunctionCoverageRunner(html.escape)))
