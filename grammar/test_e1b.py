import ast
import inspect
from ast_utils import ASTDotVisitor

def print_next_if_pos(num):
    if num > 0:
        print(num + 1)

source = inspect.getsource(print_next_if_pos)
my_ast = ast.parse(source)
dotvisitor = ASTDotVisitor()
dotvisitor.visit(my_ast)
