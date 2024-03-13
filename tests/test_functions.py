from .utils import capture_stdout, run_code


def test_argument_passing(capture_stdout):
    source = """
        fun sayHi(first, last) {
            print "Hi, " + first + " " + last + "!";
        }

        sayHi("Dear", "Reader");
    """

    run_code(source, capture_stdout)
    assert capture_stdout["stdout"] == "Hi, Dear Reader!\n" 

# def test_return_statement(capture_stdout):
def test_return_statement():
    source = """
        fun fib(n) {
            if (n <= 1) return n;         
            return fib(n - 1) + fib(n - 2);
        }

        for (var i = 1; i < 10; i = i + 1) {
            print i + ": " + fib(i);
        }
    """

    run_code(source, capture_stdout)