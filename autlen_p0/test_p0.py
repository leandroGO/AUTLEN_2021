#!/usr/bin/env python

import re
import unittest

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5


class TestP0(unittest.TestCase):
    """Tests of assignment 0."""

    def check_expression(self, expr: str, string: str, expected: bool) -> None:
        with self.subTest(string=string):
            match = re.fullmatch(expr, string)
            self.assertEqual(bool(match), expected)

    def test_exercise_0(self) -> None:
        self.check_expression(RE0, "asdfaASEasdf", True)
        self.check_expression(RE0, "as1dfaASEasdf", False)
        self.check_expression(RE0, "", False)

    def test_exercise_1(self) -> None:
        self.check_expression(RE1, "ejemplo.py", True)
        self.check_expression(RE1, "ejemplo.c", False)
        self.check_expression(RE1, ".py", False)
        self.check_expression(RE1, "_ejemplo_19.py", True)
        self.check_expression(RE1, "ejemplo-19.py", False)

    def test_exercise_2(self) -> None:
        self.check_expression(RE2, "2344", True)
        self.check_expression(RE2, "2344.", True)
        self.check_expression(RE2, "2344.0012", True)
        self.check_expression(RE2, "0.0012", True)
        self.check_expression(RE2, "0", True)
        self.check_expression(RE2, ".023", True)
        self.check_expression(RE2, "-2344", True)
        self.check_expression(RE2, "-2344.", True)
        self.check_expression(RE2, "-2344.0012", True)
        self.check_expression(RE2, "-0.0012", True)
        self.check_expression(RE2, "-0", True)
        self.check_expression(RE2, "-.023", True)
        self.check_expression(RE2, "023", False)
        self.check_expression(RE2, "1.5e-7", False)

    def test_exercise_3(self) -> None:
        self.check_expression(RE3, "juan.rufo@uam.es", True)
        self.check_expression(RE3, "juan.rufo@estudiante.uam.es", True)
        self.check_expression(RE3, "juan.rufo@gmail.com", False)
        self.check_expression(RE3, "juan@uam.es", False)

    def test_exercise_4(self) -> None:
        self.check_expression(RE4, "asd (sdsdf) cs (aa) sdfsdf", True)
        self.check_expression(RE4, "asd (sdsdf) cs (aa) sdfsdf))", False)
        self.check_expression(RE4, "()", True)
        self.check_expression(RE4, "()()()()()()", True)
        self.check_expression(RE4, "hola", False)
        self.check_expression(RE4, "(())", False)

    def test_exercise_5(self) -> None:
        self.check_expression(RE5, "asd (sdsdf) cs (aa) sdfsdf", True)
        self.check_expression(RE5, "asd (sdsdf) cs (aa) sdfsdf))", False)
        self.check_expression(RE5, "()", True)
        self.check_expression(RE5, "()()()()()()", True)
        self.check_expression(RE5, "hola", False)
        self.check_expression(RE5, "(())()(())()()()((a))()()", True)
        self.check_expression(RE5, "(())()(())()(()())()(())()()", True)
        self.check_expression(RE5, "((()))", False)


if __name__ == '__main__':
    unittest.main()
