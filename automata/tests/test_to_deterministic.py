"""Test evaluation of automatas."""
import unittest
from abc import ABC

from automata.automaton import FiniteAutomaton
from automata.utils import (AutomataFormat, deterministic_automata_isomorphism,
                            write_dot)

def save_automata_dot(n_test: int, automaton: FiniteAutomaton) -> None:
    return    # Comentar esta línea para generar los ficheros dot
    with open(f'automata_dot/to_deterministic_inicial_{n_test}.txt', 'w') as f:
        print(write_dot(automaton), file=f)

    with open(f'automata_dot/to_deterministic_final_{n_test}.txt', 'w') as f:
        print(write_dot(automaton.to_deterministic()), file=f)


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(
            expected,
            transformed,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1."""
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(1, automaton)

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            empty

            --> q0
            q0 -0-> qf
            q0 -1-> empty
            qf -0-> empty
            qf -1-> empty
            empty -0-> empty
            empty -1-> empty

        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Test Case 2.
        Un AFN-lambda que reconoce las cadenas de {1}* de longitud par,
        artificiosamente ampliado con transiciones lambda.

        Este test comprueba que se realiza la clausura-lambda correctamente.
        """
        automaton_str = """
        Automaton:
            Symbols: 1

            q0
            q1
            q2 final
            q3

            --> q0
            q0 --> q1
            q0 --> q2
            q1 --> q2
            q2 -1-> q3
            q3 -1-> q2
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(2, automaton)

        expected_str = """
        Automaton:
            Symbols: 1

            q0q1q2 final
            q2 final
            q3

            --> q0q1q2
            q0q1q2 -1-> q3
            q3 -1-> q2
            q2 -1-> q3
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case3(self) -> None:
        """Test Case 3.
        Un AFN-lambda que reconoce las cadenas de {1}* de longitud par,
        artificiosamente ampliado con transiciones lambda en bucle.

        Este test comprueba que se realiza la clausura-lambda correctamente.
        """
        automaton_str = """
        Automaton:
            Symbols: 1

            q0
            q1
            q2 final
            q3

            --> q0
            q0 --> q1
            q2 --> q0
            q1 --> q2
            q2 -1-> q3
            q3 -1-> q2
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(3, automaton)

        expected_str = """
        Automaton:
            Symbols: 1

            q0q1q2 final
            q3

            --> q0q1q2
            q0q1q2 -1-> q3
            q3 -1-> q0q1q2
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        """Test Case 4.
        Un AFN-lambda que reconoce las cadenas de {a,b,c}* conformadas por, a
        lo más, dos letras distintas, es decir, tales que exista un elemento de
        {a,b,c} que no esté en ellas.

        Este test comprueba que el AFN-lambda de entrada puede tener varios
        estados de aceptación.
        """
        automaton_str = """
        Automaton:
            Symbols: abc

            q0
            q1 final
            q2 final
            q3 final

            --> q0
            q0 --> q1
            q0 --> q2
            q0 --> q3
            q1 -a-> q1
            q1 -b-> q1
            q2 -a-> q2
            q2 -c-> q2
            q3 -b-> q3
            q3 -c-> q3
        """

        automaton = AutomataFormat.read(automaton_str)
        save_automata_dot(4, automaton)

        expected_str = """
        Automaton:
            Symbols: abc

            q0q1q2q3 final
            q1q2 final
            q1q3 final
            q2q3 final
            q1 final
            q2 final
            q3 final
            qe

            --> q0q1q2q3
            q0q1q2q3 -a-> q1q2
            q0q1q2q3 -b-> q1q3
            q0q1q2q3 -c-> q2q3
            q1q2 -a-> q1q2
            q1q2 -b-> q1
            q1q2 -c-> q2
            q1q3 -a-> q1
            q1q3 -b-> q1q3
            q1q3 -c-> q3
            q2q3 -a-> q2
            q2q3 -b-> q3
            q2q3 -c-> q2q3
            q1 -a-> q1
            q1 -b-> q1
            q1 -c-> qe
            q2 -a-> q2
            q2 -b-> qe
            q2 -c-> q2
            q3 -a-> qe
            q3 -b-> q3
            q3 -c-> q3
            qe -a-> qe
            qe -b-> qe
            qe -c-> qe
        """

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case5(self) -> None:
        """Test Case 5.
        Un AFN que reconoce las cadenas de {0,1}* que terminan en 0

        Este test comprueba que la función de transición del AFN puede ser
        multivaluada, es decir, conducir a dos estados distintos con el mismo
        símbolo.
        """
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> q0
            q0 -0-> qf
            q0 -1-> q0
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

    def test_case6(self) -> None:
        """Test Case 6.
        Un AFD que acepta cadenas de {0,1}* que terminan en 0.

        Este test comprueba que transforma AFD en ellos mismos.
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
        save_automata_dot(6, automaton)

        expected_str = automaton_str

        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

if __name__ == '__main__':
    unittest.main()
