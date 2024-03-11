from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner


def test_while_loop():
    source = """
        var count = 0;
        while (count < 10) {
            print count;
            count = count + 1;
        }    
    """

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)

def test_for_loop():
    source = """
        for (var i = 0; i < 10; i = i + 1) {
            print i;
        }
    """

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)