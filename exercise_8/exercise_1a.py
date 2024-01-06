from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, PowerSchedule, Mutator
from fuzzingbook.GreyboxGrammarFuzzer import LangFuzzer, GreyboxGrammarFuzzer, FragmentMutator, AFLSmartSchedule, \
    RegionMutator
from fuzzingbook.Parser import EarleyParser
from html_grammar import HTML_GRAMMAR
import os

seeds = []
for i in range(50):
    with open(os.path.join('html', f'{i}.html'), 'r') as fp:
        seeds.append(fp.read())


def get_random_fuzzer() -> RandomFuzzer:
    return RandomFuzzer()


def get_grammar_fuzzer(grammar) -> GrammarFuzzer:
    return GrammarFuzzer(grammar)


def get_mutation_fuzzer(seeds) -> MutationFuzzer:
    return MutationFuzzer(seed=seeds)


def get_greybox_fuzzer(seeds) -> GreyboxFuzzer:
    mutator = Mutator()
    schedule = PowerSchedule()
    return GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)


def get_lang_fuzzer(seeds, grammar) -> LangFuzzer:
    parser = EarleyParser(grammar)
    mutator = FragmentMutator(parser=parser)
    schedule = PowerSchedule()
    return LangFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)


def get_greybox_grammar_fuzzer(seeds, grammar) -> GreyboxGrammarFuzzer:
    byte_mutator = Mutator()
    parser = EarleyParser(grammar)
    tree_mutator = RegionMutator(parser=parser)
    schedule = AFLSmartSchedule(parser=parser)
    return GreyboxGrammarFuzzer(seeds=seeds, tree_mutator=tree_mutator, byte_mutator=byte_mutator, schedule=schedule)


assert isinstance(get_random_fuzzer(), RandomFuzzer)
assert isinstance(get_mutation_fuzzer(seeds=seeds), MutationFuzzer)
assert isinstance(get_greybox_fuzzer(seeds), GreyboxFuzzer)
assert isinstance(get_greybox_grammar_fuzzer(seeds=seeds, grammar=HTML_GRAMMAR), GreyboxGrammarFuzzer)
assert isinstance(get_lang_fuzzer(seeds=seeds, grammar=HTML_GRAMMAR), LangFuzzer)
