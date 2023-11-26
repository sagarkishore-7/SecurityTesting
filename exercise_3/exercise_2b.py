"""
Use this file to implement your solution for exercise 3-2 a.
"""

from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from re_coverage import get_coverage

from exercise_2 import RE_GRAMMAR
from exercise_2a import RE_GRAMMAR_EXPANDED

import random

random.seed()

def run_fuzzer(fuzzer, grammar, num_trials=25):
    total_coverage = 0
    for trial in range(num_trials):
        generated_input = fuzzer(grammar)
        total_coverage += get_coverage(generated_input)
    return total_coverage / num_trials

# run the experiment for GrammarFuzzer with RE_GRAMMAR
coverage_GF_RE = run_fuzzer(GrammarFuzzer, RE_GRAMMAR)
# run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR
coverage_GCF_RE = run_fuzzer(GrammarCoverageFuzzer, RE_GRAMMAR)
# run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR_EXPANDED
coverage_GCF_REX = run_fuzzer(GrammarCoverageFuzzer, RE_GRAMMAR_EXPANDED)

print(f'GrammarFuzzer: {coverage_GF_RE}'.format(0)) # print the average code coverage for GrammarFuzzer + RE_GRAMMAR
print(f'GrammarCoverageFuzzer: {coverage_GCF_RE}'.format(0)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR
print(f'GrammarCoverageFuzzer+: {coverage_GCF_REX}'.format(0)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR_EXPANDED
