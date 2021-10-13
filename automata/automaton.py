"""Automaton implementation."""
from typing import Collection, Set, Dict, List

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        new_states: Set[State]
        new_states = set()
        tam = len(set_to_complete)

        for state in set_to_complete:
            for transition in self.transitions:
                if transition.initial_state == state and transition.symbol is None:
                    new_states.add(transition.final_state)

        set_to_complete.update(new_states)

        if len(set_to_complete) != tam:
            self._complete_lambdas(set_to_complete)

    def _new_states(self, orgin_set: Set[State], symbol: str) -> Set[State]:
        raise NotImplementedError("This method must be implemented.")

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        deterministic: FiniteAutomaton
        new_names: Dict[Set[State], str]
        evaluate: List[State]

        tag = 0
        initial_set = self._complete_lambdas({self.initial_state})
        new_names = {}
        evaluate = [initial_set]
        flag = True

        while evaluate:
            current_state = evaluate.pop()
            if current_state not in new_names:
                new_names[current_state] = f"Q{tag}"
                tag += 1

            for symbol in self.symbols:
                next_state = self._next_states(current_state, symbol)


        deterministic = FiniteAutomaton()
        raise NotImplementedError("This method must be implemented.")

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
