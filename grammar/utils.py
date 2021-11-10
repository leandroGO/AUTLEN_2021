from __future__ import annotations

import re
from collections import defaultdict
from typing import AbstractSet, DefaultDict

from grammar.grammar import Grammar, LL1Table, Production, ParseTree


class FormatParseError(Exception):
    """Exception for parsing problems."""


class GrammarFormat():
    re_comment = re.compile(r"\s*#\.*")
    re_empty = re.compile(r"\s*")
    re_production = re.compile(r"\s*(\S)\s*->\s*(\S*)\s*")

    @classmethod
    def read(cls, description: str) -> Grammar:
        splitted_lines = description.splitlines()

        terminals: AbstractSet[str] = set()
        non_terminals = set()
        productions = []
        axiom = None

        for line in splitted_lines:
            if cls.re_comment.fullmatch(line) or cls.re_empty.fullmatch(line):
                continue

            match = cls.re_production.fullmatch(line)
            if match:
                left, right = match.groups()
                if axiom is None:
                    axiom = left
                non_terminals.add(left)
                terminals = terminals | set(right)
                productions.append(Production(left, right))
            else:
                raise FormatParseError(f"Invalid line: {line}")

        terminals -= non_terminals

        assert axiom

        return Grammar(terminals, non_terminals, productions, axiom)

def write_table(table: LL1Table) -> str:
    col_widths: DefaultDict[str, int] = defaultdict(int)
    total_width = 0
    for t in table.terminals:
        for nt in table.non_terminals:
            width = 5
            if (nt, t) in table.cells:
                x = table.cells[(nt, t)]
                if x == '':
                    width += 2
                else:
                    width += len(x)
            if width > col_widths[t]:
                col_widths[t] = width
        total_width += col_widths[t] + 1

    table_str = "-" * (6 + total_width) + "\n"
    table_str += "      "
    for t in table.terminals:
        table_str += f"{t}" + " " * col_widths[t]
    table_str += "\n"
    table_str += "-" * (6 + total_width) + "\n"
    for nt in table.non_terminals:
        table_str += f"{nt}     "
        for t in table.terminals:
            if (nt, t) not in table.cells:
                table_str += " " * (col_widths[t] + 1)
                continue
            x = table.cells[(nt, t)]
            if x == '':
                table_str += "λ" + " " * (col_widths[t])
            else:
                table_str += f"{x}" + " " * (col_widths[t] - len(x) + 1)
        table_str += "\n"
    table_str += "-" * (6 + total_width)

    return table_str

def parse_tree_to_dot(ptree: ParseTree) -> str:
    return (
        "digraph {\n"
        "  rankdir=TB;\n"
        "\n"
        + parse_tree_to_dot_rec(ptree)
        + "}\n"
    )

def parse_tree_to_dot_rec(ptree: ParseTree) -> str:
    return (
        f'"node{id(ptree)}" [label="{ptree.root}", shape=circle]\n'
        + "\n".join([parse_tree_to_dot_rec(x) for x in ptree.children])
        + "\n".join([f"node{id(ptree)} -> node{id(x)}\n" for x in ptree.children])
    )
