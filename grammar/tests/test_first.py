import unittest
from typing import AbstractSet

from grammar.grammar import Grammar
from grammar.utils import GrammarFormat

class TestFirst(unittest.TestCase):
    def _check_first(
        self,
        grammar: Grammar,
        input_string: str,
        first_set: AbstractSet[str],
    ) -> None:
        with self.subTest(
            string=f"First({input_string}), expected {first_set}",
        ):
            computed_first = grammar.compute_first(input_string)
            self.assertEqual(computed_first, first_set)

    def test_case1(self) -> None:
        """Test Case 1."""
        grammar_str = """
        E -> TX
        X -> +E
        X ->
        T -> iY
        T -> (E)
        Y -> *T
        Y ->
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {'(', 'i'})
        self._check_first(grammar, "T", {'(', 'i'})
        self._check_first(grammar, "X", {'', '+'})
        self._check_first(grammar, "Y", {'', '*'})
        self._check_first(grammar, "", {''})
        self._check_first(grammar, "Y+i", {'+', '*'})
        self._check_first(grammar, "YX", {'+', '*', ''})
        self._check_first(grammar, "YXT", {'+', '*', 'i', '('})
        self._check_first(grammar, "XT", {'+', '(', 'i'})
        with self.assertRaises(ValueError):
            grammar.compute_first("foo")

    def test_case2(self) -> None:
        """Test case 2 (for recursion)"""
        grammar_str = """
        E-> T
        T-> EX
        X -> x
        E -> 
        E -> e
        """

        grammar = GrammarFormat.read(grammar_str)
        self._check_first(grammar, "E", {"e", "x"})
        self._check_first(grammar, "T", {"e", "x"})
        self._check_first(grammar, "X", {"x"})

if __name__ == '__main__':
    unittest.main()
