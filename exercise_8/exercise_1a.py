from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, PowerSchedule, Mutator
from fuzzingbook.GreyboxGrammarFuzzer import LangFuzzer, GreyboxGrammarFuzzer, FragmentMutator, AFLSmartSchedule, RegionMutator
from fuzzingbook.Parser import EarleyParser


def get_random_fuzzer() -> RandomFuzzer:
    pass


def get_grammar_fuzzer(grammar) -> GrammarFuzzer:
    pass


def get_mutation_fuzzer(seeds) -> MutationFuzzer:
    pass


def get_greybox_fuzzer(seeds) -> GreyboxFuzzer:
    pass


def get_lang_fuzzer(seeds, grammar) -> LangFuzzer:
    pass


def get_greybox_grammar_fuzzer(seeds, grammar) -> GreyboxGrammarFuzzer:
    pass
