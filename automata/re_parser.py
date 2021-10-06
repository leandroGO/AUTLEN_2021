"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser
from typing import Collection


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
        q0: State
        q0 = State('q0', is_final=False)

        qf: State
        qf = State('qf', is_final=True)

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=q0, states={q0, qf}, symbols=set(),
                              transitions=set())
        return aut

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        q0: State
        q0 = State('q0', is_final=False)
        qf: State
        qf = State('qf', is_final=True)

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=q0, states={q0, qf},
                              symbols=set(),
                              transitions={Transition(q0, None, qf)})
        return aut

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        q0: State
        q0 = State('q0', is_final=False)
        qf: State
        qf = State('qf', is_final=True)

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=q0, states={q0, qf},
                              symbols={symbol},
                              transitions={Transition(q0, symbol, qf)})
        return aut

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        qf: State
        qf = State('qf', is_final=True)

        states: Collection[State]
        states = set()
        transitions: Collection[Transition]
        transitions = set()
        self.state_counter = 0
        for state in automaton.states:
            self.state_counter += 1
            state.name = 'q' + str(self.state_counter)
            states.add(state)
            if state.is_final:
                transitions.add(Transition(state, None,
                                           automaton.initial_state))
                transitions.add(Transition(state, None, qf))
        states.add(qf)

        for transition in automaton.transitions:
            transitions.add(transition)
        transitions.add(Transition(automaton.initial_state, None, qf))

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=automaton.initial_state,
                              states=states, symbols=automaton.symbols,
                              transitions=transitions)
        return aut

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        qf: State
        qf = State('qf', is_final=True)
        q0: State
        q0 = State('q0', is_final=False)

        states: Collection[State]
        states = set()
        transitions: Collection[Transition]
        transitions = set()
        symbols: Collection[str]
        symbols = set()

        self.state_counter = 0
        for state in automaton1.states:
            self.state_counter += 1
            state.name = 'q' + str(self.state_counter)
            states.add(state)
            if state.is_final:
                transitions.add(Transition(state, None, qf))
        for state in automaton2.states:
            self.state_counter += 1
            state.name = 'q' + str(self.state_counter)
            states.add(state)
            if state.is_final:
                transitions.add(Transition(state, None, qf))
        states.add(q0)
        states.add(qf)

        for transition in automaton1.transitions:
            transitions.add(transition)
        for transition in automaton2.transitions:
            transitions.add(transition)

        transitions.add(Transition(q0, None, automaton1.initial_state))
        transitions.add(Transition(q0, None, automaton2.initial_state))

        for symbol in automaton1.symbols:
            symbols.add(symbol)
        for symbol in automaton2.symbols:
            symbols.add(symbol)

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=q0, states=states, symbols=symbols,
                              transitions=transitions)
        return aut

    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        states: Collection[State]
        states = set()
        transitions: Collection[Transition]
        transitions = set()
        symbols: Collection[str]
        symbols = set()

        self.state_counter = 0
        for state in automaton1.states:
            self.state_counter += 1
            state.name = 'q' + str(self.state_counter)
            if state.is_final:
                transitions.add(Transition(state, None,
                                           automaton2.initial_state))
                state.is_final = False
            states.add(state)
        for state in automaton2.states:
            self.state_counter += 1
            state.name = 'q' + str(self.state_counter)
            states.add(state)

        for transition in automaton1.transitions:
            transitions.add(transition)
        for transition in automaton2.transitions:
            transitions.add(transition)

        for symbol in automaton1.symbols:
            symbols.add(symbol)
        for symbol in automaton2.symbols:
            symbols.add(symbol)

        aut: FiniteAutomaton
        aut = FiniteAutomaton(initial_state=automaton1.initial_state,
                              states=states, symbols=symbols,
                              transitions=transitions)
        return aut
