import ast
import inspect
from ast_utils import ASTMagicNumberDetector

def my_fun(p):
    if p == 1:
        print(p + 1j)
    elif p == 5:
        print(0)
    else:
        print(p - 27.3 * 3j)

source = inspect.getsource(my_fun)
my_ast = ast.parse(source)
magic_detector = ASTMagicNumberDetector()
magic_detector.visit(my_ast)
print(magic_detector.magic_numbers)
# Debería dar 3

