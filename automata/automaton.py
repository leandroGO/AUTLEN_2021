"""Automaton implementation."""
from typing import Collection, Set, FrozenSet, Dict, List, Optional

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
        # Estados del nuevo autómata como valor
        new_states: Dict[FrozenSet[State], State]
        evaluate: List[FrozenSet[State]]
        # Transiciones del nuevo autómata
        transitions: Set[Transition]
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
        is_final = self._set_has_final_state(initial_set)
        initial_state = State("Q0", is_final=is_final)
        new_states = {initial_set: initial_state}
        tag = 1
        evaluate = [initial_set]
        transitions = set()

        while evaluate:
            current_set = evaluate.pop()
            for symbol in self.symbols:
                next_set = self._new_states(current_set, symbol)
                if next_set not in new_states:
                    is_final = self._set_has_final_state(next_set)
                    next_state = State(f"Q{tag}", is_final=is_final)
                    new_states[next_set] = next_state
                    tag += 1
                    evaluate.append(next_set)

                transitions.add(Transition(new_states[current_set],
                                           symbol, new_states[next_set]))

        return FiniteAutomaton(initial_state=initial_state,
                               states=new_states.values(),
                               symbols=self.symbols,
                               transitions=transitions)

    def _process_symbol(self, state: State, symbol: str) -> State:
        '''
        Devuelve el valor de la función de transición del AFD.
        '''
        for transition in self.transitions:
            if (transition.initial_state == state
                    and transition.symbol == symbol):
                return transition.final_state
        raise ValueError("Automaton is not complete")

    def _remove_inaccessible(self) -> "FiniteAutomaton":
        '''
        Elimina estados inaccesibles de un AFD.
        '''
        evaluate: List[State]
        accesible: Set[State]
        new_transitions: List[Transition]
        current_state: State
        new_state: State

        evaluate = [self.initial_state]
        accessible = {self.initial_state}
        new_transitions = []

        while evaluate:
            current_state = evaluate.pop()
            for symbol in self.symbols:
                next_state = self._process_symbol(current_state, symbol)
                if next_state not in accessible:
                    accessible.add(next_state)
                    evaluate.append(next_state)

        for transition in self.transitions:
            if transition.initial_state in accessible:
                new_transitions.append(transition)

        return FiniteAutomaton(initial_state=self.initial_state,
                               states=accessible,
                               symbols=self.symbols,
                               transitions=set(new_transitions))


    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        automaton: FiniteAutomaton
        states: List[State]
        aux: State
        tag: int
        change: bool
        n_states: int
        list1: List[Optional[int]]
        list2: List[Optional[int]]
        idx: int
        i1: int
        i2: int
        elim: Set[State]
        new_transitions: List[Transition]

        automaton = self._remove_inaccessible()
        states = list(automaton.states).copy()
        idx = states.index(automaton.initial_state)
        aux = states[idx]           # El estado inicial es el primero
        states[idx] = states[0]     # (así aseguramos que no se elimina)
        states[0] = aux

        change = True
        n_states = len(automaton.states)
        list1 = [int(state.is_final != states[0].is_final) for state in states]

        while change:
            tag = 0
            list2 = [None] * n_states
            while None in list2:
                idx = list2.index(None)
                list2[idx] = tag
                for i in range(idx + 1, n_states):
                    if not list2[i] and list1[idx] == list1[i]:
                        list2[i] = tag
                        for symbol in automaton.symbols:
                            i1 = states.index(
                                    automaton._process_symbol(states[idx],
                                                              symbol))
                            i2 = states.index(
                                    automaton._process_symbol(states[i],
                                                              symbol))
                            if list1[i1] != list1[i2]:
                                list2[i] = None
                                break
                tag += 1
            change = (list1 != list2)
            list1 = list2

        elim = set()
        new_transitions = list(automaton.transitions).copy()
        for i in range(n_states):
            for j in range(i + 1, n_states):
                if list1[i] == list1[j]:
                    elim.add(states[j])
                    for transition in new_transitions:
                        if transition.initial_state == states[j]:
                            transition.initial_state = states[i]
                        if transition.final_state == states[j]:
                            transition.final_state = states[i]

        for elem in elim:
            states.remove(elem)

        return FiniteAutomaton(initial_state=automaton.initial_state,
                               states=states, symbols=automaton.symbols,
                               transitions=set(new_transitions))
