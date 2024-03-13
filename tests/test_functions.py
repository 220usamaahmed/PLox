from .utils import capture_stdout, run_code


def test(capture_stdout):
    source = """
        fun sayHi(first, last) {
            print "Hi, " + first + " " + last + "!";
        }

        sayHi("Dear", "Reader");
    """

    run_code(source, capture_stdout)
    assert capture_stdout["stdout"] == "Hi, Dear Reader!\n" 
