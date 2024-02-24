from plox.ast.expr_visitor import ExprVisitor


class Expr:

    def accept(self, visitor: ExprVisitor) -> None:
        raise Exception('accept(visitor: ExprVisitor) is not implemented')