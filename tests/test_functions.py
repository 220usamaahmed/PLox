import textwrap
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


def test_return_statement(capture_stdout):
    source = """
        fun fib(n) {
            if (n <= 1) return n;         
            return fib(n - 1) + fib(n - 2);
        }

        for (var i = 1; i < 10; i = i + 1) {
            print i + ": " + fib(i);
        }
    """

    expected = (
        textwrap.dedent(
            """
        1: 1
        2: 1
        3: 2
        4: 3
        5: 5
        6: 8
        7: 13
        8: 21
        9: 34
    """
        ).strip()
        + "\n"
    )

    run_code(source, capture_stdout)
    assert expected == capture_stdout["stdout"]


def test_closures(capture_stdout):
    source = """
        fun makeCounter() {
            var i = 0;
            fun count() {
                i = i + 1;
                print i;
            }

            return count;
        }

        var counter = makeCounter();
        counter(); // "1".
        counter(); // "2".
        counter(); // "3".
    """

    expected = (
        textwrap.dedent(
            """
        1
        2
        3
    """
        ).strip()
        + "\n"
    )

    run_code(source, capture_stdout)
    assert expected == capture_stdout["stdout"]
