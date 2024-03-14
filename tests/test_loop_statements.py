from .utils import capture_stdout, run_code
import pytest


def test_while_loop(capture_stdout):
    source = """
        var count = 0;
        while (count < 10) {
            print count;
            count = count + 1;
        }    
    """

    run_code(source, capture_stdout)
    assert capture_stdout["stdout"] == "\n".join(map(str, list(range(10)))) + "\n"


def test_for_loop(capture_stdout):
    source = """
        for (var i = 0; i < 10; i = i + 1) {
            print i;
        }
    """

    run_code(source, capture_stdout)
    assert capture_stdout["stdout"] == "\n".join(map(str, list(range(10)))) + "\n"
