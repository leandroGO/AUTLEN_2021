"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[a-zA-Z]+"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
RE1 = "[0-9a-zA-Z_]+.py"
RE2 = "-?(0|([1-9][0-9]*))?(\.[0-9]*)?"

nombreapellidoat = "[a-z]+\.[a-z]+@"
RE3 = nombreapellidoat + "(estudiante\.)?uam\.es"

np = "[^\(\)]*"     #not parenthesis
RE4 = "({0}\({0}\){0})*".format(np)
RE5 = "({0}\({0}(\({0}\){0})*{0}\){0})+".format(np)

"""
Recuerda que puedes usar el fichero prueba.py para probar tus
expresiones regulares.
"""

""" 
EJERCICIO 6:
Incluye a continuacion, dentro de esta cadena, tu respuesta 
al ejercicio 6.

... tu respuesta aqui...

"""
