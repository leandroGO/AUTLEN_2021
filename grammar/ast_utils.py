import ast
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
        self.n_node += 1
        if self.last_parent:
            print(f's{self.last_parent} -> s{self.n_node} [label = "{self.last_field_name}"]')

        self.level += 1
        self.last_parent = self.n_node
        for field, value in iter_fields(node):
            self.last_field_name = str(field)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
            else:
                node_args += f'{field}={value!r}, '


        self.level -= 1
        if node_args != "":
            node_args = node_args[:-2]

        print(node_str + node_args + ')"]')

        if self.level == 0:
            print("}")

