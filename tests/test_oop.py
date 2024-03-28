import textwrap
from .utils import capture_stdout, run_code


def test_argument_passing(capture_stdout):
    source = """
        class Foo {}
        print Foo;

        var foo = Foo();
        print foo;
    """

    expected = (
        textwrap.dedent(
            """
            Foo
            Foo instance
    """
        ).strip()
        + "\n"
    )

    run_code(source)
    assert capture_stdout["stdout"] == expected


def test_field_geter_and_seter(capture_stdout):
    source = """
        class Foo {}
        var foo = Foo();

        foo.bar = "baz";
        print foo.bar;
    """

    run_code(source)
    assert capture_stdout["stdout"] == "baz\n"


def test_method_call(capture_stdout):
    source = """
        class Foo {
            bar() {
                print "baz";
            }
        }

        var foo = Foo();
        foo.bar();
    """

    run_code(source)
    assert capture_stdout["stdout"] == "baz\n"


def test_this(capture_stdout):
    source = """
        class Cake {
            taste() {
                var adjective = "delicious";
                print "The " + this.flavor + " cake is " + adjective + "!";
            }
        }

        var cake = Cake();
        cake.flavor = "German chocolate";
        cake.taste(); // Prints "The German chocolate cake is delicious!".
    """

    run_code(source)
    assert capture_stdout["stdout"] == "The German chocolate cake is delicious!\n"


def test_this_with_callbacks(capture_stdout):
    source = """
        class Thing {
        getCallback() {
            fun localFunction() {
                print this;
                }

                return localFunction;
            }
        }

        var callback = Thing().getCallback();
        callback();
    """

    run_code(source)
    assert capture_stdout["stdout"] == "Thing instance\n"


def test_initializer(capture_stdout):
    source = """
    class Circle {
        init(radius) {
            this.radius = radius;
        }

        area() {
            return 3.141592653 * this.radius * this.radius;
        }
    }

    var circle = Circle(4);
    print circle.area(); // Prints roughly "50.2655".
    """

    run_code(source)
    assert capture_stdout["stdout"].startswith("50.265")


def test_inheritance(capture_stdout):
    source = """
        class Doughnut {
            cook() {
                print "Fry until golden brown.";
            }
        }

        class BostonCream < Doughnut {}

        BostonCream().cook();
    """

    run_code(source)
    assert capture_stdout["stdout"] == "Fry until golden brown.\n"