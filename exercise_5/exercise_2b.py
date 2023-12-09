"""
Use this file to implement your solution for exercise 5-1 b.
"""
from fuzzingbook.Fuzzer import RandomFuzzer
from exercise_2a import FunctionCoverageRunner
import html


class RandomCoverageFuzzer(RandomFuzzer):
    
    def runs(self, runner: FunctionCoverageRunner):
        pass


if __name__ == '__main__':
    fuzzer = RandomCoverageFuzzer()
    print(fuzzer.runs(FunctionCoverageRunner(html.escape)))
