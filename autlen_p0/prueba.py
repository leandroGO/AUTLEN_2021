#!/usr/bin/env python

import re

from regular_expressions import RE0, RE1, RE2, RE3, RE4, RE5

def check_expression(expr: str, string: str, expected: bool) -> None:
    return re.fullmatch(expr, string)


if re.fullmatch(RE2, "."):
    print("OK")
else:
    print("ERROR")
