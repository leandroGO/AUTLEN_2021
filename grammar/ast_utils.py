import ast
import inspect
import types
from typing import Union, List
from ast import iter_fields
import numbers


class ASTMagicNumberDetector(ast.NodeVisitor):
    def __init__(self):
        self.magic_numbers = 0

    def _check_magic_number(self, number: complex) -> None:
        if isinstance(number, numbers.Number):
            if number != 0 and number != 1 and number != 1j:
                self.magic_numbers += 1

    def visit_Num(self, node: ast.Num) -> None:
        self._check_magic_number(node.n)

    # Para Python >= 3.8
    def visit_Constant(self, node: ast.Constant) -> None:
        self._check_magic_number(node.value)


class ASTDotVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.level = 0
        self.n_node = 0
        self.last_parent: Optional[int] = None
        self.last_field_name = ""

    def generic_visit(self, node: ast.AST) -> None:
        if self.level == 0:
            print("digraph {")

        node_str = f's{self.n_node} [label = "{type(node).__name__}('
        node_args = ""
        current = self.n_node
        if self.last_parent is not None:
            print(f's{self.last_parent} -> s{self.n_node} [label = "{self.last_field_name}"]')

        self.n_node += 1
        self.level += 1
        for field, value in iter_fields(node):
            self.last_field_name = str(field)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.last_parent = current
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.last_parent = current
                self.visit(value)
            else:
                node_args += f'{field}={value!r}, '


        self.level -= 1
        if node_args != "":
            node_args = node_args[:-2]  # Quita el último ', '

        print(node_str + node_args + ')"]')

        if self.level == 0:
            print("}")


class ASTReplaceNum(ast.NodeTransformer):
    def __init__(self, number:complex):
        self.number = number

    def visit_Num(self, node:ast.Num) -> ast.AST:
        return ast.Num(n=self.number)

    def visit_Constant(self, node:ast.Constant) -> ast.AST:
        if isinstance(node.value, numbers.Number):
            return ast.Constant(value=self.number)
        return node


def transform_code(f, transformer):
    f_ast = ast.parse(inspect.getsource(f))

    new_tree = ast.fix_missing_locations(transformer.visit(f_ast))

    old_code = f.__code__
    code = compile(new_tree, old_code.co_filename, 'exec')
    new_f = types.FunctionType(code.co_consts[0], f.__globals__)

    return new_f


class ASTRemoveConstantIf(ast.NodeTransformer):
    def visit_If(self, node: ast.If) -> Union[ast.AST, List[ast.stmt]]:
        if isinstance(node.test, ast.NameConstant):
            if node.test.value:
                return node.body
            return node.orelse
        return node
