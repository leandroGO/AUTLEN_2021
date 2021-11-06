from graphviz import Source
import os

for entry in os.scandir("automata_dot"):
    if entry.path.endswith(".txt"):
        Source.from_file(entry.path).render(os.path.splitext(entry.path)[0], format="png")
