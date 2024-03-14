from .utils import capture_stdout, run_code
import textwrap


def test(capture_stdout):
    source = """
        var a = "global a";
        var b = "global b";
        var c = "global c";
        {
            var a = "outer a";
            var b = "outer b";
            {
                var a = "inner a";
                print a;
                print b;
                print c;
            }
            print a;
            print b;
            print c;
        }
        print a;
        print b;
        print c;    
    """

    expected = (
        textwrap.dedent(
            """
        inner a
        outer b
        global c
        outer a
        outer b
        global c
        global a
        global b
        global c
    """
        ).strip()
        + "\n"
    )

    run_code(source, capture_stdout)
    assert capture_stdout["stdout"] == expected
