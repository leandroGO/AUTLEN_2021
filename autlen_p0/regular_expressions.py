"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = r"[a-zA-Z]+"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
RE1 = r"[0-9a-zA-Z_]+.py"
RE2 = r"-?((0|([1-9][0-9]*))(\.[0-9]*)?|(\.[0-9]+))"

nombreApellidoAt = r"[a-z]+\.[a-z]+@"
RE3 = nombreApellidoAt + r"(estudiante\.)?uam\.es"

noParentesis = r"[^\(\)]*"
RE4 = r"({0}\({0}\){0})*".format(noParentesis)
RE5 = r"({0}\({0}(\({0}\){0})*{0}\){0})+".format(noParentesis)

"""
Recuerda que puedes usar el fichero prueba.py para probar tus
expresiones regulares.
"""

"""
EJERCICIO 6:
Incluye a continuacion, dentro de esta cadena, tu respuesta
al ejercicio 6.

Como se puede observar, la respuesta dada para los paréntesis anidados recrea
la estructura de los mismos manualmente (en la expresión se puede ver cómo se
abren dos niveles y luego se cierran). Es evidente que esto no se puede aplicar
para una profundidad infinita, ya que la expresión nunca terminaría (o debería
ser una expresión recurrente). El motivo por el que tampoco es posible
recrearlo por otros métodos es que las expresiones regulares carecen de un
sistema que permita 'memorizar' la profundidad que se alcanza en cada momento,
es decir, que contabilice el número de paréntesis abiertos menos el de
cerrados. Esta falta de memoria impide saber cuándo los paréntesis han sido
cerrados correctamente.

"""
