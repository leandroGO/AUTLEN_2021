from graphviz import Source
import sys

if len(sys.argv) != 2:
    print(f"Debe ser 'python3 {sys.argv[0]} <filename>'")

else:
    with open(sys.argv[1], 'r') as f:
        s = Source.from_file(sys.argv[1])
        s.view()
