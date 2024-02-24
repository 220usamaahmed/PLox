from plox.ast.stmt_visitor import StmtVisitor


class Stmt:

    def accept(self, visitor: StmtVisitor) -> None:
        raise Exception('accept(visitor: StmtVisitor) is not implemented')