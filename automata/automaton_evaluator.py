"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        next_states: Set[_State]
        next_states = set()

        if symbol is not None and symbol not in self.automaton.symbols:
            raise ValueError(
                f"Symbol {symbol} "
                f"is not in the set of symbols",
            )

        for state in self.current_states:
            for transition in self.automaton.transitions:
                if state == transition.initial_state and symbol == transition.symbol:
                    next_states.add(transition.final_state)

        self._complete_lambdas(next_states)
        self.current_states = next_states


    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        new_states: Set[_State]
        new_states = set()
        tam = len(set_to_complete)

        for state in set_to_complete:
            for transition in self.automaton.transitions:
                if transition.initial_state == state and transition.symbol is None:
                    new_states.add(transition.final_state)

        set_to_complete.update(new_states)

        if len(set_to_complete) != tam:
            self._complete_lambdas(set_to_complete)


    def is_accepting(self) -> bool:
        for state in self.current_states:
            if state.is_final:
                return True

        return False
