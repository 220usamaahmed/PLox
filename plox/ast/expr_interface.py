from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from plox.ast.expr_visitor import ExprVisitor


class Expr:

    def accept(self, visitor: 'ExprVisitor') -> Any:
        raise Exception('accept(visitor: ExprVisitor) is not implemented')