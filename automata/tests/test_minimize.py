"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import (AutomataFormat, deterministic_automata_isomorphism,
                            write_dot)

def save_automata_dot(n_test: int, automaton: FiniteAutomaton) -> None:
    return    # Comentar esta línea para generar los ficheros dot
    with open(f'automata_dot/to_minimized_inicial_{n_test}.txt', 'w') as f:
        print(write_dot(automaton), file=f)

    with open(f'automata_dot/to_minimized_final_{n_test}.txt', 'w') as f:
        print(write_dot(automaton.to_minimized()), file=f)


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_minimized()
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1.
        Un AFD que acepta cadenas de {1}* de longitud par, ampliado
        artificiosamente con estados adicionales.

        Este test comprueba que los estados que intuitivamente son equivalentes
        son "agrupados" correctamente.
        """
        automaton_str = """
        Automaton:
            Symbols: 1

            q0 final
            q1
            q2 final
            q3

            --> q0
            q0 -1-> q1
            q1 -1-> q2
            q2 -1-> q3
            q3 -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(1, automaton)

        expected_str = """
        Automaton:
            Symbols: 1

            q0 final
            qe

            --> q0
            q0 -1-> qe
            qe -1-> q0
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Test Case 2.
        Un AFD que acepta cadenas de {a,b,c}* que consten de un carácter
        seguido de una cadena de ces de longitud par (p.e. acccc, b y ccc son
        válidas).

        Este test comprueba que los estados que intuitivamente son equivalentes
        son "agrupados" correctamente. En concreto, que es innecesario
        condicionar por el primer carácter leído, pues las tres ramas posibles
        son equivalentes.
        """
        automaton_str = """
        Automaton:
            Symbols: abc

            q0
            q1 final
            q2
            q1r final
            q2r
            q1rr final
            q2rr
            qe

            --> q0
            q0 -a-> q1
            q1 -c-> q2
            q2 -c-> q1
            q1 -a-> qe
            q1 -b-> qe
            q2 -a-> qe
            q2 -b-> qe

            q0 -b-> q1r
            q1r -c-> q2r
            q2r -c-> q1r
            q1r -a-> qe
            q1r -b-> qe
            q2r -a-> qe
            q2r -b-> qe

            q0 -c-> q1rr
            q1rr -c-> q2rr
            q2rr -c-> q1rr
            q1rr -a-> qe
            q1rr -b-> qe
            q2rr -a-> qe
            q2rr -b-> qe

            qe -a-> qe
            qe -b-> qe
            qe -c-> qe
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(2, automaton)

        expected_str = """
        Automaton:
            Symbols: abc

            q0
            q1 final
            q2
            qe

            --> q0
            q0 -a-> q1
            q0 -b-> q1
            q0 -c-> q1
            q1 -c-> q2
            q2 -c-> q1
            q1 -a-> qe
            q1 -b-> qe
            q2 -a-> qe
            q2 -b-> qe
            qe -a-> qe
            qe -b-> qe
            qe -c-> qe
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        """Test Case 3.
        Un AFD mínimo que acepta cadenas de {0,1}* que terminan en 0.

        Este test comprueba que transforma AFD mínimos en ellos mismos.
        """
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
            q0 -1-> q0
            qf -0-> qf
            qf -1-> q0
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(3, automaton)

        expected_str = automaton_str

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        """Test Case 4.
        Un AFD mínimo que acepta cadenas de {0,1}* que terminan en 0, añadiendo
        un estado inaccesible.

        Este test comprueba que se eliminan los estados inaccesibles.
        """
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            inaccessible

            --> q0
            q0 -0-> qf
            q0 -1-> q0
            qf -0-> qf
            qf -1-> q0
            inaccessible -0-> q0
            inaccessible -1-> qf
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(4, automaton)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
            q0 -1-> q0
            qf -0-> qf
            qf -1-> q0
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case5(self) -> None:
        """Test Case 5.
        Un AFD mínimo que acepta cadenas de {0,1}* que terminan en 0, añadiendo
        dos estados inaccesibles que son accesibles entre sí

        Este test comprueba que se eliminan los estados inaccesibles.
        """
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            inaccessible1
            inaccessible2

            --> q0
            q0 -0-> qf
            q0 -1-> q0
            qf -0-> qf
            qf -1-> q0
            inaccessible1 -0-> q0
            inaccessible1 -1-> inaccessible2
            inaccessible2 -0-> inaccessible1
            inaccessible2 -1-> inaccessible2
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(5, automaton)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
            q0 -1-> q0
            qf -0-> qf
            qf -1-> q0
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)


if __name__ == '__main__':
    unittest.main()
