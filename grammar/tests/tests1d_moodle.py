import ast
import inspect
import unittest

from ast_utils import ASTRemoveConstantIf

def simple_fun():
    if True:
        return 1
    else:
        return 0

def nested_fun():
    if True:
        if False:
            return 1
        else:
            return 2
    else:
        return 0

class TestIfASTRemoveConstantIf(unittest.TestCase):
    """Tests for ASTRemoveConstantIf."""

    def _assertNumNodeValue(self, node: ast.AST, value: float) -> None:
        self.assertIsInstance(node, (ast.Num, ast.Constant))
        if isinstance(node, ast.Num):
            self.assertEqual(node.n, value)
        else:
            self.assertEqual(node.value, value)

    def test_simple(self) -> None:
        """Test optimization simple case."""
        source = inspect.getsource(simple_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 1)

    def test_nested(self) -> None:
        """Test case with nested ifs."""
        source = inspect.getsource(nested_fun)
        parsed_ast = ast.parse(source)
        transformed_ast = ASTRemoveConstantIf().visit(parsed_ast)

        self.assertIsInstance(transformed_ast, ast.Module)
        self.assertTrue(len(transformed_ast.body) == 1)
        fundef = transformed_ast.body[0]
        self.assertIsInstance(fundef, ast.FunctionDef)
        self.assertTrue(len(fundef.body) == 1)
        ret1 = fundef.body[0]
        self.assertIsInstance(ret1, ast.Return)
        ret1val = ret1.value
        self._assertNumNodeValue(ret1val, 2)

if __name__ == "__main__":
    unittest.main()
