from os import walk, unlink
from os.path import join
import textwrap
from typing import List, Literal, Tuple

OUTPUT_PATH = "../plox/ast/"
EXPRESSIONS: List[Tuple[str, str]] = [
    ("Assign", "name: Token, value: Expr"),
    ("Binary", "left: Expr, operator: Token, right: Expr"),
    ("Call", "callee: Expr, paren: Token, params: List[Expr]"),
    ("Get", "object: Expr, name: Token"),
    ("Grouping", "expression: Expr"),
    ("Literal", "value: object"),
    ("Logical", "left: Expr, operator: Token, right: Expr"),
    ("Set", "object: Expr, name: Token, value: Expr"),
    ("Super", "keyword: Token, method: Token"),
    ("This", "keyword: Token"),
    ("Unary", "operator: Token, right: Expr"),
    ("Variable", "name: Token"),
]
STATEMENTS: List[Tuple[str, str]] = [
    ("Block", "statements: List[Stmt]"),
    ("Function", "name: Token, params: List[Token], body: List[Stmt]"),
    ("Class",
     "name: Token, superclass: Variable, method: List[Function]"),
    ("Expression", "expression: Expr"),
    ("If", "condition: Expr, thenBranch: Stmt, elseBranch: Stmt"),
    ("Print", "expression: Expr"),
    ("Return", "keyword: Token, expr: Expr"),
    ("VariableDeclaration", "name: Token, initializer: Expr"),
    ("While", "condition: Expr, body: Stmt"),
]


def generate_expr_types(content_type: Literal["Expr", "Stmt"], content: List[Tuple[str, str]]):
    code = f"""
        from typing import TYPE_CHECKING, List
        from plox.token import Token
        from plox.ast.expr_interface import Expr

        if TYPE_CHECKING:
            from plox.ast.{content_type.lower()}_visitor import {content_type}Visitor
    """

    class_code = ""
    for name, params in content:
        param_names = map(lambda x: x.split(":")[0], params.split(", "))
        class_code += textwrap.dedent(f"""
            class {name}({content_type}):

                def __init__(self, {params}):      
        """)
        for param in param_names:
            class_code += f"{' ' * 8}self.{param} = {param}\n"

        class_code += textwrap.indent(textwrap.dedent(f"""
            def accept(self, visitor: '{content_type}Visitor'):
                return visitor.visit_{name.lower()}_{content_type.lower()}(self)
        """), "    ")

        class_code += "\n"

    code = textwrap.dedent(code).strip()
    if content_type == "Stmt":
        code += "\nfrom plox.ast.stmt_interface import Stmt"
        code += "\nfrom plox.ast.expr_types import Variable"

    code += "\n\n" + class_code
    create_file(join(OUTPUT_PATH, f"{content_type.lower()}_types.py"), code)


def generate_expr_visitor(content_type: Literal["Expr", "Stmt"], content: List[Tuple[str, str]]):
    imports = ", ".join(map(lambda x: x[0], content))
    code = f"""
        from plox.ast.{content_type.lower()}_types import {imports}
        from typing import Any


        class {content_type}Visitor: 
    """

    for name, params in content:
        code += f"""
            def visit_{name.lower()}_{content_type.lower()}(self, {content_type.lower()}: {name}) -> Any:
                raise Exception('visit_{name.lower()}_{content_type.lower()}({params}) not implemented')

        """

    code = textwrap.dedent(code).strip()
    create_file(join(OUTPUT_PATH, f"{content_type.lower()}_visitor.py"), code)


def generate_expr_interface(content_type: Literal["Expr", "Stmt"], content: List[Tuple[str, str]]):
    code = textwrap.dedent(f"""
        from typing import TYPE_CHECKING, Any
        if TYPE_CHECKING:
            from plox.ast.{content_type.lower()}_visitor import {content_type}Visitor

                              
        class {content_type}:

            def accept(self, visitor: '{content_type}Visitor') -> Any:
                raise Exception('accept(visitor: {content_type}Visitor) is not implemented')
    """).strip()

    create_file(
        join(OUTPUT_PATH, f"{content_type.lower()}_interface.py"), code)


def generate_expressions():
    create_file(join(OUTPUT_PATH, "__init__.py"))

    generate_expr_interface("Expr", EXPRESSIONS)
    generate_expr_visitor("Expr", EXPRESSIONS)
    generate_expr_types("Expr", EXPRESSIONS)

    generate_expr_interface("Stmt", STATEMENTS)
    generate_expr_visitor("Stmt", STATEMENTS)
    generate_expr_types("Stmt", STATEMENTS)


def create_file(path: str, code: str = ''):
    print(f"Creating file {path}")

    with open(path, '+a') as file:
        file.write(code)


def clear_old_files():
    for root, _, files in walk(OUTPUT_PATH):
        for file in files:
            path = join(root, file)
            print(f"Deleting {path}")
            unlink(path)


def main():
    clear_old_files()
    generate_expressions()


if __name__ == '__main__':
    main()
