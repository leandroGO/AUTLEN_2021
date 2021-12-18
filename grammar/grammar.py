from __future__ import annotations

from collections import deque
from typing import AbstractSet, Collection, MutableSet, Optional

class RepeatedCellError(Exception):
    """Exception for repeated cells in LL(1) tables."""

class SyntaxError(Exception):
    """Exception for parsing errors."""

class Production:
    """
    Class representing a production rule.

    Args:
        left: Left side of the production rule. It must be a character
            corresponding with a non terminal symbol.
        right: Right side of the production rule. It must be a string
            that will result from expanding ``left``.

    """

    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.left == other.left
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.left!r} -> {self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.left, self.right))

class Grammar:
    """
    Class that represent a grammar.

    Args:
        terminals: Terminal symbols of the grammar.
        non_terminals: Non terminal symbols of the grammar.
        productions: Production rules of the grammar.
        axiom: Axiom of the grammar.

    """

    def __init__(
        self,
        terminals: AbstractSet[str],
        non_terminals: AbstractSet[str],
        productions: Collection[Production],
        axiom: str,
    ) -> None:
        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        if axiom not in non_terminals:
            raise ValueError(
                "Axiom must be included in the set of non terminals.",
            )

        for p in productions:
            if p.left not in non_terminals:
                raise ValueError(
                    f"{p}: "
                    f"Left symbol {p.left} is not included in the set "
                    f"of non terminals.",
                )
            if p.right is not None:
                for s in p.right:
                    if (
                        s not in non_terminals
                        and s not in terminals
                    ):
                        raise ValueError(
                            f"{p}: "
                            f"Invalid symbol {s}.",
                        )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.productions = productions
        self.axiom = axiom

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"axiom={self.axiom!r}, "
            f"productions={self.productions!r})"
        )


    def compute_first(self, sentence: str) -> AbstractSet[str]:
        """
        Method to compute the first set of a string.

        Args:
            str: string whose first set is to be computed.

        Returns:
            First set of str.
        """

        return self._compute_first_rec(sentence, set())

    def _compute_first_rec(self, sentence: str, visited: AbstractSet[str]) -> AbstractSet[str]:
        primeros = set()

        if sentence == "" or sentence is None:
            return set([""])
        for symbol in sentence:
            if symbol in self.terminals:
                primeros.add(symbol)
                return primeros
            if symbol in self.non_terminals:
                for prod in self.productions:
                    if prod.left == symbol:
                        if prod not in visited:
                            visited.add(prod)
                            primeros.update(self._compute_first_rec(prod.right, visited))
                if "" not in primeros:
                    return primeros
                primeros.remove("")
            else:
                raise ValueError("Unexpected symbol found")

        primeros.add("")
        return primeros




    def compute_follow(self, symbol: str) -> AbstractSet[str]:
        """
        Method to compute the follow set of a non-terminal symbol.

        Args:
            symbol: non-terminal whose follow set is to be computed.

        Returns:
            Follow set of symbol.
        """

        return self._compute_follow_rec(symbol, set())

    def _compute_follow_rec(self, symbol: str, visited: AbstractSet[str]) -> AbstractSet[str]:
        siguientes = set()

        if symbol not in self.non_terminals:
            raise ValueError("Invalid symbol")

        if symbol == self.axiom:
            siguientes.add('$')

        for prod in self.productions:
            after = prod.right
            while symbol in after:
                idx = after.index(symbol)
                after = after[idx+1:]
                siguientes.update(self.compute_first(after))
            if "" in siguientes:
                siguientes.remove("")
                if prod.left not in visited:
                    visited.add(prod.left)
                    siguientes.update(self._compute_follow_rec(prod.left, visited))

        return siguientes


    def get_ll1_table(self) -> Optional[LL1Table]:
        """
        Method to compute the LL(1) table.

        Returns:
            LL(1) table for the grammar, or None if the grammar is not LL(1).
        """

        tabla = LL1Table(self.non_terminals, self.terminals, {})

        for prod in self.productions:
            for t in self.compute_first(prod.right):
                if t == '':
                    for s in self.compute_follow(prod.left):
                        try:
                            tabla.add_cell(TableCell(prod.left, s, prod.right))
                        except RepeatedCellError:
                            return None
                else:
                    try:
                        tabla.add_cell(TableCell(prod.left, t, prod.right))
                    except RepeatedCellError:
                        return None

        return tabla


    def is_ll1(self) -> bool:
        return self.get_ll1_table() is not None

