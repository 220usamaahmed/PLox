from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner


def test_if_else_statement():
    source = """
        var name = "Usama";
        var age = 25;
        
        if (age == 24 and name == "Usama")
            print "Hello";
        else
            print "Bye";
    """

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)
