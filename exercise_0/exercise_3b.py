import random
from fuzzingbook.Fuzzer import RandomFuzzer

if __name__ == '__main__':
    random.seed()
    random_fuzzer = RandomFuzzer()
    data = random_fuzzer.fuzz() # call the fuzzer function here to generate data
    with open('solution_3b.txt', 'w') as f:
        f.write(data)