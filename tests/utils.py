import pytest
import sys
from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.resolver import Resolver
from plox.scanner import Scanner


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s: str):
        assert isinstance(buffer["stdout"], str)
        assert isinstance(buffer["write_calls"], int)

        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer


def run_code(code: str):
    interpreter = Interpreter()

    scanner = Scanner(code)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    resolver = Resolver(interpreter)
    resolver.resolve(statements)

    interpreter.interpret(statements)
