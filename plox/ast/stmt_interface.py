from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from plox.ast.stmt_visitor import StmtVisitor


class Stmt:

    def accept(self, visitor: 'StmtVisitor') -> Any:
        raise Exception('accept(visitor: StmtVisitor) is not implemented')