class TableCell:
    """
    Cell of a LL1 table.

    Args:
        non_terminal: Non terminal symbol.
        terminal: Terminal symbol.
        right: Right part of the production rule.

    """

    def __init__(self, non_terminal: str, terminal: str, right: str) -> None:
        self.non_terminal = non_terminal
        self.terminal = terminal
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.non_terminal == other.non_terminal
            and self.terminal == other.terminal
            and self.right == other.right
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.non_terminal!r}, {self.terminal!r}, "
            f"{self.right!r})"
        )

    def __hash__(self) -> int:
        return hash((self.non_terminal, self.terminal))

class LL1Table:
    """
    LL1 table.

    Args:
        non_terminals: Set of non terminal symbols.
        terminals: Set of terminal symbols.
        cells: Cells of the table.

    """

    def __init__(
        self,
        non_terminals: AbstractSet[str],
        terminals: AbstractSet[str],
        cells: Collection[TableCell],
    ) -> None:

        if terminals & non_terminals:
            raise ValueError(
                "Intersection between terminals and non terminals "
                "must be empty.",
            )

        for c in cells:
            if c.non_terminal not in non_terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.non_terminal} is not included in the set "
                    f"of non terminals.",
                )
            if c.terminal not in terminals:
                raise ValueError(
                    f"{c}: "
                    f"{c.terminal} is not included in the set "
                    f"of terminals.",
                )
            for s in c.right:
                if (
                    s not in non_terminals
                    and s not in terminals
                ):
                    raise ValueError(
                        f"{c}: "
                        f"Invalid symbol {s}.",
                    )

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.cells = {(c.non_terminal, c.terminal): c.right for c in cells}

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"terminals={self.terminals!r}, "
            f"non_terminals={self.non_terminals!r}, "
            f"cells={self.cells!r})"
        )

    def add_cell(self, cell: TableCell) -> None:
        """
        Adds a cell to an LL(1) table.

        Args:
            cell: table cell to be added.

        Raises:
            RepeatedCellError: if trying to add a cell already filled.
        """
        if (cell.non_terminal, cell.terminal) in self.cells:
            raise RepeatedCellError(
                f"Repeated cell ({cell.non_terminal}, {cell.terminal}).")
        else:
            self.cells[(cell.non_terminal, cell.terminal)] = cell.right

    def analyze(self, input_string: str, start: str) -> ParseTree:
        """
        Method to analyze a string using the LL(1) table.

        Args:
            input_string: string to analyze.
            start: initial symbol.

        Returns:
            ParseTree object with either the parse tree (if the elective exercise is solved)
            or an empty tree (if the elective exercise is not considered).

        Raises:
            SyntaxError: if the input string is not syntactically correct.
        """

        exp = [start]
        input = list(input_string)
        input.reverse()
        tree = ParseTree(start)
        tree_stack = [tree]     # ParserTree version of exp stack

        while len(exp) > 0 and len(input) > 0:
            current = exp.pop()
            if current in self.terminals:
                if current == input[-1]:
                    input.pop()
                else:
                    raise SyntaxError(f"Unexpected symbol {input[-1]}")
            else:
                right_side = self.cells.get((current, input[-1]), None)
                if right_side is None:
                    raise SyntaxError(f"Unexpected symbol {input[-1]}")
                else:
                    aux = list(right_side)
                    aux.reverse()
                    exp.extend(aux)
                    # Parser Tree
                    current_node = tree_stack.pop()
                    if len(aux) > 0:
                        children = [ParseTree(ch) for ch in aux]
                        non_terminal_idx = ([i for i in range(len(aux)) if
                                             aux[i] in self.non_terminals])
                        tree_stack.extend([children[i] for i in
                                           non_terminal_idx])
                        children.reverse()
                    else:
                        children = [ParseTree('λ')]
                    current_node.add_children(children)

        if len(exp) != 0 or input != ['$']:
            raise SyntaxError("Ill-formed string")

        return tree

class ParseTree():
    """
    Parse Tree.

    Args:
        root: root node of the tree.
        children: list of children, which are also ParseTree objects.
    """
    def __init__(self, root: str, children: Collection[ParseTree] = []) -> None:
        self.root = root
        self.children = children

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.root!r}: {self.children})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return (
            self.root == other.root
            and len(self.children) == len(other.children)
            and all([x.__eq__(y) for x, y in zip(self.children, other.children)])
        )

    def add_children(self, children: Collection[ParseTree]) -> None:
        self.children = children
