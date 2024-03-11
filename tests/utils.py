import pytest
import sys
from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner


@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = { "stdout": "", "write_calls": 0 }

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, 'write', fake_write)
    return buffer


def run_code(code: str, capture_stdout) -> str:
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)