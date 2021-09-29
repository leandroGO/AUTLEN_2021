"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:

        raise NotImplementedError("This method must be implemented.")

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:

        raise NotImplementedError("This method must be implemented.")

    def is_accepting(self) -> bool:

        raise NotImplementedError("This method must be implemented.")
