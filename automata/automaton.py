"""Automaton implementation."""
from typing import Collection, Set, FrozenSet, Dict, List, Tuple, Optional

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
                if (transition.initial_state == state
                        and transition.symbol is None):
                    new_states.add(transition.final_state)

        set_to_complete.update(new_states)

        if len(set_to_complete) != tam:
            self._complete_lambdas(set_to_complete)

    def _new_states(self, origin_set: FrozenSet[State],
                    symbol: str) -> FrozenSet[State]:
        '''
        Devuelve el conjunto de estados a los que se puede llegar con el
        símbolo dado a partir del conjunto de estados actuales.
        '''
        new_states: Set[State]
        new_states = set()

        for state in origin_set:
            for transition in self.transitions:
                if (transition.initial_state == state
                        and transition.symbol == symbol):
                    new_states.add(transition.final_state)

        self._complete_lambdas(new_states)
        return frozenset(new_states)    # Inmutable y hasheable

    def _set_has_final_state(self, state_set: FrozenSet[State]) -> bool:
        '''
        Devuelve True si alguno de los estados del conjunto es final
        '''
        for state in state_set:
            if state.is_final:
                return True
        return False

    def to_deterministic(
            self,
            ) -> "FiniteAutomaton":
        deterministic: FiniteAutomaton
        new_names: Dict[FrozenSet[State], str]
        evaluate: List[FrozenSet[State]]
        transitions: (Set[Tuple[FrozenSet[State], Optional[str],
                                FrozenSet[State]]])
        new_states: Set[State]            # Los estados del nuevo autómata
        new_transitions: Set[Transition]  # Las transiciones del nuevo autómata
        melted_initial_set: Set[State]
        initial_set: FrozenSet[State]
        current_set: FrozenSet[State]
        next_set: FrozenSet[State]
        initial_state: State
        current_state: State
        next_state: State
        tag: int
        is_final: bool

        melted_initial_set = {self.initial_state}
        self._complete_lambdas(melted_initial_set)
        initial_set = frozenset(melted_initial_set)
        new_names = {initial_set: "Q0"}
        tag = 1
        evaluate = [initial_set]
        transitions = set()

        while evaluate:
            current_set = evaluate.pop()
            for symbol in self.symbols:
                next_set = self._new_states(current_set, symbol)
                if next_set not in new_names:
                    new_names[next_set] = f"Q{tag}"
                    tag += 1
                    evaluate.append(next_set)

                transitions.add((current_set, symbol, next_set))

        new_states = set()
        new_transitions = set()

        is_final = self._set_has_final_state(initial_set)
        initial_state = State(new_names[initial_set], is_final=is_final)
        new_states.add(initial_state)
        for transition in transitions:
            current_set = transition[0]
            next_set = transition[2]

            is_final = self._set_has_final_state(current_set)
            current_state = State(new_names[current_set], is_final=is_final)
            new_states.add(current_state)

            is_final = self._set_has_final_state(next_set)
            next_state = State(new_names[next_set], is_final=is_final)
            new_states.add(next_state)

            new_transitions.add(Transition(current_state, transition[1],
                                           next_state))

        return FiniteAutomaton(initial_state=initial_state,
                               states=new_states,
                               symbols=self.symbols,
                               transitions=new_transitions)

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
