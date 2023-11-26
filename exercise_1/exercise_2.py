from exercise_1 import levenshtein_distance
from fuzzingbook import Fuzzer


class FunctionRunner(Fuzzer.ProgramRunner):
    def run_process(self, inp: str = ""):
        # running the stored function (self.program) with the input (inp)
        return self.program(inp)

    def run(self, inp: str = ""):

        try:
            # Try running the function (self.run_process)
            output = (inp, self.run_process(inp))
            exit_code = self.PASS

        except LookupError:
            exit_code = self.FAIL
            output = (inp, None)
        except:
            exit_code = self.UNRESOLVED
            output = (inp, None)

        return (output, exit_code)


def ld_wrapper(inp):
    # Split the input string where '+' occurs
    splits = inp.split('+')

    # Raise ValueError is less than 2 splits available
    if len(splits) < 2:
        raise ValueError("Must contain +    ")

    # Perform LD on first two inputs
    ld_result = levenshtein_distance(splits[0], splits[1])
    return ld_result


def run():
    random_fuzzer = Fuzzer.RandomFuzzer(char_start=43, char_range=15, min_length=1, max_length=20)
    return random_fuzzer.runs(runner=FunctionRunner(ld_wrapper), trials=10)


if __name__ == '__main__':
    for result in run():
        print(result)
