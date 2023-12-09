from examples import examples
from fuzzingbook.Parser import Parser, EarleyParser
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarMiner

RE_GRAMMAR = {
    '<start>': ['<re>'],
    '<re>': ['<alternative>', '^<alternative>', '<alternative>$', '^<alternative>$'],
    '<alternative>': ['<concat>', '<concat>|<alternative>'],
    '<concat>': ['', '<concat><regex>'],
    '<regex>': ['<symbol>', '<symbol>*', '<symbol>+', '<symbol>?', '<symbol>{<range>}'],
    '<symbol>': ['.', '<char>', '(<alternative>)'],
    '<char>': ['a', 'b', 'c'],
    '<range>': ['<num>', ',<num>', '<num>,'],
    '<num>': ['1', '2'],
}

def learn_probabilities():
    
    p = EarleyParser(RE_GRAMMAR)     
    m = ProbabilisticGrammarMiner(p)     
    return m.mine_probabilistic_grammar(examples) 


print(learn_probabilities())