from fuzzingbook.Grammars import Grammar, crange, is_valid_grammar, opts
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from fuzzingbook.GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarCoverageFuzzer
from fuzzingbook.WebFuzzer import WebFormFuzzer, HTMLGrammarMiner, cgi_encode
from luhn import luhn

def calculate_luhn_check_sum(digits):
    return digits[:-1] + str(luhn(digits[:-1]))

def request_generator(name, lastname, email, password, password2, banking):
    return (f"/register?name={name}&lastname={lastname}&email={email}&password={password}&password2={password2}&banking={banking}")

flags = {'name_flag':False,
         'lastname_flag':False,
         'mail_flag':False,
         'password_exists_flag':False,
         'password_short_flag':False,
         'password_long_flag':False,
         'password2_flag':False
         }

def modify_and_send_request(name, lastname, email, password, password2, banking):
    if not flags['name_flag']:
        flags['name_flag'] = True
        name = '1'
    if not flags['lastname_flag']:
        flags['lastname_flag'] = True
        lastname = '1'
    if not flags['password_exists_flag']:
        flags['password_exists_flag'] = True
        password = 'password1'
        password2 = 'password1'
    elif not flags['password2_flag']:
        flags['password2_flag'] = True
        password2 = 'password1'
    elif all([flags['name_flag'], flags['lastname_flag'], flags['password_exists_flag'], flags['password2_flag']]):
        if not flags['password_short_flag']:
            flags['password_short_flag'] = True
            password = cgi_encode('pa#')
            password2 = cgi_encode('pa#')
        elif not flags['password_long_flag']:
            flags['password_long_flag'] = True
            password = cgi_encode('pass#' * 5)
            password2 = cgi_encode('pass#' * 5)
        elif not flags['mail_flag']:
            flags['mail_flag'] = True
            email = email + '.saarland'

    request = request_generator(name, lastname, email, password, password2, banking)
    return request

REGISTRATION_GRAMMAR: Grammar = {
    "<start>": ["<registration>"],
    "<registration>": [("/register?name=<name>&lastname=<lastname>&email=<email>"
                       "&password=<password>&password2=<password2>&banking=<banking>",
                       opts(post=modify_and_send_request)
                       )],
    "<name>": ["Leon", "Marius"],
    "<lastname>": ["Bettscheider", "Smytzek"],
    "<email>": [cgi_encode("leon.bettscheider@cispa.de"), cgi_encode("marius.smytzek@cispa.de")],
    "<password>": [cgi_encode("password#")],
    "<password2>": [cgi_encode("password#")],
    "<banking>": [("<digits>",
                   opts(post=calculate_luhn_check_sum)
                   )],
    "<digits>": ["<digit>" * 16],
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(REGISTRATION_GRAMMAR)

def get_fuzzer(httpd_url):
    return GeneratorGrammarFuzzer(REGISTRATION_GRAMMAR)
