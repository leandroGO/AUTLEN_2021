from ast_utils import ASTReplaceNum, transform_code


def my_fun(p):
    if p == 1:
        print(p + 1j)
    elif p == 5:
        print(0)
    else:
        print(p - 27.3 * 3j)


num_replacer = ASTReplaceNum(3)
new_fun = transform_code(my_fun, num_replacer)

new_fun(1)
# Debería imprimir -8

new_fun(3)
# Debería imprimir 6
